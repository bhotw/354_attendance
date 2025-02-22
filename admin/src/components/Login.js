// src/components/Login.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import api from "../axiosInstance";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
        const response = await api.post("/api/auth/login", { username, password });

        if (response.data.status === "success"){
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("username", response.data.user.username);
            console.log(response.data);
            navigate("/dashboard");
        } else {
            setErrorMessage(response.data.message);
        }
    } catch (error) {
      console.error("Login error:", error);
      setErrorMessage("Incorrect Username or Password!");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Admin Login</h2>
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
        {errorMessage && <p className="error-message">{errorMessage}</p>} {/* Display error message */}
      </div>
    </div>
  );
};

export default Login;
