import React, { useState, useEffect } from "react";
import { useNavigate, navigate } from "react-router-dom";
import api from "../axiosInstance";
import "../components/ViewAttendance.css";
import Navbar from "../components/Navbar";

const ViewAttendance = () => {
  const [attendance, setAttendance] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({ sign_in_time: "", sign_out_time: "" });
  const navigate = useNavigate();


  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login")
        }
        const response = await api.get("/api/view/view_attendance", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setAttendance(response.data);
      } catch (error) {
        console.error("Error fetching attendance records:", error);
      }
    };

    fetchAttendance();
  }, []);


  const handleEdit = (id, sign_in_time, sign_out_time) => {
    setEditingId(id);
    setEditData({ sign_in_time, sign_out_time });
  };


  const handleInputChange = (e) => {
    setEditData({ ...editData, [e.target.name]: e.target.value });
  };


  const handleSave = async (id) => {
    try {
      const token = localStorage.getItem("token"); // Get token from localStorage
      await api.put(`/api/view/view_attendance/${id}`, editData, {
        headers: {
          Authorization: `Bearer ${token}`, // Pass the token in the headers
        },
      });
      setAttendance((prev) =>
        prev.map((record) =>
          record.id === id ? { ...record, ...editData } : record
        )
      );
      setEditingId(null);
    } catch (error) {
      console.error("Error updating attendance record:", error);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="view-attendance-container">
        <h1>View Attendance</h1>
        <table className="attendance-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Date</th>
              <th>Sign In Time</th>
              <th>Sign Out Time</th>
              <th>Days Hours</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {attendance.map((record) => (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td>{record.user_name}</td>
                <td>{record.date}</td>
                <td>
                  {editingId === record.id ? (
                    <input
                      type="time"
                      name="sign_in_time"
                      value={editData.sign_in_time}
                      onChange={handleInputChange}
                    />
                  ) : (
                    record.sign_in_time || "—"
                  )}
                </td>
                <td>
                  {editingId === record.id ? (
                    <input
                      type="time"
                      name="sign_out_time"
                      value={editData.sign_out_time}
                      onChange={handleInputChange}
                    />
                  ) : (
                    record.sign_out_time || "—"
                  )}
                </td>
                <td>{record.days_hours}</td>
                <td>
                  {editingId === record.id ? (
                    <button className="save-btn" onClick={() => handleSave(record.id)}>Save</button>
                  ) : (
                    <button className="edit-btn" onClick={() => handleEdit(record.id, record.sign_in_time, record.sign_out_time)}>Edit</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ViewAttendance;
