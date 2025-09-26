# Aerotwin
Digital Twin for Airports with 360 integrations on air and land side

![Alt text for the image](aerotwinplatform.jpeg "Optional title for the image") 
AeroTwin is a modular, plug-and-play digital twin for modern airports and airside operations. It combines highly realistic 3D modeling with live or simulated aircraft movements, offering a unified view of land and airside activities.

## Key Features of AeroTwin

Our AeroTwin platform offers a comprehensive suite of features designed to revolutionize airport operations and training:

* **Realistic 3D Environments:** Experience highly detailed and accurate 3D representations of terminals, aprons, and runways, providing an immersive and true-to-life operational view.
* **Game Engine-like Simulations:** Benefit from realistic simulations of aircraft landings and departures on runways, powered by advanced game engine technology for unparalleled visual fidelity and physics.
* **Dynamic Aircraft Movement:** Real-time aircraft movement simulation integrated with live transponder data, offering an accurate and up-to-the-minute view of airside activity.
* **Seamless System Integration:** Robust capabilities for integration with existing airport systems, supporting both synchronous and asynchronous (queue-based) communication methods.
* **Integrated RF Communications:** Comprehensive simulation of radio frequency communications, including cockpit-to-ATC interactions, ACARS (Aircraft Communications Addressing and Reporting System), ATIS (Automatic Terminal Information Service), and NOTAMs (Notices to Airmen).
* **API-Driven Platform:** A powerful API (Application Programming Interface) driven platform facilitating easy and flexible integration with various airport management systems such as AMS (Airport Management System), MRO (Maintenance, Repair, and Overhaul), and BHS (Baggage Handling System).
* **Advanced Operational Insights:** Integration with real-time weather data, Turnaround Time (TAT) predictions, intelligent stand allocations, and comprehensive KPI (Key Performance Indicator) integration for optimized decision-making and performance monitoring.


# Enabled Features
- **3D Airport Visualization**: Interactive 3D airport model using JS
- **Real-time Weather**: Live weather data from Open-Meteo API
- **Plane Management**: Dynamic plane positioning and rotation
- **Stand Management**: Aircraft stand configuration and control
- **Real-time Communication**: WebSocket and RabbitMQ integration
- **Ops Chat**: Real-time operations chat (Socket.IO) with presence and rolling feed
- **Apron Watch**: Video analytics overlay (Visionflow) with event logging and CDM updates
- **Control Panel**: Interactive controls for managing the digital twin
- **Responsive Design**: Modern UI with Angular Material
- 

![Alt text for the image](aerotwin.gif "Optional title for the image") 

## Technology Stack

### Frontend
- **Angular 17**: Modern web framework
- **CES**: 3D geospatial visualization
- **Angular Material**: UI components
- **Socket.IO Client**: Real-time communication (chat, plane/stand updates)
- **RxJS**: Reactive programming

### Backend
- **Node.js**: Server runtime
- **Express**: Web framework
- **MongoDB**: NoSQL database
- **RabbitMQ**: Message broker
- **Socket.IO**: Real-time communication (chat, alerts, plane/stand updates)
- **Mongoose**: MongoDB ODM

### External APIs
- **Open-Meteo**: Free weather API
- **Ion**: 3D terrain and imagery
- **Vision**: Serverless inference workflow (Apron Watch)

## Prerequisites

- Node.js 18+ and npm
- MongoDB 5+
- RabbitMQ 3.8+
- Angular CLI 17+

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd airport-digital-twin
```

### 2. Install Dependencies
```bash
# Install Angular dependencies
npm install

# Install backend dependencies
cd server
npm install
cd ..
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
# Server Configuration
PORT=3000
NODE_ENV=development

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/airport-digital-twin

# RabbitMQ Configuration
RABBITMQ_URL=amqp://localhost

# viewer Configuration
viewer_ACCESS_TOKEN=your_token_here

