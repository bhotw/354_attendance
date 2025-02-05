import React, { useState, useEffect } from "react";
import api from "../axiosInstance";
import "./ReadUserCard.css";
import { useNavigate } from "react-router-dom";

const ReadUserCard = () => {
  const [message, setMessage] = useState("Tap a card to get user details...");
  const [userData, setUserData] = useState(null);
  const [isReading, setIsReading] = useState(false);
  const navigate = useNavigate();

  // ✅ Check authentication when component loads
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

    const handleRead = async () => {
      setIsReading(true);
      setMessage("Waiting for card... Tap now.");

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }

        const response = await api.get("/api/card/read_user", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.data.status === "success") {
          setUserData(response.data.user);
          setMessage("User details retrieved successfully!");
        } else {
          setMessage("Error: Card is not in our team.");
          setUserData(null);
        }
      } catch (error) {
        console.error("Read user card error:", error);
        setMessage(`Error: ${error.response?.data?.message || "Server error"}`);
        setUserData(null);
      } finally {
        setIsReading(false);
      }
    };

  };

  return (
    <div className="read-user-card">
      <h2>Read User RFID Card</h2>
      <p className="status-message">{message}</p>

      <button className="btn read-button" onClick={handleRead} disabled={isReading}>
        Read User Card
      </button>

      {userData && (
        <div className="user-info">
          <p><strong>User Id:</strong> {userData.id}</p>
          <p><strong>Card Id:</strong> {userData.card_id}</p>
          <p><strong>Name:</strong> {userData.name}</p>
          <p><strong>Role:</strong> {userData.role}</p>
          <p><strong>Email:</strong> {userData.email}</p>
          <p><strong>Phone:</strong> {userData.phone_number}</p>
          <p><strong>Emergency Contact:</strong> {userData.emergency_contact_name || "N/A"}</p>
          <p><strong>Emergency Contact Phone:</strong> {userData.emergency_contact_phone || "N/A"}</p>
          <p><strong>Parent's Email:</strong> {userData.parents_email || "N/A"}</p>
        </div>
      )}
    </div>
  );
};

export default ReadUserCard;
