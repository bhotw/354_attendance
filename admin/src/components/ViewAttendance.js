import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axiosInstance";
import "../components/ViewAttendance.css";
import Navbar from "../components/Navbar";

const ViewAttendance = () => {
  const [attendance, setAttendance] = useState([]);
  const [filteredAttendance, setFilteredAttendance] = useState([]);
  const [filter, setFilter] = useState("all"); // "today", "this_week", "all"
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({ sign_in_time: "", sign_out_time: "" });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
        }
        const response = await api.get("/api/view/view_attendance", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Parse and sort attendance data
        const sortedData = response.data.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          if (dateA > dateB) return -1;
          if (dateA < dateB) return 1;
          return a.sign_in_time.localeCompare(b.sign_in_time); // Sort by sign-in time if dates are the same
        });

        setAttendance(sortedData);
        filterAttendance(sortedData, filter);
      } catch (error) {
        console.error("Error fetching attendance records:", error);
      }
    };

    fetchAttendance();
  }, []);

  useEffect(() => {
    filterAttendance(attendance, filter);
  }, [filter, attendance]);

  const filterAttendance = (data, criteria) => {
      const today = new Date();
      const todayStr = today.getFullYear() + "-" + String(recordDate.getMonth() + 1).padStart(2, "0") + "-" + String(recordDate.getDate()).padStart(2, "0")
      console.log("today: ", todayStr);

      const startOfWeek = new Date();
      startOfWeek.setDate(today.getDate() - today.getDay()); // Get Sunday of the current week

      let filteredData = data;

      if (criteria === "today") {
        filteredData = data.filter((record) => {
          const recordDate = new Date(record.date);
          console.log("recordDate: ", recordDate);
          const recordStr = recordDate.toISOString().split("T")[0];
          console.log("recordStr: ", recordStr);
          return recordStr === todayStr;
        });
      } else if (criteria === "this_week") {
        filteredData = data.filter((record) => new Date(record.date) >= startOfWeek);
      }

      setFilteredAttendance(filteredData);
    };

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

  return (
    <div>
      <Navbar />
      <div className="view-attendance-container">
        <h1>View Attendance</h1>

        {/* Filter dropdown */}
        <div className="filter-container">
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All</option>
            <option value="today">Today</option>
            <option value="this_week">This Week</option>
          </select>
        </div>

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
            {filteredAttendance.map((record) => (
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
