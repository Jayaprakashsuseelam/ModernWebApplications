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
  salary: undefined,
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

  // Fetch employees
  const fetchEmployees = async () => {
    setLoading(true);
    setEmpError("");
    try {
      const res = await fetch(`${API_URL}/employees/`, {
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

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
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
              <button
                className="btn btn-success mb-3"
                onClick={fetchEmployees}
                disabled={loading}
              >
                {loading ? (
                  <span className="spinner-border spinner-border-sm me-2"></span>
                ) : null}
                Fetch Employees
              </button>
              <button
                className="btn btn-primary mb-3 ms-2"
                onClick={() => setShowEmpForm((v) => !v)}
              >
                {showEmpForm ? "Cancel" : "Add New Employee"}
              </button>
              {empFormError && <div className="alert alert-danger text-center">{empFormError}</div>}
              {empFormSuccess && <div className="alert alert-success text-center">{empFormSuccess}</div>}
              {showEmpForm && (
                <form onSubmit={handleEmpForm} className="mb-4 border rounded p-3 bg-light">
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
                      </tr>
                    ))}
                    {employees.length === 0 && !loading && (
                      <tr>
                        <td colSpan={6} className="text-center text-secondary">
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
