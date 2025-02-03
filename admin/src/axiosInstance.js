import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.1.27:5000", // Set your API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
