// routes/AdminRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AdminRoute = ({ children }) => {
  const { autenticado, rol } = useAuth();

  if (!autenticado || rol !== 'admin') {
    return <Navigate to="/login" />;
  }

  return children;
};

export default AdminRoute;