import React, { useState } from "react";
import "./Attendance.css";

const Attendance = () => {
  const [message, setMessage] = useState("");

  const handleAction = (action) => {
    if (action === "signIn") {
      setMessage("Tap your card to sign in!");
    } else if (action === "signOut") {
      setMessage("Mentor tap first, then student tap to sign out!");
    } else if (action === "status") {
      setMessage("Checking attendance status...");
    } else if (action === "bulkSignOut") {
      setMessage("Bulk sign-out in progress...");
    } else {
      setMessage("");
    }
  };

  return (
    <div className="page">
      <div className="navbar">
        <button className="nav-button home" onClick={() => setMessage("")}>G-House 354 </button>
        <button className="nav-button admin"onClick={() => setMessage("")}>Home</button>
      </div>


      <div className="button-container">
        {message ? (
          <div className="message-box">
            <h1>{message}</h1>
          </div>
        ) : (
          <div className="button-grid">
            <button className="btn sign-in" onClick={() => handleAction("signIn")}>Sign In</button>
            <button className="btn sign-out" onClick={() => handleAction("signOut")}>Sign Out</button>
            <button className="btn status" onClick={() => handleAction("status")}>Status</button>
            <button className="btn bulk-signout" onClick={() => handleAction("bulkSignOut")}>Bulk Sign Out</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Attendance;
