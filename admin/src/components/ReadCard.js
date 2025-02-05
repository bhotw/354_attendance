import React, { useState, useEffect } from "react";
import api from "../axiosInstance";
import Navbar from "../components/Navbar";
import "./ReadCard.css";
import { useNavigate } from "react-router-dom";

const ReadCard = () => {
  const [message, setMessage] = useState("Tap a card to read...");
  const [cardData, setCardData] = useState(null);
  const [isReading, setIsReading] = useState(false);
  const navigate = useNavigate();

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

      const response = await api.get("/api/card/read", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.data.status === "success") {
        setCardData({ id: response.data.card_id, name: response.data.name });
        setMessage("Card read successfully!");
      } else {
        setMessage(`Error: ${response.data.message}`);
      }
    } catch (error) {
      console.error("Read card error:", error);
      setMessage(`Error: ${error.response?.data?.message || "Server error"}`);
    } finally {
      setIsReading(false);
    }
  };

  return (
  <div>
    <Navbar/>
    <div className="read-card">
      <h2>Read RFID Card</h2>
      <p className="status-message">{message}</p>

      <button className="btn read-button" onClick={handleRead} disabled={isReading}>
        Read Card
      </button>

      {cardData && (
        <div className="card-info">
          <p><strong>Card ID:</strong> {cardData.id}</p>
          <p><strong>Name:</strong> {cardData.name}</p>
        </div>
      )}
    </div>
    </div>
  );
};

export default ReadCard;
