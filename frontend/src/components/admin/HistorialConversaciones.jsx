import React, { useEffect, useState } from 'react';
import api from '../../api/axios';

const HistorialConversaciones = () => {
  const [conversaciones, setConversaciones] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/api/conversaciones');
        setConversaciones(res.data);
      } catch (error) {
        console.error('Error al obtener historial:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>🗂️ Historial de Conversaciones</h2>
      {conversaciones.length === 0 ? (
        <p>📭 No hay conversaciones registradas.</p>
      ) : (
        <ul>
          {conversaciones.map((c, index) => (
            <li key={index}>
              <strong>{c.rol}</strong>: {c.mensaje}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default HistorialConversaciones;