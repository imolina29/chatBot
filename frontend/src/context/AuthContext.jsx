import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [autenticado, setAutenticado] = useState(() => {
    const datosGuardados = JSON.parse(localStorage.getItem('auth')) || {};
    return datosGuardados.autenticado || false;
  });

    const [rol, setRol] = useState(() => {
    return localStorage.getItem('rol') || null;
    });

  // 💾 Guardar cambios en localStorage cuando cambian
    useEffect(() => {
    localStorage.setItem('rol', rol);
    }, [rol]);

  // ✅ Validación de usuario y contraseña en el login
  const login = (username, password) => {
    if (username === 'admin' && password === 'admin123') {
      setAutenticado(true);
      setRol('admin');
      return true;
    } else if (username === 'cliente' && password === 'cliente123') {
      setAutenticado(true);
      setRol('cliente');
      return true;
    }
    return false;
  };

    const logout = () => {
    setAutenticado(false);
    setRol(null);
    localStorage.removeItem('autenticado');
    localStorage.removeItem('rol');
    };

  return (
    <AuthContext.Provider value={{ autenticado, rol, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook personalizado para usar el contexto fácilmente
export const useAuth = () => useContext(AuthContext);