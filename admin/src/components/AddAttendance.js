//components/AddAttendance.js
import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import { useNavigate, navigate } from "react-router-dom";
import api from "../axiosInstance";
import './AddAdminUser.css';


const AddAttendance = () => {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState("");
  const [date, setDate] = useState("");
  const [signInTime, setSignInTime] = useState("");
  const [signOutTime, setSignOutTime] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate()

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("token");
        if(!token){
            navigate("/login");
        }
        const response = await api.get("/api/manual/users", {
        headers: {
          Authorization: `Bearer ${token}`,
        }
        });
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
  e.preventDefault();
  setMessage("");

  const attendanceData = {
    user_id: selectedUserId,
    date,
    sign_in_time: signInTime,
    sign_out_time: signOutTime,
  };

  try {
    const token = localStorage.getItem("token");
    const response = await api.post(
      "/api/manual/add_attendance",
      attendanceData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    setMessage("✅ Attendance record added successfully!");
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      setMessage(error.response.data.message);
    } else {
      setMessage("❌ Failed to add attendance.");
    }
    console.error("Error submitting attendance:", error);
  }
};

  return (
  <div>
  <Navbar/>
    <div className="add-attendance-container">
      <h2>Add Attendance</h2>
      {message && <p className="message">{message}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>User:</label>
          <select value={selectedUserId} onChange={(e) => setSelectedUserId(e.target.value)} required>
            <option value="">Select a user</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Date:</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        </div>

        <div className="form-group">
          <label>Sign In Time:</label>
          <input type="time" value={signInTime} onChange={(e) => setSignInTime(e.target.value)} />
        </div>

        <div className="form-group">
          <label>Sign Out Time:</label>
          <input type="time" value={signOutTime} onChange={(e) => setSignOutTime(e.target.value)} />
        </div>

        <button className="submit-button" type="submit">Submit</button>
      </form>
    </div>
    </div>
  );
};

export default AddAttendance;