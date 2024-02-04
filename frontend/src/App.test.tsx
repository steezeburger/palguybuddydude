import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders initial page', () => {
  render(<App />);
  const elem = screen.getByText(/nice/i);
  expect(elem).toBeInTheDocument();
});
