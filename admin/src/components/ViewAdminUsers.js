import React, { useState, useEffect } from "react";
import { useNavigate, navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../axiosInstance";
import "./ViewAdminUsers.css";

const ViewAdminUsers = () => {
  const [adminUsers, setAdminUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate()

  useEffect(() => {
    const fetchAdminUsers = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login");
        }
        const response = await api.get("api/admin/view_admin_users", {
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
