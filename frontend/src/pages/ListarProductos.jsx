import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import axios from '../api/axios';

const ListarProductos = () => {
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const res = await api.get('/api/productos/');
        setProductos(res.data);
      } catch (error) {
        console.error('Error al obtener productos:', error);
      }
    };

    fetchProductos();
  }, []);

  return (
    <div>
      <h1>📦 Productos en Inventario</h1>
      <table border="1" cellPadding="10" style={{ width: '100%', marginTop: '20px' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Descripción</th>
            <th>Categoría</th>
            <th>Cantidad</th>
            <th>Valor Unitario</th>
            <th>Valor Venta</th>
            <th>Stock</th>
          </tr>
        </thead>
        <tbody>
          {productos.length > 0 ? (
            productos.map(prod => (
              <tr key={prod.id}>
                <td>{prod.id}</td>
                <td>{prod.descripcion_producto}</td>
                <td>{prod.categoria}</td>
                <td>{prod.cantidad}</td>
                <td>{prod.valor_unitario}</td>
                <td>{prod.valor_venta}</td>
                <td>{prod.stock}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="7" style={{ textAlign: 'center' }}>No hay productos</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ListarProductos;