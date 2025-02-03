// src/components/Navbar.js
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isAttendanceDropdownOpen, setIsAttendanceDropdownOpen] = useState(false);
  const [isTeamDropdownOpen, setIsTeamDropdownOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };
    const username = localStorage.getItem("username");
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/dashboard" className="navbar-logo">
          Dashboard
        </Link>
      </div>
      <div className="navbar-right">
        <span className="username">{username}</span>
        <div className="dropdown">
          <button onClick={() => setIsDropdownOpen(!isDropdownOpen)} className="dropdown-toggle">
            ▼
          </button>
          {isDropdownOpen && (
            <div className="dropdown-menu">
              <Link to="/view-admin-user" className="dropdown-item">
                View Admin Users
              </Link>
              <Link to="/add-admin-user" className="dropdown-item">
                Add Admin User
              </Link>
              <button onClick={handleLogout} className="dropdown-item">
                Log Out
              </button>
            </div>
          )}
        </div>

        <div className="dropdown">
          <button onClick={() => setIsAttendanceDropdownOpen(!isAttendanceDropdownOpen)} className="dropdown-toggle">
            Attendance
          </button>
          {isAttendanceDropdownOpen && (
            <div className="dropdown-menu">
              <Link to="/view-attendance" className="dropdown-item">
                View Attendance
              </Link>
              <Link to="/add-attendance" className="dropdown-item">
                Add Attendance
              </Link>
            </div>
          )}
        </div>

        <div className="dropdown">
          <button onClick={() => setIsTeamDropdownOpen(!isTeamDropdownOpen)} className="dropdown-toggle">
            Team
          </button>
          {isTeamDropdownOpen && (
            <div className="dropdown-menu">
              <Link to="/viewteam" className="dropdown-item">
                View Team Members
              </Link>
              <Link to="/register-team-member" className="dropdown-item">
                Register Team Member
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
