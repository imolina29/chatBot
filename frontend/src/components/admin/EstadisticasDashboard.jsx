import React, { useEffect, useState } from 'react';
import api from '../../api/axios';

const EstadisticasDashboard = () => {
  const [stats, setStats] = useState({
    totalProductos: 0,
    totalConversaciones: 0,
    stockTotal: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const productos = await api.get('/api/productos/');
        const conversaciones = await api.get('/api/conversaciones');

        const stockTotal = productos.data.reduce((acc, prod) => acc + prod.stock, 0);

        setStats({
          totalProductos: productos.data.length,
          totalConversaciones: conversaciones.data.length,
          stockTotal
        });
      } catch (error) {
        console.error('Error al cargar estadísticas:', error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div>
      <h2>📈 Estadísticas Generales</h2>
      <ul>
        <li>📦 Productos registrados: <strong>{stats.totalProductos}</strong></li>
        <li>💬 Conversaciones registradas: <strong>{stats.totalConversaciones}</strong></li>
        <li>📊 Stock total en inventario: <strong>{stats.stockTotal}</strong></li>
      </ul>
    </div>
  );
};

export default EstadisticasDashboard;