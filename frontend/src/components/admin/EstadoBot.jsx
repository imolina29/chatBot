import React, { useEffect, useState } from 'react';
import api from '../../api/axios';

const EstadoBot = () => {
  const [estado, setEstado] = useState(null);
  const [cargando, setCargando] = useState(true);

  const obtenerEstado = async () => {
    try {
      const res = await api.get('/status');
      setEstado(res.data.mensaje || 'Desconocido');
    } catch (err) {
      setEstado('❌ Error al obtener estado');
    } finally {
      setCargando(false);
    }
  };

  const cambiarEstado = async (accion) => {
    try {
      await api.post(`/${accion}`);
      obtenerEstado();
    } catch (error) {
      alert('Error al cambiar el estado del bot');
    }
  };

  useEffect(() => {
    obtenerEstado();
  }, []);

  return (
    <div>
      <h2>🤖 Estado del Bot</h2>
      {cargando ? (
        <p>🔄 Consultando estado...</p>
      ) : (
        <p><strong>Estado actual:</strong> {estado}</p>
      )}

      <button
        onClick={() => cambiarEstado('activar')}
        style={{ marginRight: '10px', backgroundColor: '#4CAF50', color: '#fff', padding: '8px', borderRadius: '5px' }}
      >
        ✅ Activar
      </button>
      <button
        onClick={() => cambiarEstado('desactivar')}
        style={{ backgroundColor: '#f44336', color: '#fff', padding: '8px', borderRadius: '5px' }}
      >
        ⛔ Desactivar
      </button>
    </div>
  );
};

export default EstadoBot;