// src/components/CategoriasGrid.jsx
import React from 'react';
import '../styles/CategoriasGrid.css';

const categorias = [
  { nombre: 'Accesorios', imagen: '/img/categorias/accesorios.jpg' },
  { nombre: 'Calzado', imagen: '/img/categorias/calzado.jpg' },
  { nombre: 'Gafas', imagen: '/img/categorias/gafas.jpg' },
  { nombre: 'Relojes', imagen: '/img/categorias/relojes.jpg' },
  { nombre: 'Perfumes', imagen: '/img/categorias/perfumes.jpg' },
  { nombre: 'Ropa', imagen: '/img/categorias/ropa.jpg' },
];

const CategoriasGrid = ({ onSeleccionarCategoria }) => {
  return (
    <div className="categorias-grid">
      {categorias.map((cat) => (
        <div
          key={cat.nombre}
          className="categoria-card"
          onClick={() => onSeleccionarCategoria(cat.nombre)}
        >
          <img src={cat.imagen} alt={cat.nombre} />
          <div className="categoria-nombre">{cat.nombre}</div>
        </div>
      ))}
    </div>
  );
};

export default CategoriasGrid;