import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axiosInstance";
import "./WriteToCard.css";
import Navbar from "../components/Navbar";

const WriteToCard = ({ onComplete }) => {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("Enter a name and tap the card...");
  const [isWriting, setIsWriting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  const handleWrite = async () => {
    if (!name.trim()) {
      setMessage("Error: Please enter a name.");
      return;
    }

    setIsWriting(true);
    setMessage("Waiting for card... Tap now.");

    try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
        }
      const response = await api.post(
        "/api/card/write",
        { name },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.status === "success") {
        const card_id = response.data.card_id;
        const card_name = response.data.card_name;
        setMessage(`Success! "${card_name}" written to the "${card_id}".`);

      } else {
        setMessage(`Error: ${response.data.message}`);
      }
    } catch (error) {
      console.error("Write to card error:", error);
      setMessage(`Error: ${error.response?.data?.message || "Server error"}`);
    } finally {
      setIsWriting(false);
    }
  };

  return (
  <div>
    <Navbar/>
    <div className="write-to-card">
      <h2>Write Name to RFID Card</h2>

      <input
        type="text"
        className="name-input"
        placeholder="Enter name..."
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={isWriting}
      />

      <p className="status-message">{message}</p>

      <button className="btn write-button" onClick={handleWrite} disabled={isWriting}>
        Write to Card
      </button>
    </div>
    </div>
  );
};

export default WriteToCard;
