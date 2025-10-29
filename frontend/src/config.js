// API Configuration
const config = {
  // Use environment variable if available, otherwise default to production
  API_URL: process.env.REACT_APP_API_URL || "https://sentrix-1.onrender.com",

  // For local development, uncomment the line below:
  // API_URL: 'http://localhost:8000',
};

export default config;
