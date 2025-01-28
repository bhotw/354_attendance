// src/components/AddAdminUser.js
import React, { useState } from "react";

const AddAdminUser = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add logic to add admin user (e.g., API call)
    console.log("Admin User Added:", { username, password });
  };

  return (
    <div>
      <h2>Add Admin User</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Add Admin User</button>
      </form>
    </div>
  );
};

export default AddAdminUser;