// src/components/CategoriaCard.jsx
import React from 'react';
import '../styles/CategoriaCard.css';

const CategoriaCard = ({ nombre, imagen, onClick }) => {
  return (
    <div className="categoria-card" onClick={() => onClick(nombre)}>
      <img src={imagen} alt={nombre} className="categoria-imagen" />
      <div className="categoria-label">{nombre}</div>
    </div>
  );
};

export default CategoriaCard;