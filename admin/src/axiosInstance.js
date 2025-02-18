import axios from "axios";

const API_BASE_URL = `http://${window.location.hostname}:5000`; // Set API base URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export { API_BASE_URL }; // Export the base URL for use in other files
export default api;