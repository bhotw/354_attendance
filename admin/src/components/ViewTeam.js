import React, { useEffect, useState } from "react";
import { useNavigate, navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../axiosInstance";
import "./ViewTeam.css";

const ViewTeam = () => {
  const [teamMembers, setTeamMembers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetchTeamMembers();
  }, []);

  const fetchTeamMembers = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        }
      const response = await api.get("/api/team/viewteam", {
        headers: { "Authorization": `Bearer ${token}` },
      });
      setTeamMembers(response.data.team_members);
    } catch (error) {
      console.error("Error fetching team members:", error);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user.id);
    setFormData(user);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    try {
      const token = localStorage.getItem("token");
      await api.put(`/api/team/viewteam/${editingUser}`, formData, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setEditingUser(null);
      fetchTeamMembers(); // Refresh data
    } catch (error) {
      console.error("Error updating user:", error);
    }
  };

  return (
  <div>
  <Navbar />
    <div className="view-team-container">
      <h1>Team Members</h1>
      <table className="team-table">
        <thead>
          <tr>
            <th>ID Card</th>
            <th>Name</th>
            <th>Role</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Emergency Contact</th>
            <th>Parents' Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {teamMembers.map((user) => (
            <tr key={user.id}>
              {editingUser === user.id ? (
                <>
                  <td>
                    <input
                      type="text"
                      name="card_id"
                      value={formData.card_id}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      name="role"
                      value={formData.role}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      name="phone_number"
                      value={formData.phone_number}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      name="emergency_contact_name"
                      value={formData.emergency_contact_name}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <input
                      type="email"
                      name="parents_email"
                      value={formData.parents_email}
                      onChange={handleChange}
                    />
                  </td>
                  <td>
                    <button className="save-btn" onClick={handleSave}>
                      Save
                    </button>
                  </td>
                </>
              ) : (
                <>
                  <td>{user.card_id}</td>
                  <td>{user.name}</td>
                  <td>{user.role}</td>
                  <td>{user.email}</td>
                  <td>{user.phone_number}</td>
                  <td>{user.emergency_contact_name}</td>
                  <td>{user.parents_email}</td>
                  <td>
                    <button className="edit-btn" onClick={() => handleEdit(user)}>
                      Edit
                    </button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </div>
  );
};

export default ViewTeam;
