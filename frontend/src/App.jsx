import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import ProductoForm from './components/ProductoForm';
import EditarProducto from './pages/EditarProducto';
import Login from './pages/Login';
import { AuthProvider, useAuth } from './context/AuthContext';
import AdminRoute from './routes/AdminRoute';
import Catalogo from './pages/Catalogo';
import { CartProvider } from './context/CartContext';
import Carrito from './pages/Carrito';
import { useCart } from './context/CartContext';
import AdminPanel from './pages/AdminPanel';

// 🧭 Componente de navegación
function Navigation() {
  const { autenticado, rol, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const { carrito } = useCart();
  const totalItems = carrito.reduce((acc, item) => acc + item.cantidad, 0);

  return (
    <nav style={{ marginBottom: '20px' }}>
      <Link to="/carrito" className="carrito-icono">
        🛒 Ver Carrito
        {totalItems > 0 && <span className="carrito-contador">{totalItems}</span>}
      </Link>
      {autenticado && rol === 'admin' && (
        <>
          <Link to="/agregar" style={{ marginRight: '20px' }}>➕ Agregar Producto</Link>
          <Link to="/admin" style={{ marginRight: '20px' }}>🛠️ Panel Admin</Link>
        </>
      )}
      {autenticado ? (
        <button onClick={handleLogout} style={{ marginLeft: '10px' }}>🔓 Cerrar sesión</button>
      ) : (
        <Link to="/login">🔐 Login</Link>
      )}
    </nav>
  );
}

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
          <div style={{ padding: '20px' }}>
            <Navigation />
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
            </Routes>
          </div>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;