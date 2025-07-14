// src/pages/Carrito.jsx
import React, { useState } from 'react';
import { useCart } from '../context/CartContext';
import api from '../api/axios';
import '../styles/Carrito.css';

const Carrito = () => {
  const { carrito, quitarProducto, vaciarCarrito } = useCart();
  const [mensaje, setMensaje] = useState('');
  const total = carrito.reduce((acc, item) => acc + item.valor_venta * item.cantidad, 0);

  const finalizarCompra = async () => {
    if (carrito.length === 0) return;

    try {
       await api.post('/api/finalizar-compra', carrito.map(item => ({
        id: item.id,
        cantidad: item.cantidad
      })));

      setMensaje("✅ Compra finalizada con éxito");
      vaciarCarrito();
      setTimeout(() => setMensaje(''), 4000);
    } catch (error) {
      console.error('Error al finalizar la compra:', error);
      setMensaje('❌ Error: No se pudo completar la compra. Verifica el stock disponible.');
      setTimeout(() => setMensaje(''), 4000);
      console.log("Datos enviados al backend:", carrito.map(item => ({
        id: item.id,
        cantidad: item.cantidad
        })));
    }
  };

  return (
    <div className="carrito-container">
      <h1>🛒 Mi Carrito</h1>

      {mensaje && <div className="carrito-mensaje">{mensaje}</div>}

      {carrito.length === 0 ? (
        <p className="carrito-vacio">No hay productos en el carrito.</p>
      ) : (
        <div className="carrito-card">
          <ul className="carrito-lista">
            {carrito.map((item) => (
              <li key={item.id} className="carrito-item">
                <div>                  
                    <strong>📦 {item.descripcion_producto}</strong>
                  <p>
                    Cantidad: {item.cantidad} | Total: ${item.valor_venta * item.cantidad}
                  </p></div>
                <button className="btn-eliminar" onClick={() => quitarProducto(item.id)}>❌</button>
              </li>
            ))}
          </ul>

          <div className="carrito-footer">
            <h3>🧮 Total: ${total}</h3>
            <div className="carrito-botones">
              <button className="btn-vaciar" onClick={vaciarCarrito}>🧹 Vaciar Carrito</button>
              <button className="btn-finalizar" onClick={finalizarCompra}>✅ Finalizar Compra</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Carrito;