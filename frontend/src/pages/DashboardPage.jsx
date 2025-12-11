import React, { useState, useEffect } from 'react';
import { FaUser, FaEnvelope, FaSignOutAlt } from 'react-icons/fa';
import { MdOutlineDateRange, MdHistory } from 'react-icons/md';
import { useNavigate, Link } from 'react-router-dom'; // Para la navegación y enlaces

// URLs de los endpoints de tu Backend
const API_USERS_ME = 'http://127.0.0.1:8000/auth/me';

// Componente para la Tarjeta de Información (Reutiliza el estilo de input)
const InfoCard = ({ icon: Icon, label, value }) => (
    <div className="info-card-container">
        <div className="icon-wrapper">
            <Icon />
        </div>
        <input
            type="text"
            className="info-card-input"
            value={value || label} // Muestra el valor real o un placeholder si está vacío
            readOnly // Los datos de perfil no se editan aquí
        />
    </div>
);

// Componente para los Botones de Acción
const ActionButton = ({ icon: Icon, text, to }) => (
    // Usamos Link para navegar a otras rutas
    <Link to={to} className="action-button">
        {text}
        <Icon className="arrow-icon" />
    </Link>
);


function DashboardPage() {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) {
                // Si no hay token, redirigir al login
                navigate('/login');
                return;
            }

            try {
                const response = await fetch(API_USERS_ME, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`, // Envía el token JWT
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setUserData(data); // Guarda {nombre, apellido, correo}
                } else {
                    // Si el token es inválido o expiró
                    localStorage.removeItem('access_token');
                    navigate('/login');
                }
            } catch (err) {
                setError('Error de conexión al obtener datos del usuario.');
                localStorage.removeItem('access_token');
                navigate('/login');
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login'); // Redirigir al login después de cerrar sesión
    };


    if (loading) {
        return (
            <div className="register-page-container">
                <h1>Cargando perfil...</h1>
            </div>
        );
    }

    if (error) {
        return (
            <div className="register-page-container">
                <h1>Error: {error}</h1>
                <button onClick={() => navigate('/login')}>Ir al Login</button>
            </div>
        );
    }
    
    // Si userData es null (ej. fallo silencioso, aunque ya manejamos la redirección)
    if (!userData) return null;


    return (
        <div className="dashboard-layout">
            
            {/* Columna Izquierda: Perfil y Datos */}
            <div className="profile-section">
                
                <button className="logout-button" onClick={handleLogout}>
                    Salir <FaSignOutAlt />
                </button>
                
                <div className="profile-icon-large">
                    <FaUser />
                </div>
                
                {/* Datos del Usuario */}
                <InfoCard 
                    icon={FaUser} 
                    label="Nombre" 
                    value={userData.nombre} 
                />
                <InfoCard 
                    icon={FaUser} 
                    label="Apellido" 
                    value={userData.apellido} 
                />
                <InfoCard 
                    icon={FaEnvelope} 
                    label="Correo" 
                    value={userData.correo} 
                />
            </div>

            {/* Columna Derecha: Bienvenida y Acciones */}
            <div className="actions-section">
                <h1 className="welcome-title">Bienvenido</h1>
                <h2 className="question-text">¿Qué deseas hacer?</h2>
                
                <div className="action-buttons-container">
                    <ActionButton 
                        icon={MdOutlineDateRange} 
                        text="Agendar Cita" 
                        to="/agenda" 
                    />
                    <ActionButton 
                        icon={MdHistory} 
                        text="Historial de Citas" 
                        to="/historial" 
                    />
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;