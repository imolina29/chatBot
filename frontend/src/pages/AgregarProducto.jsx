// src/pages/AgregarProducto.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import ProductoForm from '../components/ProductoForm';

const AgregarProducto = () => {
  const navigate = useNavigate();

  const handleCrear = async (data) => {
    try {
      await api.post('/api/productos/', data);
      alert('✅ Producto creado correctamente');
      navigate('/');
    } catch (error) {
      console.error('❌ Error al crear producto:', error);
    }
  };

  return <ProductoForm onSubmit={handleCrear} modo="crear" />;
};

export default AgregarProducto;