import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axiosInstance";
import './AddCard.css';

const AddCard = () => {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState("");
  const [message, setMessage] = useState("");
  const [cardId, setCardId] = useState("");
  const navigate = useNavigate();

  // Fetch users on component mount
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
        }
        const response = await api.get("/api/add_card/users", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, [navigate]);

  // Handle card assignment
  const handleAddCard = async () => {
    if (!selectedUserId) {
      setMessage("Please select a user.");
      return;
    }

    setMessage("Tap a card to add...");

    try {
      const token = localStorage.getItem("token");
      const response = await api.post(
        "/api/add_card/add_new_card",
        { user_id: selectedUserId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const { status, message: responseMessage } = response.data;
      if (status === "success") {
        setMessage(`✅ Card successfully assigned to ${response.data.message}`);
        setCardId(response.data.card_id);
      } else {
        setMessage(responseMessage || "❌ Failed to add card.");
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.message) {
        setMessage(error.response.data.message);
      } else {
        setMessage("❌ Failed to add card.");
      }
      console.error("Error adding card:", error);
    }
  };

  return (
    <div className="add-card-container">
      <h2>Add New Card</h2>

      {message && <p className="message">{message}</p>}

      <div className="form-group">
        <label>User:</label>
        <select
          value={selectedUserId}
          onChange={(e) => setSelectedUserId(e.target.value)}
          required
        >
          <option value="">Select a user</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name}
            </option>
          ))}
        </select>
      </div>

      <button className="submit-button" onClick={handleAddCard}>
        Add New Card
      </button>

      {cardId && (
        <div className="card-info">
          <h3>Card Information</h3>
          <p><strong>User Name:</strong> {users.find(user => user.id === selectedUserId)?.name}</p>
          <p><strong>Card ID:</strong> {cardId}</p>
        </div>
      )}
    </div>
  );
};

export default AddCard;
