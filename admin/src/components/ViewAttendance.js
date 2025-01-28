// src/components/AttendanceList.js
import React, { useEffect, useState } from "react";
import axios from "axios";

const AttendanceList = () => {
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    // Fetch attendance data from the backend
    const fetchAttendance = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:5000/api/attendance", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setAttendance(response.data);
      } catch (error) {
        console.error("Error fetching attendance:", error);
      }
    };

    fetchAttendance();
  }, []);

  return (
    <div>
      <h1>Attendance List</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {attendance.map((record) => (
            <tr key={record.id}>
              <td>{record.id}</td>
              <td>{record.name}</td>
              <td>{record.date}</td>
              <td>{record.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AttendanceList;