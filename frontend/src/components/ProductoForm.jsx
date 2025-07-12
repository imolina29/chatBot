import React, { useState } from 'react';
import api from '../api/axios'; // ← Asegúrate que esta ruta es correcta

const ProductoForm = () => {
  const [producto, setProducto] = useState({
    descripcion_producto: '',
    cantidad: 0,
    valor_unitario: 0,
    valor_venta: 0,
    categoria: 'General',
    stock: 0
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProducto({ ...producto, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/api/productos/', producto);
      console.log('✅ Producto creado:', res.data);
      // Opcional: limpiar formulario
      setProducto({
        descripcion_producto: '',
        cantidad: 0,
        valor_unitario: 0,
        valor_venta: 0,
        categoria: 'General',
        stock: 0
      });
    } catch (error) {
      console.error('❌ Error al crear producto:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>➕ Agregar Producto</h2>

      <input
        type="text"
        name="descripcion_producto"
        placeholder="Descripción"
        value={producto.descripcion_producto}
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="cantidad"
        placeholder="Cantidad"
        value={producto.cantidad}
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="valor_unitario"
        placeholder="Valor Unitario"
        value={producto.valor_unitario}
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="valor_venta"
        placeholder="Valor Venta"
        value={producto.valor_venta}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="categoria"
        placeholder="Categoría"
        value={producto.categoria}
        onChange={handleChange}
      />
      <input
        type="number"
        name="stock"
        placeholder="Stock"
        value={producto.stock}
        onChange={handleChange}
      />

      <button type="submit">Guardar</button>
    </form>
  );
};

export default ProductoForm;