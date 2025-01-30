import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import axios from "axios";
import "./ViewAdminUsers.css";  // Create a separate CSS file for styling

const ViewAdminUsers = () => {
  const [adminUsers, setAdminUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAdminUsers = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          alert("No valid token found. Please log in.");
          return;
        }

        const response = await axios.get("http://localhost:5000/api/admin/view_admin_users", {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });

        if (response.data.status === "success") {
          setAdminUsers(response.data.admin_users);
        } else {
          alert("Failed to load admin users.");
        }
      } catch (error) {
        console.error("Error fetching admin users:", error);
        alert("Error fetching admin users.");
      } finally {
        setLoading(false);
      }
    };

    fetchAdminUsers();
  }, []);

  return (
    <div>
      <Navbar />
      <div className="view-admin-users-container">
        <h2>Admin Users</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="admin-users-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {adminUsers.length > 0 ? (
                adminUsers.map((admin) => (
                  <tr key={admin.id}>
                    <td>{admin.username}</td>
                    <td>{admin.email}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="2">No admin users found</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default ViewAdminUsers;
