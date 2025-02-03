import React, { useState } from "react";
import { useNavigate, navigate } from "react-router-dom";
import "./Attendance.css";
import api from "../axiosInstance";

const Attendance = () => {
  const [message, setMessage] = useState("");
  const navigate = useNavigate()

  const handleAction = async (action) => {
    try {
      let response;

      if (action === "signIn") {
        setMessage("Tap your card to sign in!");
        response = await api.post("/api/attendance/sign-in");
        autoReset(5);
      } else if (action === "signOut") {
        setMessage("Mentor tap first, then student tap to sign out!");
        response = await api.post("/api/attendance/sign-out");
        autoReset(10);
      } else if (action === "status") {
        setMessage("Checking attendance status...");
        response = await api.get("/api/attendance/status");
        autoReset(15);
      } else if (action === "bulkSignOut") {
        setMessage("Bulk sign-out in progress...");
        response = await api.post("/api/attendance/bulk-sign-out");
        autoReset(10);
      } else {
        setMessage("");
        return;
      }

      if (response.data.status === "success") {
        setMessage(response.data.message);
        autoReset(5);
      } else {
        setMessage(`Error: ${response.data.message}`);
        autoReset(5);
      }
    } catch (error) {
      console.error(`Error during ${action}:`, error);
      setMessage(`Error: ${error.response?.data?.message || "Server error"}`);
      autoReset(5);
    }
  };

    const autoReset = (seconds) => {
    setTimeout(() => {
      setMessage("");
      navigate("/");
    }, seconds * 1000);
  };

  return (
    <div className="page">
      <div className="navbar">
        <button className="nav-button home" onClick={() => setMessage("")}>
          G-House 354
        </button>
        <button className="nav-button admin" onClick={() => setMessage("")}>
          Home
        </button>
      </div>

      <div className="button-container">
        {message ? (
          <div className="message-box">
            <h1>{message}</h1>
          </div>
        ) : (
          <div className="button-grid">
            <button className="btn sign-in" onClick={() => handleAction("signIn")}>
              Sign In
            </button>
            <button className="btn sign-out" onClick={() => handleAction("signOut")}>
              Sign Out
            </button>
            <button className="btn status" onClick={() => handleAction("status")}>
              Status
            </button>
            <button className="btn bulk-signout" onClick={() => handleAction("bulkSignOut")}>
              Bulk Sign Out
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Attendance;
