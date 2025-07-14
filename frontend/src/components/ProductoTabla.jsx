import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/ProductoTabla.css'

const ProductoTabla = ({ productos, onEliminar, onToggleActivo }) => {
  const navigate = useNavigate();

  return (
    <table border="1" cellPadding="10" style={{ width: '100%', marginTop: '20px' }}>
      <thead>
        <tr>
          <th>ID</th>
          <th>Descripción</th>
          <th>Categoría</th>
          <th>Cantidad</th>
          <th>Valor Unitario</th>
          <th>Valor Venta</th>
          <th>Stock</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {productos.length > 0 ? (
          productos.map(prod => (
            <tr key={prod.id}>
              <td>{prod.id}</td>
              <td>{prod.descripcion_producto}</td>
              <td>{prod.categoria}</td>
              <td>{prod.cantidad}</td>
              <td>{prod.valor_unitario}</td>
              <td>{prod.valor_venta}</td>
              <td>{prod.stock}</td>
              <td>{prod.activo ? '✅' : '❌'}</td>
              <td>
                <button className="editar" onClick={() => navigate(`/editar/${prod.id}`)}>✏️</button>
                <button className="eliminar" onClick={() => onEliminar(prod.id)} style={{ marginLeft: 8 }}>🗑️</button>
                <button className="toggle" onClick={() => onToggleActivo(prod.id)} style={{ marginLeft: 8 }}>
                  {prod.activo ? 'Desactivar' : 'Activar'}
                </button>
              </td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="9" style={{ textAlign: 'center' }}>No hay productos</td>
          </tr>
        )}
      </tbody>
    </table>
  );
};

export default ProductoTabla;