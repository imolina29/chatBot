// src/components/ResumenPedido.jsx
import React, { useEffect } from 'react';
import axios from 'axios';
import '../styles/ResumenPedido.css';

const ResumenPedido = ({ pedido, onVolver }) => {
  const { cliente, productos, total } = pedido;

  useEffect(() => {
    if (pedido && pedido.cliente?.email) {
      axios.post('/api/enviar-resumen', pedido)
        .then(() => console.log("📧 Resumen enviado al correo"))
        .catch((err) => console.error("❌ Error enviando correo:", err));
    }
  }, [pedido]);

  return (
    <div className="resumen-pedido-card">
      <h2 className="titulo-principal">¡Gracias por tu compra!</h2>
      <p className="subtitulo">Hemos recibido tu pedido exitosamente. A continuación te mostramos el resumen:</p>

      <div className="card-contenido">
        <div className="seccion-cliente">
          <h3>Datos del Cliente</h3>
          <ul>
            <li><strong>Nombre:</strong> {cliente.nombre}</li>
            <li><strong>Email:</strong> {cliente.email}</li>
            <li><strong>Teléfono:</strong> {cliente.telefono}</li>
            <li><strong>Dirección:</strong> {cliente.direccion}</li>
            <li><strong>Ciudad:</strong> {cliente.ciudad}</li>
            <li><strong>Referencia:</strong> {cliente.referencia}</li>
            <li><strong>Código Postal:</strong> {cliente.codigoPostal}</li>
          </ul>
        </div>

        <div className="seccion-productos">
          <h3>Productos Comprados</h3>
          <table>
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              {productos.map((p, idx) => (
                <tr key={idx}>
                  <td>{p.nombre}</td>
                  <td>{p.cantidad}</td>
                  <td>${(p.precio * p.cantidad).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="total-final">
            <strong>Total:</strong> ${total.toFixed(2)}
          </div>
        </div>
      </div>

      <div className="boton-volver-contenedor">
        <button className="btn-volver" onClick={onVolver}>
          Volver al catálogo
        </button>
      </div>
    </div>
  );
};

export default ResumenPedido;