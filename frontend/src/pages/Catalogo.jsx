// src/pages/Catalogo.jsx
import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import ProductoCard from '../components/ProductoCard';
import CategoriasGrid from '../components/CategoriasGrid';
import '../styles/Catalogo.css';

const Catalogo = () => {
  const [productos, setProductos] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState(null);

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

  const productosFiltrados = categoriaSeleccionada
    ? productos.filter(p => p.categoria === categoriaSeleccionada)
    : productos;

  return (
    <div className="catalogo-container">
      <h1>🛍️ Catálogo</h1>

      <CategoriasGrid onSeleccionarCategoria={setCategoriaSeleccionada} />

      <div className="productos-grid">
        {productosFiltrados.length > 0 ? (
          productosFiltrados.map(producto => (
            <ProductoCard key={producto.id} producto={producto} />
          ))
        ) : (
          <p>No hay productos disponibles.</p>
        )}
      </div>
    </div>
  );
};

export default Catalogo;