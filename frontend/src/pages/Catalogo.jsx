// src/pages/Catalogo.jsx
import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import ProductoCard from '../components/ProductoCard';
import '../styles/Catalogo.css';

const Catalogo = () => {
  const [productos, setProductos] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState('Todas');

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

  // Extraer categorías únicas del inventario
  const categorias = ['Todas', ...new Set(productos.map(p => p.categoria || 'General'))];

  const productosFiltrados = categoriaSeleccionada === 'Todas'
    ? productos
    : productos.filter(p => p.categoria === categoriaSeleccionada);

  return (
    <div className="catalogo-container">
      <h1>🛍️ Catálogo</h1>

        <div className="catalogo-container">
            <h1>🛍️ Catálogo de Productos</h1>
                <div className="grid-productos">
                    {productos.length > 0 ? (
                    productos.map(producto => (
                        <ProductoCard key={producto.id} producto={producto} />
                    ))
                    ) : (
                    <p>No hay productos disponibles.</p>
                    )}
                </div>
        </div>

      <div className="filtros">
        <label htmlFor="filtro-categoria">Filtrar por categoría:</label>
        <select
          id="filtro-categoria"
          value={categoriaSeleccionada}
          onChange={(e) => setCategoriaSeleccionada(e.target.value)}
        >
          {categorias.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div className="productos-grid">
        {productosFiltrados.map(producto => (
          <ProductoCard key={producto.id} producto={producto} />
        ))}
      </div>
    </div>
  );
};

export default Catalogo;