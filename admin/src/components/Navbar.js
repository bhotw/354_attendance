import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isAttendanceDropdownOpen, setIsAttendanceDropdownOpen] = useState(false);
  const [isTeamDropdownOpen, setIsTeamDropdownOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const username = localStorage.getItem("username");


  if (!isAuthenticated) {
    return null;
  }

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/dashboard" className="navbar-logo">
          Dashboard
        </Link>
      </div>
      <div className="navbar-right">
        <div className="dropdown">
          <button onClick={() => setIsAttendanceDropdownOpen(!isAttendanceDropdownOpen)} className="dropdown-toggle">
            Attendance
          </button>
          {isAttendanceDropdownOpen && (
            <div className="dropdown-menu">
              <Link to="/view-attendance" className="dropdown-item">
                View Attendance
              </Link>
              <Link to="/attendanceperperson" className="dropdown-item">
                Per Person
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
              <Link to="/writetocard" className="dropdown-item">
                Write to Card
              </Link>
              <Link to="/readcard" className="dropdown-item">
                Read Card
              </Link>
              <Link to="/readusercard" className="dropdown-item">
                Read User Card
              </Link>
              <Link to="/addcard" className="dropdown-item">
                Add Card
              </Link>
            </div>
          )}
        </div>

        <div className="dropdown">
          <button onClick={() => setIsDropdownOpen(!isDropdownOpen)} className="dropdown-toggle">
          <span className="username">{username}</span>
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
      </div>
    </nav>
  );
};

export default Navbar;
