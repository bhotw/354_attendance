import React, { useState,useEffect  } from "react";
import { useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import "./Attendance.css";
import api, { API_BASE_URL } from "../axiosInstance";

const socket = io(API_BASE_URL);

const Attendance = () => {
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Listen for different bulk sign-out events from the server
    const handleBulkSignOutUpdate = (data) => setMessage(data.message);
    const handleBulkSignOutError = (data) => setMessage(data.message);
    const handleBulkSignOutComplete = (data) => setMessage(data.message);

    socket.on("bulk_sign_out_update", handleBulkSignOutUpdate);
    socket.on("bulk_sign_out_error", handleBulkSignOutError);
    socket.on("bulk_sign_out_complete", handleBulkSignOutComplete);

    // Cleanup on unmount by removing all event listeners
    return () => {
      socket.off("bulk_sign_out_update", handleBulkSignOutUpdate);
      socket.off("bulk_sign_out_error", handleBulkSignOutError);
      socket.off("bulk_sign_out_complete", handleBulkSignOutComplete);
    };
  }, []);

  const handleAction = async (action) => {
    try {
      let response;

      if (action === "signIn") {
        setMessage("Tap your card to sign in!");
        response = await api.post("/api/attendance/sign-in");
        autoReset(2);
      } else if (action === "signOut") {
        setMessage("Mentor tap first for authorization.");
        response = await api.post("/api/attendance/mentor-auth");
        if(response.data.status !== "success"){
            setMessage(`Error: ${response.data.message}`);
            autoReset(5);
            return;
        }
        setMessage("Mentor Authorized! Student tap to Sign Out.");
        await new Promise(resolve => setTimeout(resolve, 2000));
        response = await api.post("/api/attendance/sign-out");
        autoReset(2);
      } else if (action === "status") {
        setMessage("Tap your card to check status...");
        response = await api.get("/api/attendance/status");
        if (response.data.status ==="success") {
            setMessage(response.data.message);
        } else {
            setMessage(`Error: ${response.data.message}`);
        }
        autoReset(15);
      } else if (action === "bulkSignOut") {
        setMessage("Mentor tap first for authorization.");
        response = await api.post("/api/attendance/mentor-auth");
        if(response.data.status !== "success"){
            setMessage(`Error: ${response.data.message}`);
            autoReset(2);
            return;
        }
        setMessage("Bulk sign-out mode activated. Students can now tap.");
        response = await api.post("/api/attendance/bulk-sign-out");
        socket.emit("bulk_sign_out_start");


        autoReset(40);
      } else if (action === "clear"){
        response = await api.post("/api/attendance/clear")
        if(response.data.status !== "success"){
            setMessage(`Error: ${response.data.message}`);
            autoReset(2);
            return;
        }
        setMessage(response.data.message)
        autoReset(2);
        return;
      }
       else {
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
  const clearReader = async () => {
    try {
        setMessage("");
        navigate("/");
        const response = await api.post("/api/attendance/clear");
    } catch (error) {
        console.error("Error cleaning reader.", error);

    }
  };

  const autoReset = (seconds) => {
    setTimeout( async () => {
        clearReader();
    }, seconds * 1000);
  };

  return (
    <div className="page">
      <div className="navbar-atten">
        <button className="nav-logo" onClick={() => setMessage("")}>
          G-House 354
        </button>
        <button className="nav-home" onClick={() => handleAction("clear")}>
          Clear
        </button>
      </div>

      <div className="button-container-atten">
        {message ? (
          <div className="message-box">
            <h1>{message}</h1>
          </div>
        ) : (
          <div className="button-grid-atten">
            <button className="btn_attendance sign-in" onClick={() => handleAction("signIn")}>
              Sign In
            </button>
            <button className="btn_attendance sign-out" onClick={() => handleAction("signOut")}>
              Sign Out
            </button>
            <button className="btn_attendance status" onClick={() => handleAction("status")}>
              Status
            </button>
            <button className="btn_attendance bulk-signout" onClick={() => handleAction("bulkSignOut")}>
              Bulk Sign Out
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Attendance;
