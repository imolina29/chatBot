// src/pages/AdminPanel.jsx
import React, { useState } from 'react';
import EstadoBot from '../components/admin/EstadoBot';
import HistorialConversaciones from '../components/admin/HistorialConversaciones';
import EstadisticasDashboard from '../components/admin/EstadisticasDashboard';
import ListarProductos from './ListarProductos'; // asegúrate que esta ruta es válida
import '../styles/AdminPanel.css'; // archivo opcional para estilos

const AdminPanel = () => {
  const [seccion, setSeccion] = useState('productos'); // ← "productos" por defecto

  const renderContenido = () => {
    switch (seccion) {
      case 'estadoBot':
        return <EstadoBot />;
      case 'historial':
        return <HistorialConversaciones />;
      case 'estadisticas':
        return <EstadisticasDashboard />;
      case 'productos':
      default:
        return <ListarProductos modoAdmin={true} />;
    }
  };

  return (
    <div className="admin-panel">
      <h1>🛠️ Panel de Administración</h1>

      <div className="nav-buttons">
        <button
          onClick={() => setSeccion('estadoBot')}
          className={seccion === 'estadoBot' ? 'active' : ''}
        >
          🔌 Estado del Bot
        </button>
        <button
          onClick={() => setSeccion('historial')}
          className={seccion === 'historial' ? 'active' : ''}
        >
          🗂️ Historial de Conversaciones
        </button>
        <button
          onClick={() => setSeccion('estadisticas')}
          className={seccion === 'estadisticas' ? 'active' : ''}
        >
          📊 Estadísticas
        </button>
        <button
          onClick={() => setSeccion('productos')}
          className={seccion === 'productos' ? 'active' : ''}
        >
          📦 Productos
        </button>
      </div>

      <div className="content-section">
        {renderContenido()}
      </div>
    </div>
  );
};

export default AdminPanel;