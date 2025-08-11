// src/pages/FormularioEnvio.jsx
import React, { useState } from 'react';
import { useCart } from '../context/CartContext';
import api from '../api/axios';
import '../styles/FormularioEnvio.css';

const ciudadesColombia = [
  'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Bucaramanga', 'Manizales',
  'Pereira', 'Santa Marta', 'Cúcuta', 'Armenia', 'Ibagué', 'Neiva'
];

const FormularioEnvio = () => {
  const { carrito, vaciarCarrito } = useCart();
  const [cliente, setCliente] = useState({
    nombres: '',
    identificacion: '',
    email: '',
    telefono: '',
    ciudad: '',
    direccion: '',
    codigo_postal: '',
    referencia: '',
    guardar_datos: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setCliente(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };
  const [mensaje, setMensaje] = useState('');
  const [resumen, setResumen] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (carrito.length === 0) {
      setMensaje('❌ Tu carrito está vacío.');
      return;
    }

    try {
      const response = await api.post('/api/registrar-pedido', {
        cliente,
        productos: carrito.map(item => ({
          id: item.id,
          cantidad: item.cantidad
        }))
      });

      setResumen(response.data);
      vaciarCarrito();
      setMensaje('');
    } catch (error) {
      console.error('Error al registrar pedido:', error);
      setMensaje('❌ No se pudo completar el pedido. Verifica tus datos.');
    }
  };

  if (resumen) {
    return (
      <div className="resumen-container">
        <h2>✅ Pedido confirmado</h2>
        <p><strong>Número de pedido:</strong> {resumen.numero_pedido}</p>
        <p><strong>Total:</strong> ${resumen.total}</p>
        <h3>📦 Productos:</h3>
        <ul>
          {resumen.detalle.map((item, i) => (
            <li key={i}>{item.descripcion_producto} - Cantidad: {item.cantidad}</li>
          ))}
        </ul>
        <h3>📍 Enviado a:</h3>
        <p>{resumen.cliente.nombres} ({resumen.cliente.identificacion})</p>
        <p>{resumen.cliente.direccion}, {resumen.cliente.ciudad}</p>
        <p>📩 {resumen.cliente.email} | 📞 {resumen.cliente.telefono}</p>
      </div>
    );
  }

  return (
    <div className="formulario-envio">
      <h2>📬 Información de Envío</h2>
      {mensaje && <p className="mensaje-error">{mensaje}</p>}

      <form className="formulario-grid" onSubmit={handleSubmit}>
        <div className="campo">
          <label>Nombre completo</label>
          <input type="text" name="nombres" required onChange={handleChange} />
        </div>
        <div className="campo">
          <label>Número de identificación</label>
          <input type="text" name="identificacion" required onChange={handleChange} />
        </div>

        <div className="campo">
          <label>Correo electrónico</label>
          <input type="email" name="email" required onChange={handleChange} />
        </div>
        <div className="campo">
          <label>Teléfono</label>
          <input type="tel" name="telefono" required onChange={handleChange} />
        </div>

        <div className="campo">
          <label>Ciudad de residencia</label>
          <select name="ciudad" required onChange={handleChange}>
            <option value="">Selecciona tu ciudad</option>
            {ciudadesColombia.map((ciudad, i) => (
              <option key={i} value={ciudad}>{ciudad}</option>
            ))}
          </select>
        </div>
        <div className="campo">
          <label>Dirección de envío</label>
          <input type="text" name="direccion" required onChange={handleChange} />
        </div>

        <div className="campo">
          <label>Referencia adicional</label>
          <input type="text" name="referencia" onChange={handleChange} />
        </div>
        <div className="campo">
          <label>Código postal</label>
          <input type="text" name="codigo_postal" required onChange={handleChange} />
        </div>

        <div className="campo-full">
          <label>Mensaje adicional</label>
          <textarea name="mensaje" onChange={(e) => setMensaje(e.target.value)} />
        </div>

        <div className="campo-full checkbox">
          <label>
            <input type="checkbox" name="guardar_datos" onChange={handleChange} />
            Guardar mis datos para una próxima compra
          </label>
        </div>

        <div className="boton-envio">
          <button type="submit">📦 Confirmar Pedido</button>
        </div>
      </form>
    </div>
  );
};

export default FormularioEnvio;