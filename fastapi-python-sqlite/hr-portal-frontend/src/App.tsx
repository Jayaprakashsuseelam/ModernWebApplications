import React, { useState } from "react";

interface Employee {
  id: number;
  employee_id: string;
  first_name: string;
  last_name: string;
  email: string;
  department: string;
  position: string;
  hire_date: string;
  salary?: number;
  phone?: string;
  address?: string;
  emergency_contact?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

const API_URL = "http://localhost:8000";

const initialEmployee = {
  employee_id: "",
  first_name: "",
  last_name: "",
  email: "",
  department: "",
  position: "",
  hire_date: "",
  salary: undefined as number | undefined,
  phone: "",
  address: "",
  emergency_contact: "",
};

function App() {
  // Auth state
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [loginError, setLoginError] = useState("");
  const [showRegister, setShowRegister] = useState(false);
  const [registerData, setRegisterData] = useState({
    email: "",
    username: "",
    password: "",
    full_name: "",
  });
  const [registerError, setRegisterError] = useState("");
  const [registerSuccess, setRegisterSuccess] = useState("");

  // Employee state
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(false);
  const [empError, setEmpError] = useState("");

  // New employee form state
  const [showEmpForm, setShowEmpForm] = useState(false);
  const [empForm, setEmpForm] = useState({ ...initialEmployee });
  const [empFormError, setEmpFormError] = useState("");
  const [empFormSuccess, setEmpFormSuccess] = useState("");

  // Edit employee state
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [editForm, setEditForm] = useState({ ...initialEmployee });
  const [editFormError, setEditFormError] = useState("");
  const [editFormSuccess, setEditFormSuccess] = useState("");

  // View employee state
  const [viewingEmployee, setViewingEmployee] = useState<Employee | null>(null);

  // Filter state
  const [filters, setFilters] = useState({
    department: "",
    is_active: "",
  });

  // Login handler
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError("");
    try {
      const res = await fetch(`${API_URL}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      });
      if (!res.ok) {
        setLoginError("Invalid credentials");
        return;
      }
      const data = await res.json();
      setToken(data.access_token);
    } catch (err) {
      setLoginError("Login failed");
    }
  };

  // Registration handler
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegisterError("");
    setRegisterSuccess("");
    try {
      const res = await fetch(`${API_URL}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...registerData,
          is_admin: false,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        setRegisterError(data.detail || "Registration failed");
        return;
      }
      setRegisterSuccess("Registration successful! You can now log in.");
      setShowRegister(false);
      setRegisterData({ email: "", username: "", password: "", full_name: "" });
    } catch (err) {
      setRegisterError("Registration failed");
    }
  };

  // Fetch employees with filters
  const fetchEmployees = async () => {
    setLoading(true);
    setEmpError("");
    try {
      const params = new URLSearchParams();
      if (filters.department) params.append("department", filters.department);
      if (filters.is_active !== "") params.append("is_active", filters.is_active);
      
      const res = await fetch(`${API_URL}/employees/?${params}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        setEmpError("Failed to fetch employees");
        setEmployees([]);
        setLoading(false);
        return;
      }
      const data = await res.json();
      setEmployees(data);
    } catch (err) {
      setEmpError("Error fetching employees");
    }
    setLoading(false);
  };

  // Create employee handler
  const handleEmpForm = async (e: React.FormEvent) => {
    e.preventDefault();
    setEmpFormError("");
    setEmpFormSuccess("");
    try {
      const res = await fetch(`${API_URL}/employees/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...empForm,
          salary: empForm.salary ? Number(empForm.salary) : undefined,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        setEmpFormError(data.detail || "Failed to create employee");
        return;
      }
      setEmpFormSuccess("Employee created successfully!");
      setEmpForm({ ...initialEmployee });
      setShowEmpForm(false);
      fetchEmployees();
    } catch (err) {
      setEmpFormError("Failed to create employee");
    }
  };

