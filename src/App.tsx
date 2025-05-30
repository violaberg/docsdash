import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from './store';
import LoginForm from './components/auth/LoginForm';
import Navbar from './components/layout/Navbar';
import Dashboard from './components/dashboard/Dashboard';
import PatientDetails from './components/patients/PatientDetails';

const App = () => {
  const { isDark } = useSelector((state: RootState) => state.theme);
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  return (
    <div className={isDark ? 'dark' : ''}>
      <Router>
        {isAuthenticated && <Navbar />}
        <Routes>
          <Route
            path="/login"
            element={
              !isAuthenticated ? <LoginForm /> : <Navigate to="/dashboard" />
            }
          />
          <Route
            path="/dashboard"
            element={
              isAuthenticated ? <Dashboard /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/patients/:id"
            element={
              isAuthenticated ? <PatientDetails /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/"
            element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
            }
          />
        </Routes>
      </Router>
    </div>
  );
};

export default App;