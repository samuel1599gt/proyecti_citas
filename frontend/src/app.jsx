// frontend/src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'; 
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AgendaPage from './pages/AgendaPage';
import HistorialPage from './pages/HistorialPage'; // 

// Componente para proteger las rutas (se mantiene igual)
const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        // Redirige al login si no hay token
        return <Navigate to="/login" replace />; 
    }
    return children;
};

function App() {
  return (
    <Router>
      <Routes>
        
        {/* Rutas Públicas (Login/Registro) */}
        <Route path="/" element={<RegisterPage />} /> 
        <Route path="/login" element={<LoginPage />} /> 
        
        {/* Rutas Privadas (Requieren autenticación) */}
        
        {/* RUTA DE DASHBOARD (PÁGINA PRINCIPAL) */}
        <Route 
            path="/dashboard" 
            element={
                <ProtectedRoute>
                    <DashboardPage />
                </ProtectedRoute>
            } 
        />
        
        {/* RUTA DE AGENDAR CITA */}
        <Route 
            path="/agenda" 
            element={
                <ProtectedRoute>
                    <AgendaPage />
                </ProtectedRoute>
            } 
        />
        
        {/* 🎯 RUTA DE HISTORIAL DE CITAS (NUEVA) */}
        <Route 
            path="/historial" 
            element={
                <ProtectedRoute>
                    <HistorialPage /> 
                </ProtectedRoute>
            } 
        />
        
        <Route path="*" element={<h1>404: Página no encontrada</h1>} />
      </Routes>
    </Router>
  );
}

export default App;