# Weather API Configuration
WEATHER_UPDATE_INTERVAL=300000
```

### 4. Database Setup
Start MongoDB:
```bash
# On Windows
"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"

# On macOS/Linux
mongod
```

### 5. RabbitMQ Setup
Install and start RabbitMQ:
```bash
# On Windows (using Chocolatey)
choco install rabbitmq

# On macOS
brew install rabbitmq

# Start RabbitMQ
rabbitmq-server
```

### 6. Asset Files
Place the following files in `src/assets/`:
- `airport.geojson` - Airport GeoJSON data
- `stands.csv` - Stand configuration data
- `building.glb` - Terminal 3 3D model
- `aircraftSJ.glb` - SpiceJet plane model
- `aircraft6E.glb` - Indigo plane model
- `RTSP sample` - Apron Watch sample video
- `icons` - Icons for Ops Chat and Apron Watch

## Running the Application

### Development Mode
```bash
# Terminal 1: Start the backend server (Socket.IO + APIs)
npm run backend

# Terminal 2: Start the Angular dev server
npm run start

# Or run both simultaneously
npm run dev
```

### Production Build
```bash
# Build the Angular application
npm run build

# Start the production server
npm run backend
```

## Project Structure

```
airport-digital-twin/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── viewer/
│   │   │   ├── weather-widget/
│   │   │   └── control-panel/
│   │   ├── services/
│   │   │   ├── data.service.ts
│   │   │   ├── weather.service.ts
│   │   │   └── message.service.ts
│   │   ├── app.component.ts
│   │   └── app.module.ts
│   ├── assets/
│   │   ├── del.geojson
│   │   ├── stands.csv
│   │   ├── t3.glb
│   │   ├── sj.glb
│   │   └── indigo.glb
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── server/
│   └── server.js
├── package.json
├── angular.json
├── tsconfig.json
└── README.md
```    

## Architecture 
- Integrates seamless with all Layer 7 (AMS/Xovis/Weather/Supervisory(SCADA/BMS/EMS)) and layer 4 systems (modbus/snmp/ILS/Radars)
- ### Supervisory
- SCADA/BMS/EMS
- ### Modbux/SNMP (ILS/RADAR/PBB)
- Supported via Slave configs and RS-485/Rs-232 adapter dongles (hardware cost around 7k INR per integration, all serial TTL systems supported) 
- ### Layer 7 MQTT (parsers for Asterix)
- Supported via Transformers/Bridge/Wrappers

- 
![Alt text for the image](AT_A.png "Optional title for the image") 

## Real-time Features

### WebSocket Events
- `plane-update` - Plane position/rotation updates
- `stand-update` - Stand configuration changes
- `weather-update` - Weather data updates
- `system-command` - System control commands

### RabbitMQ Queues
-MQTT and sequence based support





## Troubleshooting

### Common Issues

1. **Scene not loading**
   - Check  access token
   - Verify asset files are in correct location
   - Check browser console for errors

2. **MongoDB connection failed**
   - Ensure MongoDB is running
   - Check connection string in .env
   - Verify database permissions

3. **RabbitMQ connection failed**
   - Ensure RabbitMQ is running
   - Check connection URL
   - Verify queue permissions

4. **Angular build errors**
   - Clear node_modules and reinstall
   - Check TypeScript version compatibility
   - Verify Angular CLI version

### Performance Optimization

1. **3D Performance**
   - Reduce model complexity
   - Optimize texture sizes
   - Use LOD (Level of Detail)

2. **Network Performance**
   - Enable compression
   - Use CDN for static assets
   - Optimize API responses



## Future Enhancements on Digital twin Airport Ops

- [ ] Airport Agent with MCP support
- [ ] Arrivals at T3 with BHS integration
- [ ] Advanced cockpit integration
- [ ] Resilient ACDM
- [ ] Advanced Chaos Management


# ATC ACARS integration 
![Alt text for the image](aerotwin_acars.gif "Optional title for the image") 

# Codebase & support for above
- mail me at arora.abhishek@outlook.com
- 
