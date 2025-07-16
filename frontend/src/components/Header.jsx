// src/components/Header.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import '../styles/Header.css';

const Header = () => {
  const { autenticado, logout } = useAuth();
  const { carrito } = useCart();
  const navigate = useNavigate();

  const totalItems = carrito.reduce((acc, item) => acc + item.cantidad, 0);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <div className="header-left">
        <Link to="/" className="logo">📱 MiTienda</Link>
      </div>

      <div className="header-right">
        <Link to="/carrito" className="header-btn">
          🛒 Carrito
          {totalItems > 0 && <span className="carrito-contador">{totalItems}</span>}
        </Link>

        {!autenticado ? (
          <Link to="/login" className="header-btn">🔐 Login</Link>
        ) : (
          <button onClick={handleLogout} className="header-btn">🔓 Logout</button>
        )}
      </div>
    </header>
  );
};

export default Header;