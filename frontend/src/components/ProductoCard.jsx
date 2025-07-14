// src/components/ProductoCard.jsx
import React from 'react';
import { useCart } from '../context/CartContext';
import '../styles/ProductoCard.css';

const ProductoCard = ({ producto }) => {
  const { agregarProducto } = useCart();

  const handleAddToCart = () => {
    agregarProducto(producto);
    alert(`✅ "${producto.descripcion_producto}" agregado al carrito`);
  };

  const agotado = producto.stock === 0;
  const ultimasUnidades = producto.stock > 0 && producto.stock <= 5;

  return (
    <div className="producto-card">
      <div className="producto-imagen">
        <img
          src={`/img/${producto.categoria?.toLowerCase() || 'generico'}.jpg`}
          alt={producto.descripcion_producto}
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = '/img/generico.jpg';
          }}
        />
        {agotado && <span className="badge agotado">Agotado</span>}
        {ultimasUnidades && !agotado && <span className="badge ultimas">¡Últimas unidades!</span>}
      </div>

      <div className="producto-info">
        <h3>{producto.descripcion_producto}</h3>
        <p className="categoria">Categoría: {producto.categoria}</p>
        <p className="precio">${producto.valor_venta}</p>
        <p className="stock">Stock: {producto.stock}</p>

        <button
          onClick={handleAddToCart}
          disabled={agotado}
          className={`btn-comprar ${agotado ? 'btn-disabled' : ''}`}
        >
          {agotado ? 'Agotado' : '🛒 Agregar al carrito'}
        </button>
      </div>
    </div>
  );
};

export default ProductoCard;