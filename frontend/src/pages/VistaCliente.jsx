// src/pages/VistaCliente.jsx
import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import '../styles/VistaCliente.css';

const VistaCliente = () => {
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
    <div className="vista-cliente">
      <h1 className="titulo">🛍 Nuestros Productos</h1>
      <div className="grid-productos">
        {productos.length > 0 ? (
          productos.map((prod) => (
            <div className="tarjeta-producto" key={prod.id}>
              <img
                src="https://via.placeholder.com/200x150"
                alt={prod.descripcion_producto}
                className="imagen-producto"
              />
              <h3>{prod.descripcion_producto}</h3>
              <p>Categoría: <strong>{prod.categoria}</strong></p>
              <p>Precio: <strong>${prod.valor_venta}</strong></p>
              <p>Stock: {prod.stock > 0 ? prod.stock : 'Agotado'}</p>
              <button className="btn-agregar" disabled>
                Agregar al carrito
              </button>
            </div>
          ))
        ) : (
          <p>No hay productos disponibles</p>
        )}
      </div>
    </div>
  );
};

export default VistaCliente;