// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import RegisterTeamMember from "./components/RegisterTeamMember";
import AddAdminUser from "./components/AddAdminUser";
import AddAttendance from "./components/AddAttendance";
import UpdateAttendance from "./components/UpdateAttendance";
import ViewAttendance from "./components/ViewAttendance";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register-team-member" element={<RegisterTeamMember />} />
        <Route path="/add-admin-user" element={<AddAdminUser />} />
        <Route path="/add-attendance" element={<AddAttendance />} />
        <Route path="/update-attendance" element={<UpdateAttendance />} />
        <Route path="/view-attendance" element={<ViewAttendance />} />
      </Routes>
    </Router>
  );
};

export default App;