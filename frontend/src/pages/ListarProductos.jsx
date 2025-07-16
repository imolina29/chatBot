// src/components/ListarProductos.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import '../styles/ListarProductos.css';

const ListarProductos = ({ modoAdmin = false }) => {
  const [productos, setProductos] = useState([]);
  const navigate = useNavigate();

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

  const handleEliminar = async (id) => {
    const confirm = window.confirm('¿Estás seguro de eliminar este producto?');
    if (!confirm) return;

    try {
      await api.delete(`/api/productos/${id}`);
      setProductos(productos.filter((p) => p.id !== id));
    } catch (error) {
      console.error('Error al eliminar:', error);
      alert('No se pudo eliminar el producto.');
    }
  };

  const handleEditar = (id) => {
    navigate(`/editar/${id}`);
  };

  return (
    <div className="contenedor-listado">
      <h2 className="titulo-lista">📦 Productos en Inventario</h2>

      <table className="tabla-productos">
        <thead>
          <tr>
            <th>ID</th>
            <th>Descripción</th>
            <th>Categoría</th>
            <th>Cantidad</th>
            <th>Valor Unitario</th>
            <th>Valor Venta</th>
            <th>Stock</th>
            {modoAdmin && <th>Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {productos.length > 0 ? (
            productos.map((prod) => (
              <tr key={prod.id}>
                <td>{prod.id}</td>
                <td>{prod.descripcion_producto}</td>
                <td>{prod.categoria}</td>
                <td>{prod.cantidad}</td>
                <td>${prod.valor_unitario}</td>
                <td>${prod.valor_venta}</td>
                <td>
                  {prod.stock}
                  {prod.stock <= 5 && (
                    <span className="stock-bajo"> ⚠️ Últimas unidades</span>
                  )}
                </td>
                {modoAdmin && (
                  <td>
                    <button onClick={() => handleEditar(prod.id)} className="btn-editar">
                      ✏️ Editar
                    </button>
                    <button onClick={() => handleEliminar(prod.id)} className="btn-eliminar">
                      🗑️ Eliminar
                    </button>
                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={modoAdmin ? 8 : 7} style={{ textAlign: 'center' }}>
                No hay productos disponibles.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ListarProductos;