// src/components/BannerSlider.jsx
import React, { useEffect, useState } from 'react';
import '../styles/BannerSlider.css';

const imagenes = [
  '/banner/accesorios.jpg',
  '/banner/relojes.jpg',
  '/banner/ropa.jpg',
  '/banner/gafas.jpg',
  '/banner/calzado.jpg',
  '/banner/perfumes.jpg'
];

const BannerSlider = () => {
  const [indice, setIndice] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndice((prev) => (prev + 1) % imagenes.length);
    }, 4000); // cada 4 segundos

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="banner-slider">
      <img src={imagenes[indice]} alt={`Banner ${indice}`} className="banner-imagen" />
    </div>
  );
};

export default BannerSlider;