// src/components/RegisterTeamMember.js
import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import api from "../axiosInstance";
import { useNavigate, navigate } from "react-router-dom";
import "./RegisterTeamMember.css";

const RegisterTeamMember = () => {
  const navigate = useNavigate();


  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);


  const [formData, setFormData] = useState({
    name: "",
    role: "Student",
    email: "",
    phone_number: "",
    emergency_contact_name: "",
    emergency_contact_phone: "",
    parents_email: "",
  });

  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);


    const handleChange = (e) => {
      const { name, value } = e.target;


      if (name === "name" || name === "emergency_contact_name") {
        setFormData((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      } else {

        setFormData((prevData) => ({
          ...prevData,
          [name]: name.includes("phone") ? String(value) : value.trim(),
        }));
      }
    };



  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
       if (!token) {
        alert("No valid token found. Please log in again.");
        return;
      }
      setMessage("Please Tap a new card for the new member.")
      setIsLoading(true);

      const response = await api.post(
        "api/register_team_member",
        formData,
        {
          headers: {
           "Authorization": `Bearer ${token}`,
          },
        }
      );
      if (response.data.status === "success") {
        alert("Team member registered successfully!");
        navigate("/dashboard");
      } else if (response.data.status === "card"){
        alert(response.data.message);
      }
       else {
        alert(response.data.message);
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert(error.response.data.msg);
    }
  };

return (
    <div>
    <Navbar/>
  <div className="registration-container">
    <div className="registration-box">
      <h2>Register Team Member</h2>
      {message && <div className="message-box"><h3>{message}</h3></div>}
      <form onSubmit={handleSubmit}>
        {/* Name */}
        <div className="form-group">
          <label htmlFor="name">
            Name<span className="required">*</span>
          </label>
          <input
            type="text"
            id="name"
            name="name"
            placeholder="Enter full name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        {/* Role */}
        <div className="form-group">
          <label htmlFor="role">
            Role<span className="required">*</span>
          </label>
          <select
            id="role"
            name="role"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="">Select role</option>
            <option value="mentor">Mentor</option>
            <option value="student">Student</option>
          </select>
        </div>

        {/* Email */}
        <div className="form-group">
          <label htmlFor="email">
            Email<span className="required">*</span>
          </label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="Enter email address"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        {/* Phone Number */}
        <div className="form-group">
          <label htmlFor="phone_number">
            Phone Number<span className="required">*</span>
          </label>
          <input
            type="tel"
            id="phone_number"
            name="phone_number"
            placeholder="Enter phone number"
            value={formData.phone_number}
            onChange={handleChange}
            required
          />
        </div>

        {/* Emergency Contact Name */}
        <div className="form-group">
          <label htmlFor="emergency_contact_name">Emergency Contact Name<span className="required">*</span>
           </label>
          <input
            type="text"
            id="emergency_contact_name"
            name="emergency_contact_name"
            placeholder="Enter emergency contact's name"
            value={formData.emergency_contact_name}
            onChange={handleChange}
          />
        </div>

        {/* Emergency Contact Phone */}
        <div className="form-group">
          <label htmlFor="emergency_contact_phone">
            Emergency Contact Phone <span className="required">*</span>
          </label>
          <input
            type="tel"
            id="emergency_contact_phone"
            name="emergency_contact_phone"
            placeholder="Enter emergency contact's phone number"
            value={formData.emergency_contact_phone}
            onChange={handleChange}
          />
        </div>

        {/* Parents' Email */}
        <div className="form-group">
          <label htmlFor="parents_email">Parents Email <span className="required">*</span>
          </label>
          <input
            type="email"
            id="parents_email"
            name="parents_email"
            placeholder="Enter parents' email address"
            value={formData.parents_email}
            onChange={handleChange}
          />
        </div>

        <button type="submit" className="submit-button">
          Register
        </button>
      </form>
    </div>
  </div>
  </div>
);
};

export default RegisterTeamMember;