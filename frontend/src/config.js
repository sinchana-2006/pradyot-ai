/**
 * Frontend configuration - loads from environment variables.
 * Vite exposes only variables prefixed with VITE_ to the client.
 * Never hardcode API URLs or secrets here.
 */

// Backend API base URL - set VITE_API_URL in .env (default: local FastAPI)
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
