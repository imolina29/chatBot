import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ProductoForm from '../../../frontend/src/components/ProductoForm';
import '@testing-library/jest-dom/extend-expect';

describe('ProductoForm', () => {
  test('renderiza el formulario correctamente', () => {
    render(<ProductoForm />);

    expect(screen.getByPlaceholderText('Descripción')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Cantidad')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Valor Unitario')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Valor Venta')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Categoría')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Stock')).toBeInTheDocument();
    expect(screen.getByText('Guardar')).toBeInTheDocument();
  });

  test('permite escribir en los campos', () => {
    render(<ProductoForm />);

    const descripcionInput = screen.getByPlaceholderText('Descripción');
    fireEvent.change(descripcionInput, { target: { value: 'Producto de prueba' } });
    expect(descripcionInput.value).toBe('Producto de prueba');
  });
});