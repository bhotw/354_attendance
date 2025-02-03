import axios from "axios";

const api = axios.create({
  baseURL: `http://${window.location.hostname}:5000`, // Set your API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
