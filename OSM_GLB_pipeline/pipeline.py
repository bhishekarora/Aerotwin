#!/usr/bin/env python3
"""
osm_to_glb_blender.py

Convert OSM (.osm or .pbf) building data directly into a GLB file for digital twins.

Usage:
    blender --background --python osm_to_glb_blender.py -- input.osm output.glb [default_height_m]

Example:
    blender --background --python osm_to_glb_blender.py -- data/delhi_airport.osm data/delhi_airport.glb 8

Requirements:
    - Blender installed
    - Python modules `osmnx`, `shapely`, `geopandas` available in Blender's Python environment
      (Install via: blender_python -m pip install osmnx shapely geopandas)

What it does:
    - Reads buildings from an OSM file using osmnx
    - Extracts height or building:levels (default 3m per level)
    - Generates 3D extruded meshes in Blender
    - Assigns basic materials
    - Exports as GLB
"""

import bpy
import bmesh
import sys
import os
import math

# -----------------------------
# CLI Arguments
# -----------------------------
argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []

if len(argv) < 2:
    print("Usage: blender --background --python osm_to_glb_blender.py -- input.osm output.glb [default_height_m]")
    sys.exit(1)

input_osm = argv[0]
output_glb = argv[1]
default_height = float(argv[2]) if len(argv) >= 3 else 10.0
levels_to_meters = 3.0

print(f"[INFO] Input OSM: {input_osm}")
print(f"[INFO] Output GLB: {output_glb}")
print(f"[INFO] Default height: {default_height} m")

# -----------------------------
# Import OSMNX
# -----------------------------
try:
    import osmnx as ox
except ImportError as e:
    print("ERROR: osmnx is not installed in Blender's Python.")
    print("Run: blender_python -m pip install osmnx shapely geopandas")
    sys.exit(1)

# -----------------------------
# Load OSM Building Data
# -----------------------------
print("[INFO] Parsing OSM file...")
tags = {"building": True}
gdf = ox.geometries_from_xml(input_osm, tags=tags)

if gdf.empty:
    print("[ERROR] No buildings found in the OSM file.")
    sys.exit(1)

print(f"[INFO] Found {len(gdf)} building features")

# -----------------------------
# Clear Blender Scene
# -----------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)

clear_scene()

# -----------------------------
# Coordinate Projection: Web Mercator
# -----------------------------
R = 6378137.0
def lonlat_to_mercator(lon, lat):
    x = R * math.radians(lon)
    lat = max(min(lat, 89.9), -89.9)
    y = R * math.log(math.tan(math.pi / 4.0 + math.radians(lat) / 2.0))
    return x, y

# -----------------------------
# Prepare Blender Mesh Creation
# -----------------------------
def ensure_ccw(ring):
    s = 0.0
    for i in range(len(ring)):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % len(ring)]
        s += (x2 - x1) * (y2 + y1)
    return list(reversed(ring)) if s > 0 else ring

def create_extruded_mesh(name, coords, height):
    """Create extruded 3D mesh from footprint coords."""
    mesh = bpy.data.meshes.new(name + "_mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    verts = [bm.verts.new((x, y, 0)) for x, y in coords]
    bm.verts.ensure_lookup_table()
    try:
        face = bm.faces.new(verts)
    except:
        bm.free()
        return None

    bm.faces.ensure_lookup_table()
    ret = bmesh.ops.extrude_face_region(bm, geom=[face])
    extruded_verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=extruded_verts, vec=(0, 0, height))
    bm.to_mesh(mesh)
    bm.free()
    return obj

# -----------------------------
# Center the Scene
# -----------------------------
print("[INFO] Centering coordinates...")
all_points = []
for idx, row in gdf.iterrows():
    geom = row.geometry
    if geom.is_empty:
        continue
    if geom.geom_type == "Polygon":
        all_points.extend(list(geom.exterior.coords))
    elif geom.geom_type == "MultiPolygon":
        for poly in geom.geoms:
            all_points.extend(list(poly.exterior.coords))

if not all_points:
    print("[ERROR] No geometry points found.")
    sys.exit(1)

merc_points = [lonlat_to_mercator(lon, lat) for lon, lat in all_points]
cx = sum(p[0] for p in merc_points) / len(merc_points)
cy = sum(p[1] for p in merc_points) / len(merc_points)

# -----------------------------
# Create Buildings
# -----------------------------
print("[INFO] Creating buildings...")
count = 0
for idx, row in gdf.iterrows():
    geom = row.geometry
    if geom.is_empty:
        continue

    # Determine building height
    h = None
    if "height" in row and row["height"] not in [None, ""]:
        try:
            h = float(str(row["height"]).replace("m", ""))
        except:
            h = None
    if h is None and "building:levels" in row and row["building:levels"] not in [None, ""]:
        try:
            h = float(row["building:levels"]) * levels_to_meters
        except:
            h = None
    if h is None:
        h = default_height

    # Geometry handling
    if geom.geom_type == "Polygon":
        coords = [lonlat_to_mercator(lon, lat) for lon, lat in geom.exterior.coords]
        coords = [(x - cx, y - cy) for x, y in coords]
        coords = ensure_ccw(coords)
        obj = create_extruded_mesh(f"building_{count}", coords, h)
        if obj:
            count += 1

    elif geom.geom_type == "MultiPolygon":
        for poly in geom.geoms:
            coords = [lonlat_to_mercator(lon, lat) for lon, lat in poly.exterior.coords]
            coords = [(x - cx, y - cy) for x, y in coords]
            coords = ensure_ccw(coords)
            obj = create_extruded_mesh(f"building_{count}", coords, h)
            if obj:
                count += 1

print(f"[INFO] Created {count} buildings")

# -----------------------------
# Assign Simple Material
# -----------------------------
def assign_material(obj, color=(0.7, 0.7, 0.7, 1.0)):
    mat = bpy.data.materials.get("BuildingMaterial")
    if mat is None:
        mat = bpy.data.materials.new(name="BuildingMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Roughness"].default_value = 0.8
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)

for obj in bpy.context.collection.objects:
    if obj.type == "MESH":
        assign_material(obj)

# -----------------------------
# Export to GLB
# -----------------------------
os.makedirs(os.path.dirname(output_glb), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=output_glb, export_format='GLB', export_materials='EXPORT')

print(f"[INFO] Export complete: {output_glb}")
