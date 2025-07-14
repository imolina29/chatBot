// src/components/ProductoForm.jsx
import React, { useState, useEffect } from 'react';
import '../styles/ProductoForm.css'; // ✅ Importa estilos externos

const ProductoForm = ({ initialData = null, onSubmit, modo = "crear" }) => {
  const [producto, setProducto] = useState({
    descripcion_producto: '',
    cantidad: 0,
    valor_unitario: 0,
    valor_venta: 0,
    categoria: 'General',
    stock: 0
  });

  useEffect(() => {
    if (initialData) {
      setProducto(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProducto({ ...producto, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(producto);
  };

  return (
    <div className="formulario-producto">
      <form onSubmit={handleSubmit}>
        <h2>{modo === "editar" ? "✏️ Editar Producto" : "➕ Agregar Producto"}</h2>
        
        <input
          className="form-input"
          type="text"
          name="descripcion_producto"
          placeholder="Descripción"
          value={producto.descripcion_producto}
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          type="number"
          name="cantidad"
          placeholder="Cantidad"
          value={producto.cantidad}
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          type="number"
          name="valor_unitario"
          placeholder="Valor Unitario"
          value={producto.valor_unitario}
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          type="number"
          name="valor_venta"
          placeholder="Valor Venta"
          value={producto.valor_venta}
          onChange={handleChange}
          required
        />
        <input
          className="form-input"
          type="text"
          name="categoria"
          placeholder="Categoría"
          value={producto.categoria}
          onChange={handleChange}
        />
        <input
          className="form-input"
          type="number"
          name="stock"
          placeholder="Stock"
          value={producto.stock}
          onChange={handleChange}
        />

        <button type="submit" className="form-button">
          {modo === "editar" ? "Guardar Cambios" : "Guardar Producto"}
        </button>
      </form>
    </div>
  );
};

export default ProductoForm;