// src/pages/Carrito.jsx
import React, { useState } from 'react';
import { useCart } from '../context/CartContext';
import '../styles/Carrito.css';
import FormularioEnvio from '../components/FormularioEnvio';
import ResumenPedido from '../components/ResumenPedido';

const Carrito = () => {
  const { carrito, quitarProducto, vaciarCarrito, actualizarCantidad } = useCart();
  const [pasoActual, setPasoActual] = useState('carrito'); // 'carrito' | 'envio' | 'resumen'
  const [pedido, setPedido] = useState(null);
  const [error, setError] = useState(null);

  const total = carrito.reduce((acc, item) => acc + item.valor_venta * item.cantidad, 0);

  const confirmarEnvio = async (datosCliente) => {
    try {
      // Construir payload para el backend
      const compraPayload = carrito.map(item => ({
        id: item.id,
        cantidad: item.cantidad
      }));

      // Hacer POST a /api/productos/finalizar-compra
      const response = await fetch('/api/productos/finalizar-compra', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(compraPayload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al finalizar compra');
      }

      const nuevoPedido = {
        cliente: datosCliente,
        productos: carrito,
        total,
      };

      setPedido(nuevoPedido);
      vaciarCarrito();
      setPasoActual('resumen');
      setError(null); // Limpiar errores previos si todo salió bien
    } catch (err) {
      setError(err.message || 'Error desconocido al finalizar la compra.');
    }
  };

  const volverAlCatalogo = () => {
    setPedido(null);
    setPasoActual('carrito');
    window.location.href = '/catalogo';
  };

  // PANTALLA: CARRITO
  if (pasoActual === 'carrito') {
    return (
      <div className="carrito-container">
        <h1>🛒 Mi Carrito</h1>
        {carrito.length === 0 ? (
          <p className="carrito-vacio">No hay productos en el carrito.</p>
        ) : (
          <div className="carrito-card">
            <ul className="carrito-lista">
              {carrito.map((item) => (
                <li key={item.id} className="carrito-item">
                  <div>
                    <strong>📦 {item.descripcion_producto}</strong>
                    <div className="carrito-cantidad">
                      <button
                        onClick={() =>
                          actualizarCantidad(item.id, Math.max(1, item.cantidad - 1))
                        }
                        disabled={item.cantidad === 1}
                      >
                        ➖
                      </button>
                      <span>{item.cantidad}</span>
                      <button
                        onClick={() => {
                          if (item.cantidad < item.stock) {
                            actualizarCantidad(item.id, item.cantidad + 1);
                          }
                        }}
                        disabled={item.cantidad >= item.stock}
                      >
                        ➕
                      </button>
                      <span> | Total: ${item.valor_venta * item.cantidad}</span>
                    </div>
                  </div>
                  <button
                    className="btn-eliminar"
                    onClick={() => quitarProducto(item.id)}
                  >
                    ❌
                  </button>
                </li>
              ))}
            </ul>

            <div className="carrito-footer">
              <h3>🧮 Total: ${total.toFixed(2)}</h3>
              <div className="carrito-botones">
                <button className="btn-vaciar" onClick={vaciarCarrito}>
                  🧹 Vaciar Carrito
                </button>
                <button
                  className="boton-finalizar"
                  onClick={() => setPasoActual('envio')}
                >
                  🧾 Finalizar Compra
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // PANTALLA: FORMULARIO DE ENVÍO
  if (pasoActual === 'envio') {
    return (
      <div className="carrito-container">
        <h2>📦 Datos de Envío</h2>
        {error && <p className="error-compra">❌ {error}</p>}
        <FormularioEnvio onConfirmar={confirmarEnvio} />
        <button onClick={() => setPasoActual('carrito')} className="btn-regresar">
          🔙 Regresar
        </button>
      </div>
    );
  }

  // PANTALLA: RESUMEN DE PEDIDO
  if (pasoActual === 'resumen') {
    return (
      <div className="carrito-container">
        <ResumenPedido pedido={pedido} onVolver={volverAlCatalogo} />
      </div>
    );
  }

  return null;
};

export default Carrito;