// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProductoForm from './components/ProductoForm';
import EditarProducto from './pages/EditarProducto';
import Login from './pages/Login';
import { AuthProvider, useAuth } from './context/AuthContext';
import AdminRoute from './routes/AdminRoute';
import Catalogo from './pages/Catalogo';
import { CartProvider } from './context/CartContext';
import Carrito from './pages/Carrito';
import AdminPanel from './pages/AdminPanel';
import Header from './components/Header';
import Footer from './components/Footer';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// 🧠 Componente de bienvenida
function Bienvenida() {
  const { autenticado, rol } = useAuth();

  if (!autenticado) return null;

  return (
    <p style={{ marginBottom: '20px', fontWeight: 'bold' }}>
      👋 Bienvenido {rol === 'admin' ? 'Administrador' : 'Cliente'}
    </p>
  );
}

// 🌐 App principal
function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <Header />
          <div style={{ padding: '20px' }}>
            <Bienvenida />
            <Routes>
              <Route path="/" element={<Catalogo />} />
              <Route path="/login" element={<Login />} />
              <Route path="/carrito" element={<Carrito />} />
              <Route path="/admin" element={
                <AdminRoute>
                  <AdminPanel />
                </AdminRoute>
              } />
              <Route path="/agregar" element={
                <AdminRoute>
                  <ProductoForm />
                </AdminRoute>
              } />
              <Route path="/editar/:id" element={
                <AdminRoute>
                  <EditarProducto />
                </AdminRoute>
              } />
              <Route path="/productos" element={<Navigate to="/admin" />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
          <Footer />
        </Router>
        {/* ✅ Posicionado fuera del Router pero dentro del árbol general */}
        <ToastContainer position="bottom-right" autoClose={3000} theme="light" />
      </CartProvider>
    </AuthProvider>
  );
}

export default App;