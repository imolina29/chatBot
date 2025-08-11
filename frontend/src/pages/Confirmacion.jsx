import React from 'react';
import { useLocation } from 'react-router-dom';
import FormularioEnvio from '../components/FormularioEnvio';
import '../styles/Confirmacion.css';

const Confirmacion = () => {
  const location = useLocation();
  const productosComprados = location.state?.carrito || [];

  const total = productosComprados.reduce((acc, item) => acc + item.valor_venta * item.cantidad, 0);

  const handleFormularioSubmit = (datos) => {
    console.log('📦 Datos de envío recibidos:', datos);
    console.log('🧾 Productos comprados:', productosComprados);
    // Aquí luego se enviará a backend para registrar pedido + cliente
  };

  return (
    <div className="confirmacion-container">
      <h1>✅ ¡Gracias por tu compra!</h1>
      <h2>🧾 Resumen de la compra:</h2>
      <ul className="lista-productos">
        {productosComprados.map((item) => (
          <li key={item.id}>
            {item.descripcion_producto} x {item.cantidad} → ${item.valor_venta * item.cantidad}
          </li>
        ))}
      </ul>
      <h3>Total: ${total}</h3>

      <FormularioEnvio onSubmit={handleFormularioSubmit} />
    </div>
  );
};

export default Confirmacion;