// src/components/Dashboard.js
import React from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css"; // Import the CSS file

const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <h1>Admin Dashboard</h1>
      <div className="dashboard-flex">
        <Link to="/register-team-member" className="dashboard-card">
          <h2>Register Team Member</h2>
          <p>Add new team members to the system.</p>
        </Link>
        <Link to="/add-admin-user" className="dashboard-card">
          <h2>Add Admin User</h2>
          <p>Create new admin users with access privileges.</p>
        </Link>
        <Link to="/add-attendance" className="dashboard-card">
          <h2>Add Attendance</h2>
          <p>Manually add attendance records for team members.</p>
        </Link>
        <Link to="/update-attendance" className="dashboard-card">
          <h2>Update Attendance</h2>
          <p>Edit or update existing attendance records.</p>
        </Link>
        <Link to="/view-attendance" className="dashboard-card">
          <h2>View Attendance</h2>
          <p>View all attendance records in a detailed sheet.</p>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;