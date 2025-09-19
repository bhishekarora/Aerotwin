// Central feature flag configuration
// Claude Sonnet 4 enabled globally for all clients.
export interface FeatureFlags {
  CLAUDE_SONNET_4: boolean;
}

export const FEATURE_FLAGS: FeatureFlags = {
  CLAUDE_SONNET_4: true,
};

// Helper accessor (future-proof if you later fetch from backend)
export function isClaudeSonnet4Enabled(): boolean {
  return FEATURE_FLAGS.CLAUDE_SONNET_4;
}

// Usage (Angular component/service):
// import { isClaudeSonnet4Enabled } from './config/feature-flags';
// if (isClaudeSonnet4Enabled()) { /* model-specific logic */ }