  // View employee handler
  const handleViewEmployee = async (employeeId: string) => {
    try {
      const res = await fetch(`${API_URL}/employees/${employeeId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        setEmpError("Failed to fetch employee details");
        return;
      }
      const data = await res.json();
      setViewingEmployee(data);
    } catch (err) {
      setEmpError("Error fetching employee details");
    }
  };

  // Edit employee handler
  const handleEditEmployee = (employee: Employee) => {
    setEditingEmployee(employee);
    setEditForm({
      employee_id: employee.employee_id,
      first_name: employee.first_name,
      last_name: employee.last_name,
      email: employee.email,
      department: employee.department,
      position: employee.position,
      hire_date: employee.hire_date.split('T')[0], // Convert to date input format
      salary: employee.salary,
      phone: employee.phone || "",
      address: employee.address || "",
      emergency_contact: employee.emergency_contact || "",
    });
  };

  // Update employee handler
  const handleUpdateEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    setEditFormError("");
    setEditFormSuccess("");
    if (!editingEmployee) return;

    try {
      const res = await fetch(`${API_URL}/employees/${editingEmployee.employee_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...editForm,
          salary: editForm.salary ? Number(editForm.salary) : undefined,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        setEditFormError(data.detail || "Failed to update employee");
        return;
      }
      setEditFormSuccess("Employee updated successfully!");
      setEditingEmployee(null);
      setEditForm({ ...initialEmployee });
      fetchEmployees();
    } catch (err) {
      setEditFormError("Failed to update employee");
    }
  };

  // Delete employee handler
  const handleDeleteEmployee = async (employeeId: string) => {
    if (!confirm("Are you sure you want to delete this employee?")) return;
    
    try {
      const res = await fetch(`${API_URL}/employees/${employeeId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        const data = await res.json();
        setEmpError(data.detail || "Failed to delete employee");
        return;
      }
      setEmpError("");
      fetchEmployees();
    } catch (err) {
      setEmpError("Failed to delete employee");
    }
  };

  // Activate/Deactivate employee handlers
  const handleActivateEmployee = async (employeeId: string) => {
    try {
      const res = await fetch(`${API_URL}/employees/${employeeId}/activate`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        setEmpError("Failed to activate employee");
        return;
      }
      setEmpError("");
      fetchEmployees();
    } catch (err) {
      setEmpError("Failed to activate employee");
    }
  };

  const handleDeactivateEmployee = async (employeeId: string) => {
    try {
      const res = await fetch(`${API_URL}/employees/${employeeId}/deactivate`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        setEmpError("Failed to deactivate employee");
        return;
      }
      setEmpError("");
      fetchEmployees();
    } catch (err) {
      setEmpError("Failed to deactivate employee");
    }
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-10 col-lg-8">
          <div className="text-center mb-4">
            <h1 className="display-4 fw-bold">HR Portal Demo</h1>
            <p className="lead text-secondary">FastAPI + React + Bootstrap</p>
          </div>
          {!token ? (
            showRegister ? (
              <form onSubmit={handleRegister} className="card p-4 shadow-sm">
                <h2 className="h4 mb-3 text-center">Register</h2>
                {registerError && <div className="alert alert-danger text-center">{registerError}</div>}
                {registerSuccess && <div className="alert alert-success text-center">{registerSuccess}</div>}
                <div className="mb-3">
                  <label className="form-label">Full Name</label>
                  <input
                    className="form-control"
                    type="text"
                    value={registerData.full_name}
                    onChange={e => setRegisterData({ ...registerData, full_name: e.target.value })}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    className="form-control"
                    type="email"
                    value={registerData.email}
                    onChange={e => setRegisterData({ ...registerData, email: e.target.value })}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    className="form-control"
                    type="text"
                    value={registerData.username}
                    onChange={e => setRegisterData({ ...registerData, username: e.target.value })}
                    required
                  />
                </div>
                <div className="mb-4">
                  <label className="form-label">Password</label>
                  <input
                    className="form-control"
                    type="password"
                    value={registerData.password}
                    onChange={e => setRegisterData({ ...registerData, password: e.target.value })}
                    required
                  />
                </div>
                <button className="btn btn-success w-100 mb-2" type="submit">
                  Register
                </button>
                <button type="button" className="btn btn-link w-100" onClick={() => { setShowRegister(false); setRegisterError(""); }}>
                  Already have an account? Login
                </button>
              </form>
            ) : (
              <form onSubmit={handleLogin} className="card p-4 shadow-sm">
                <h2 className="h4 mb-3 text-center">Sign In</h2>
                {loginError && <div className="alert alert-danger text-center">{loginError}</div>}
                {registerSuccess && <div className="alert alert-success text-center">{registerSuccess}</div>}
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    className="form-control"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoFocus
                  />
                </div>
                <div className="mb-4">
                  <label className="form-label">Password</label>
                  <input
                    className="form-control"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <button className="btn btn-primary w-100 mb-2" type="submit">
                  Login
                </button>
                <button type="button" className="btn btn-link w-100" onClick={() => { setShowRegister(true); setRegisterSuccess(""); setLoginError(""); }}>
                  New user? Register here
                </button>
              </form>
            )
          ) : (
            <div className="card p-4 shadow-sm">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h2 className="h4 mb-0">Employees</h2>
                <button className="btn btn-outline-secondary btn-sm" onClick={() => setToken(null)}>
                  Logout
                </button>
              </div>

              {/* Filters */}
              <div className="row g-2 mb-3">
                <div className="col-md-4">
                  <label className="form-label">Department</label>
                  <input
                    className="form-control"
                    type="text"
                    value={filters.department}
                    onChange={e => setFilters({ ...filters, department: e.target.value })}
                    placeholder="Filter by department"
                  />
                </div>
                <div className="col-md-4">
                  <label className="form-label">Status</label>
                  <select
                    className="form-select"
                    value={filters.is_active}
                    onChange={e => setFilters({ ...filters, is_active: e.target.value })}
                  >
                    <option value="">All</option>
                    <option value="true">Active</option>
                    <option value="false">Inactive</option>
                  </select>
                </div>
                <div className="col-md-4 d-flex align-items-end">
                  <button
                    className="btn btn-primary w-100"
                    onClick={fetchEmployees}
                    disabled={loading}
                  >
                    {loading ? (
                      <span className="spinner-border spinner-border-sm me-2"></span>
                    ) : null}
                    Apply Filters
                  </button>
                </div>
              </div>

              <button
                className="btn btn-primary mb-3 me-2"
                onClick={() => setShowEmpForm((v) => !v)}
              >
                {showEmpForm ? "Cancel" : "Add New Employee"}
              </button>

              {empFormError && <div className="alert alert-danger text-center">{empFormError}</div>}
              {empFormSuccess && <div className="alert alert-success text-center">{empFormSuccess}</div>}
              {editFormError && <div className="alert alert-danger text-center">{editFormError}</div>}
              {editFormSuccess && <div className="alert alert-success text-center">{editFormSuccess}</div>}

              {/* New Employee Form */}
              {showEmpForm && (
                <form onSubmit={handleEmpForm} className="mb-4 border rounded p-3 bg-light">
                  <h5>Add New Employee</h5>
                  <div className="row g-2">
                    <div className="col-md-6">
                      <label className="form-label">Employee ID</label>
                      <input className="form-control" type="text" value={empForm.employee_id} onChange={e => setEmpForm({ ...empForm, employee_id: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">First Name</label>
                      <input className="form-control" type="text" value={empForm.first_name} onChange={e => setEmpForm({ ...empForm, first_name: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Last Name</label>
                      <input className="form-control" type="text" value={empForm.last_name} onChange={e => setEmpForm({ ...empForm, last_name: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Email</label>
                      <input className="form-control" type="email" value={empForm.email} onChange={e => setEmpForm({ ...empForm, email: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Department</label>
                      <input className="form-control" type="text" value={empForm.department} onChange={e => setEmpForm({ ...empForm, department: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Position</label>
                      <input className="form-control" type="text" value={empForm.position} onChange={e => setEmpForm({ ...empForm, position: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Hire Date</label>
                      <input className="form-control" type="date" value={empForm.hire_date} onChange={e => setEmpForm({ ...empForm, hire_date: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Salary</label>
                      <input className="form-control" type="number" value={empForm.salary !== undefined ? String(empForm.salary) : ""} onChange={e => setEmpForm({ ...empForm, salary: e.target.value ? Number(e.target.value) : undefined })} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Phone</label>
                      <input className="form-control" type="text" value={empForm.phone} onChange={e => setEmpForm({ ...empForm, phone: e.target.value })} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Address</label>
                      <input className="form-control" type="text" value={empForm.address} onChange={e => setEmpForm({ ...empForm, address: e.target.value })} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Emergency Contact</label>
                      <input className="form-control" type="text" value={empForm.emergency_contact} onChange={e => setEmpForm({ ...empForm, emergency_contact: e.target.value })} />
                    </div>
                  </div>
                  <button className="btn btn-success mt-3 w-100" type="submit">Create Employee</button>
                </form>
              )}

              {/* Edit Employee Form */}
              {editingEmployee && (
                <form onSubmit={handleUpdateEmployee} className="mb-4 border rounded p-3 bg-light">
                  <h5>Edit Employee: {editingEmployee.first_name} {editingEmployee.last_name}</h5>
                  <div className="row g-2">
                    <div className="col-md-6">
                      <label className="form-label">Employee ID</label>
                      <input className="form-control" type="text" value={editForm.employee_id} onChange={e => setEditForm({ ...editForm, employee_id: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">First Name</label>
                      <input className="form-control" type="text" value={editForm.first_name} onChange={e => setEditForm({ ...editForm, first_name: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Last Name</label>
                      <input className="form-control" type="text" value={editForm.last_name} onChange={e => setEditForm({ ...editForm, last_name: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Email</label>
                      <input className="form-control" type="email" value={editForm.email} onChange={e => setEditForm({ ...editForm, email: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Department</label>
                      <input className="form-control" type="text" value={editForm.department} onChange={e => setEditForm({ ...editForm, department: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Position</label>
                      <input className="form-control" type="text" value={editForm.position} onChange={e => setEditForm({ ...editForm, position: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Hire Date</label>
                      <input className="form-control" type="date" value={editForm.hire_date} onChange={e => setEditForm({ ...editForm, hire_date: e.target.value })} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Salary</label>
                      <input className="form-control" type="number" value={editForm.salary !== undefined ? String(editForm.salary) : ""} onChange={e => setEditForm({ ...editForm, salary: e.target.value ? Number(e.target.value) : undefined })} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Phone</label>
                      <input className="form-control" type="text" value={editForm.phone} onChange={e => setEditForm({ ...editForm, phone: e.target.value })} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Address</label>
                      <input className="form-control" type="text" value={editForm.address} onChange={e => setEditForm({ ...editForm, address: e.target.value })} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label">Emergency Contact</label>
                      <input className="form-control" type="text" value={editForm.emergency_contact} onChange={e => setEditForm({ ...editForm, emergency_contact: e.target.value })} />
                    </div>
                  </div>
                  <div className="mt-3">
                    <button className="btn btn-success me-2" type="submit">Update Employee</button>
                    <button className="btn btn-secondary" type="button" onClick={() => { setEditingEmployee(null); setEditForm({ ...initialEmployee }); }}>
                      Cancel
                    </button>
                  </div>
                </form>
              )}

              {/* View Employee Modal */}
              {viewingEmployee && (
                <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
                  <div className="modal-dialog modal-lg">
                    <div className="modal-content">
                      <div className="modal-header">
                        <h5 className="modal-title">Employee Details</h5>
                        <button type="button" className="btn-close" onClick={() => setViewingEmployee(null)}></button>
                      </div>
                      <div className="modal-body">
                        <div className="row">
                          <div className="col-md-6">
                            <p><strong>Employee ID:</strong> {viewingEmployee.employee_id}</p>
                            <p><strong>Name:</strong> {viewingEmployee.first_name} {viewingEmployee.last_name}</p>
                            <p><strong>Email:</strong> {viewingEmployee.email}</p>
                            <p><strong>Department:</strong> {viewingEmployee.department}</p>
                            <p><strong>Position:</strong> {viewingEmployee.position}</p>
                            <p><strong>Hire Date:</strong> {new Date(viewingEmployee.hire_date).toLocaleDateString()}</p>
                          </div>
                          <div className="col-md-6">
                            <p><strong>Salary:</strong> {viewingEmployee.salary ? `$${viewingEmployee.salary.toLocaleString()}` : 'Not specified'}</p>
                            <p><strong>Phone:</strong> {viewingEmployee.phone || 'Not specified'}</p>
                            <p><strong>Address:</strong> {viewingEmployee.address || 'Not specified'}</p>
                            <p><strong>Emergency Contact:</strong> {viewingEmployee.emergency_contact || 'Not specified'}</p>
                            <p><strong>Status:</strong> 
                              {viewingEmployee.is_active ? (
                                <span className="badge bg-success ms-2">Active</span>
                              ) : (
                                <span className="badge bg-danger ms-2">Inactive</span>
                              )}
                            </p>
                            <p><strong>Created:</strong> {new Date(viewingEmployee.created_at).toLocaleString()}</p>
                            {viewingEmployee.updated_at && (
                              <p><strong>Last Updated:</strong> {new Date(viewingEmployee.updated_at).toLocaleString()}</p>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" onClick={() => setViewingEmployee(null)}>Close</button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {empError && <div className="alert alert-danger text-center">{empError}</div>}
              <div className="table-responsive">
                <table className="table table-bordered table-hover align-middle">
                  <thead className="table-light">
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Department</th>
                      <th>Position</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {employees.map((emp) => (
                      <tr key={emp.id}>
                        <td>{emp.employee_id}</td>
                        <td>{emp.first_name} {emp.last_name}</td>
                        <td>{emp.email}</td>
                        <td>{emp.department}</td>
                        <td>{emp.position}</td>
                        <td>
                          {emp.is_active ? (
                            <span className="badge bg-success">Active</span>
                          ) : (
                            <span className="badge bg-danger">Inactive</span>
                          )}
                        </td>
                        <td>
                          <div className="btn-group btn-group-sm" role="group">
                            <button 
                              className="btn btn-outline-info" 
                              onClick={() => handleViewEmployee(emp.employee_id)}
                              title="View Details"
                            >
                              👁️
                            </button>
                            <button 
                              className="btn btn-outline-warning" 
                              onClick={() => handleEditEmployee(emp)}
                              title="Edit"
                            >
                              ✏️
                            </button>
                            {emp.is_active ? (
                              <button 
                                className="btn btn-outline-secondary" 
                                onClick={() => handleDeactivateEmployee(emp.employee_id)}
                                title="Deactivate"
                              >
                                ⏸️
                              </button>
                            ) : (
                              <button 
                                className="btn btn-outline-success" 
                                onClick={() => handleActivateEmployee(emp.employee_id)}
                                title="Activate"
                              >
                                ▶️
                              </button>
                            )}
                            <button 
                              className="btn btn-outline-danger" 
                              onClick={() => handleDeleteEmployee(emp.employee_id)}
                              title="Delete"
                            >
                              🗑️
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {employees.length === 0 && !loading && (
                      <tr>
                        <td colSpan={7} className="text-center text-secondary">
                          No employees to display
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
