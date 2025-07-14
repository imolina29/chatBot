// src/pages/AdminDashboard.jsx

import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import ProductoTabla from '../components/ProductoTabla';
import { useNavigate, Link } from 'react-router-dom';
import '../styles/ListarProductos.css'; // ✅ estilo compartido con ListarProductos

const AdminDashboard = () => {
  const [productos, setProductos] = useState([]);
  const [botStatus, setBotStatus] = useState(null);
  const [loadingBot, setLoadingBot] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProductos();
    obtenerEstadoBot();
  }, []);

  const fetchProductos = async () => {
    try {
      const res = await api.get('/api/productos/');
      setProductos(res.data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
    }
  };

  const handleEliminar = async (id) => {
    if (!window.confirm('¿Estás seguro de eliminar este producto?')) return;

    try {
      await api.delete(`/api/productos/${id}`);
      setProductos(prev => prev.filter(p => p.id !== id));
    } catch (error) {
      console.error('Error al eliminar producto:', error);
    }
  };

  const handleEditar = (id) => {
    navigate(`/editar/${id}`);
  };

  const handleToggleActivo = async (id) => {
    try {
      const producto = productos.find(p => p.id === id);
      const actualizado = { ...producto, activo: !producto.activo };

      await api.put(`/api/productos/${id}`, actualizado);
      setProductos(prev =>
        prev.map(p => (p.id === id ? { ...p, activo: actualizado.activo } : p))
      );
    } catch (error) {
      console.error('Error al cambiar estado activo:', error);
    }
  };

  const obtenerEstadoBot = async () => {
    try {
      const res = await api.get('/status');
      setBotStatus(res.data?.mensaje || 'Desconocido');
    } catch (err) {
      setBotStatus('❌ Error al obtener estado');
    }
  };

  const cambiarEstado = async (accion) => {
    setLoadingBot(true);
    try {
      await api.post(`/${accion}`);
      await obtenerEstadoBot();
    } catch (error) {
      alert('Error al cambiar estado del bot');
    }
    setLoadingBot(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <div className="admin-container">
        <h1>🛠️ Panel de Administración</h1>

        <section className="estado-bot">
          <h2>🤖 Estado del Bot</h2>

          <div className="bot-estado-info">
            <strong>Estado:</strong>
            {botStatus === null ? (
              <span className="estado-cargando">🟡 Cargando...</span>
            ) : botStatus.includes('ok') ? (
              <span className="estado-activo">✅ Activo</span>
            ) : (
              <span className="estado-inactivo">⛔ Inactivo</span>
            )}
          </div>

          <div className="bot-botones">
            <button
              onClick={() => cambiarEstado('activar')}
              disabled={loadingBot}
              className="btn-activar"
            >
              🔄 Activar Bot
            </button>

            <button
              onClick={() => cambiarEstado('desactivar')}
              disabled={loadingBot}
              className="btn-desactivar"
            >
              ⛔ Desactivar Bot
            </button>
          </div>
        </section>

        <section className="acciones-admin">
          <Link to="/agregar" className="btn-agregar">➕ Agregar Producto</Link>
        </section>

        <ProductoTabla
          productos={productos}
          onEditar={handleEditar}
          onEliminar={handleEliminar}
          onToggleActivo={handleToggleActivo}
        />
      </div>
    </div>
  );
};

export default AdminDashboard;