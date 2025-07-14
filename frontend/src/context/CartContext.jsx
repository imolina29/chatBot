import React, { createContext, useContext, useState, useEffect } from 'react';

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
    setCarrito(carrito => {
    const existente = carrito.find(p => p.id === producto.id);
    if (existente) {
        return carrito.map(p =>
        p.id === producto.id ? { ...p, cantidad: p.cantidad + 1 } : p
      );
    } 
    return [...carrito, { ...producto, cantidad:1 }];
  });
};

  const quitarProducto = (id) => {
    setCarrito(carrito.filter(p => p.id !== id));
  };

  const vaciarCarrito = () => setCarrito([]);

  return (
    <CartContext.Provider value={{ carrito, agregarProducto, quitarProducto, vaciarCarrito }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);