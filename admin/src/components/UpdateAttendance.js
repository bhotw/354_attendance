// src/components/UpdateAttendance.js
import React, { useState } from "react";

const UpdateAttendance = () => {
  const [id, setId] = useState("");
  const [signInTime, setSignInTime] = useState("");
  const [signOutTime, setSignOutTime] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add logic to update attendance (e.g., API call)
    console.log("Attendance Updated:", { id, signInTime, signOutTime });
  };

  return (
    <div>
      <h2>Update Attendance</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Attendance ID"
          value={id}
          onChange={(e) => setId(e.target.value)}
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
        <button type="submit">Update Attendance</button>
      </form>
    </div>
  );
};

export default UpdateAttendance;