import React, { useState } from 'react';
import EstadoBot from '../components/admin/EstadoBot';
import HistorialConversaciones from '../components/admin/HistorialConversaciones';
import EstadisticasDashboard from '../components/admin/EstadisticasDashboard';
import '../styles/AdminPanel.css';

const AdminPanel = () => {
  const [seccion, setSeccion] = useState('estadoBot');

  const renderContenido = () => {
    switch (seccion) {
      case 'estadoBot':
        return <EstadoBot />;
      case 'historial':
        return <HistorialConversaciones />;
      case 'estadisticas':
        return <EstadisticasDashboard />;
      default:
        return null;
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
      </div>

      <div className="content-section">
        {renderContenido()}
      </div>
    </div>
  );
};

export default AdminPanel;