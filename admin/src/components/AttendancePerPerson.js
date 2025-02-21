import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axiosInstance";
import "../components/AttendancePerPerson.css";
import Navbar from "../components/Navbar";
import "font-awesome/css/font-awesome.min.css"; // Import FontAwesome icons

const AttendancePerPerson = () => {
  const [users, setUsers] = useState([]); // List of users
  const [selectedUser, setSelectedUser] = useState(""); // Selected user ID
  const [attendance, setAttendance] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({ sign_in_time: "", sign_out_time: "" });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }
        const response = await api.get("/api/manual/users", {
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

  useEffect(() => {
    if (!selectedUser) return;

    const fetchAttendance = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }
        const response = await api.get(`/api/view/user_attendance/${selectedUser}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const sortedData = response.data.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          if (dateA > dateB) return -1;
          if (dateA < dateB) return 1;
          return a.sign_in_time.localeCompare(b.sign_in_time); // Sort by sign-in time if dates are the same
        });
        setAttendance(sortedData);
      } catch (error) {
        console.error("Error fetching attendance records:", error);
      }
    };

    fetchAttendance();
  }, [selectedUser, navigate]);

  const handleEdit = (id, sign_in_time, sign_out_time) => {
    setEditingId(id);
    setEditData({ sign_in_time, sign_out_time });
  };

  const handleInputChange = (e) => {
    setEditData({ ...editData, [e.target.name]: e.target.value });
  };

  const handleSave = async (id) => {
    try {
      const token = localStorage.getItem("token");
      await api.put(`/api/view/view_attendance/${id}`, editData, {
        headers: {
          Authorization: `Bearer ${token}`,
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

  const handleDelete = async (id) => {
    const isConfirmed = window.confirm("Are you sure you want to delete this attendance record?");
    if (!isConfirmed) return;

    try {
      const token = localStorage.getItem("token");
      const response = await api.delete(`/api/view/view_attendance/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.status === 200) {
        setAttendance(attendance.filter((record) => record.id !== id));
        alert("Attendance record deleted successfully.");
      }
    } catch (error) {
      console.error("Error deleting attendance record:", error);
      alert("Error deleting attendance record.");
    }
  };

  return (
    <div>
      <Navbar />
      <div className="attendance-per-person-container">
        <h1>
          Attendance for
          <select
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            className="user-select"
          >
            <option value="">-- Select User --</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </h1>

        {selectedUser && (
          <table className="attendance-table">
            <thead>
              <tr>
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
                      <button className="save-btn" onClick={() => handleSave(record.id)}>
                        Save
                      </button>
                    ) : (
                      <div className="button-wrapper">
                        <button
                          className="edit-btn"
                          onClick={() => handleEdit(record.id, record.sign_in_time, record.sign_out_time)}
                        >
                          <i className="fa fa-pencil"></i> 
                        </button>
                        <button className="delete-btn" onClick={() => handleDelete(record.id)}>
                          <i className="fa fa-trash"></i> 
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default AttendancePerPerson;
