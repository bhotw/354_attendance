// src/components/AddAttendance.js
import React, { useState } from "react";

const AddAttendance = () => {
  const [member, setMember] = useState("");
  const [signInTime, setSignInTime] = useState("");
  const [signOutTime, setSignOutTime] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add logic to save attendance (e.g., API call)
    console.log("Attendance Added:", { member, signInTime, signOutTime });
  };

  return (
    <div>
      <h2>Add Attendance</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Member Name"
          value={member}
          onChange={(e) => setMember(e.target.value)}
        />
        <input
          type="datetime-local"
          value={signInTime}
          onChange={(e) => setSignInTime(e.target.value)}
        />
        <input
          type="datetime-local"
          value={signOutTime}
          onChange={(e) => setSignOutTime(e.target.value)}
        />
        <button type="submit">Add Attendance</button>
      </form>
    </div>
  );
};

export default AddAttendance;