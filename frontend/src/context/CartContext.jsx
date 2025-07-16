import React, { createContext, useContext, useState, useEffect } from 'react';
import { toast } from 'react-toastify';

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [carrito, setCarrito] = useState(() => {
    const guardado = localStorage.getItem('carrito');
    return guardado ? JSON.parse(guardado) : [];
  });

  useEffect(() => {
    localStorage.setItem('carrito', JSON.stringify(carrito));
  }, [carrito]);

  const agregarProducto = (producto) => {
    if (producto.stock === 0) {
      toast.error(`❌ "${producto.descripcion_producto}" está agotado`);
      return;
    }

    setCarrito((carritoAnterior) => {
      const existente = carritoAnterior.find(p => p.id === producto.id);

      if (existente) {
        if (existente.cantidad >= producto.stock) {
          toast.warning(`⚠️ Ya agregaste todas las unidades disponibles de "${producto.descripcion_producto}"`);
          return carritoAnterior;
        }

        toast.success(`✅ Se agregó otra unidad de "${producto.descripcion_producto}"`);
        return carritoAnterior.map(p =>
          p.id === producto.id
            ? { ...p, cantidad: p.cantidad + 1 }
            : p
        );
      }

      toast.success(`✅ "${producto.descripcion_producto}" agregado al carrito`);
      return [...carritoAnterior, { ...producto, cantidad: 1 }];
    });
  };

  const quitarProducto = (id) => {
    setCarrito((carrito) => carrito.filter((p) => p.id !== id));
  };

  const vaciarCarrito = () => setCarrito([]);

  const actualizarCantidad = (id, nuevaCantidad) => {
    setCarrito(prev =>
      prev.map(p =>
        p.id === id
          ? { ...p, cantidad: nuevaCantidad }
          : p
      )
    );
  };

  return (
    <CartContext.Provider value={{ carrito, agregarProducto, quitarProducto, vaciarCarrito, actualizarCantidad }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);