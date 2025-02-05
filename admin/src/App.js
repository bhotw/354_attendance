// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import RegisterTeamMember from "./components/RegisterTeamMember";
import AddAdminUser from "./components/AddAdminUser";
import AddAttendance from "./components/AddAttendance";
import ViewAttendance from "./components/ViewAttendance";
import ViewTeam from "./components/ViewTeam";
import Attendance from "./components/Attendance";
import ViewAdminUsers from "./components/ViewAdminUsers";
import WriteToCard from "./components/WriteToCard";
import ReadCard from "./components/ReadCard";
import ReadUserCard from "./components/ReadUserCard";
import AddCard from "./components/AddCard";




function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Attendance/>} />
        <Route path="/admin" element={<Login/>} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register-team-member" element={<RegisterTeamMember />} />
        <Route path="/add-admin-user" element={<AddAdminUser />} />
        <Route path="/view-admin-user" element={<ViewAdminUsers />} />
        <Route path="/add-attendance" element={<AddAttendance />} />
        <Route path="/viewteam" element={<ViewTeam />} />
        <Route path="/view-attendance" element={<ViewAttendance />} />
        <Route path="/writetocard" element={<WriteToCard />} />
        <Route path="/readcard" element={<ReadCard />} />
        <Route path="/readusercard" element={<ReadUserCard />} />
        <Route path="./addcard" element={<AddCard />} />

      </Routes>
    </Router>
  );
};

export default App;