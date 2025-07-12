import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ProductoForm from './components/ProductoForm';
import ListarProductos from './pages/ListarProductos';

function App() {
  return (
    <Router>
      <div style={{ padding: '20px' }}>
        <nav>
          <Link to="/agregar" style={{ marginRight: '20px' }}>➕ Agregar Producto</Link>
          <Link to="/productos">📦 Ver Productos</Link>
        </nav>

        <Routes>
          <Route path="/agregar" element={<ProductoForm />} />
          <Route path="/productos" element={<ListarProductos />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;