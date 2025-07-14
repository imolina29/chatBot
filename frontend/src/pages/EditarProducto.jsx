// src/pages/EditarProducto.jsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ProductoForm from '../components/ProductoForm';
import axios from '../api/axios';

const EditarProducto = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [producto, setProducto] = useState(null);

  useEffect(() => {
    const obtenerProducto = async () => {
      try {
        const response = await axios.get(`/api/productos/${id}`);
        setProducto(response.data);
      } catch (error) {
        console.error('Error al obtener el producto:', error);
      }
    };

    obtenerProducto();
  }, [id]);

  const handleUpdate = async (productoActualizado) => {
    try {
      await axios.put(`/api/productos/${id}`, productoActualizado);
      navigate('/productos');
    } catch (error) {
      console.error('Error al actualizar el producto:', error);
    }
  };

  return (
    <div className="formulario-producto">
      {producto ? (
        <ProductoForm
          initialData={producto}
          onSubmit={handleUpdate}
          modo="editar"
        />
      ) : (
        <p>Cargando producto...</p>
      )}
    </div>
  );
};

export default EditarProducto;