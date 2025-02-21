import React, { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import "./Dashboard.css";

const Dashboard = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };


  return (
      <div>
      <Navbar />
      <div className="dashboard-container">
        <div className="dashboard-flex">
           <Link to="/view-attendance" className="dashboard-card">
            <h2>View Attendance</h2>
            <p>View all attendance records in a detailed sheet.</p>
          </Link>

          <Link to="/viewteam" className="dashboard-card">
            <h2>View Team Members</h2>
            <p>View and manage all team members.</p>
          </Link>
          <Link to="/add-attendance" className="dashboard-card">
            <h2>Add Attendance</h2>
            <p>Manually add attendance records for team members.</p>
          </Link>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;
