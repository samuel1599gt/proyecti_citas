import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaArrowRight, FaStar, FaTrashAlt } from 'react-icons/fa';


// Endpoints de la API (deben coincidir con las rutas del backend corregidas)
const API_CITAS_ME = 'http://127.0.0.1:8000/citas/me/';
const API_CITAS_DELETE = 'http://127.0.0.1:8000/citas/'; // Base para DELETE /citas/{id}

function HistorialPage() {
    const navigate = useNavigate();
    const [citas, setCitas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchCitas();
    }, []);

    // ----------------------------------------------------
    // FUNCIÓN PARA CARGAR LAS CITAS DEL USUARIO
    // ----------------------------------------------------
    const fetchCitas = async () => {
        setLoading(true);
        setError('');
        const token = localStorage.getItem('access_token');

        if (!token) {
            setError('Error de autenticación. Por favor, inicia sesión.');
            navigate('/login');
            return;
        }

        try {
            const response = await fetch(API_CITAS_ME, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setCitas(data);
            } else if (response.status === 401) {
                setError('Sesión expirada. Por favor, inicia sesión de nuevo.');
                navigate('/login');
            } else {
                // Intenta leer el error detallado del backend
                const errorData = await response.json();
                setError(errorData.detail || 'Fallo al cargar el historial de citas.');
            }
        } catch (err) {
            setError('Error de conexión con el servidor.');
        } finally {
            setLoading(false);
        }
    };

    // ----------------------------------------------------
    // FUNCIÓN PARA ELIMINAR UNA CITA (¡CONFIRMACIÓN AÑADIDA!)
    // ----------------------------------------------------
    const handleDelete = async (citaId) => {
        
        // 🚨 CAMBIO CLAVE: Solicitud de confirmación
        const isConfirmed = window.confirm("¿Estás seguro de que quieres eliminar esta cita? Esta acción es irreversible.");
        
        if (!isConfirmed) {
            return; // Detiene la ejecución si el usuario cancela
        }

        const token = localStorage.getItem('access_token');
        setLoading(true);

        try {
            const response = await fetch(`${API_CITAS_DELETE}${citaId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            // El backend devuelve 200 OK con un cuerpo, o 404/403 con error.
            if (response.ok) {
                alert("Cita eliminada exitosamente.");
                // Volver a cargar la lista de citas para actualizar la tabla
                fetchCitas(); 
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Fallo al eliminar la cita.');
                setLoading(false);
            }
        } catch (err) {
            setError('Error de conexión al intentar eliminar la cita.');
            setLoading(false);
        }
    };

    // ----------------------------------------------------
    // FUNCIONES DE NAVEGACIÓN
    // ----------------------------------------------------
    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login');
    };

    const handleGoToDashboard = () => {
        navigate('/dashboard'); 
    };
    
    // Función de utilidad para renderizar las listas (Sintomas, Zonas, Condiciones)
    const renderListContent = (list) => {
        // Asegura que si la lista es nula o vacía, se muestre 'NINGUNA'
        if (!list || list.length === 0 || (list.length === 1 && list[0] === "")) return 'NINGUNA';
        return list.join('\n'); // Usa salto de línea para formatear en la celda
    };

    if (loading && citas.length === 0) {
        return <div className="historial-page-container">Cargando historial...</div>;
    }

    return (
        <div className="historial-page-container">
            
            {/* Header y Botón Salir */}
            <div className="historial-header">
                <h1 className="historial-title">Historial de Citas</h1>
                <button className="logout-button" onClick={handleLogout}>
                    Salir <FaArrowRight />
                </button>
            </div>

            {error && <p className="error-message">{error}</p>}
            
            {/* Tabla de Citas */}
            <div className="citas-table-wrapper">
                {citas.length === 0 ? (
                    <p className="no-citas">No tienes citas agendadas aún.</p>
                ) : (
                    <table className="citas-table">
                        <thead>
                            <tr>
                                <th>id</th>
                                <th>Síntomas</th>
                                <th>Zona Afectada</th>
                                <th>Condiciones Previas</th>
                                <th>Tiempo con Síntomas</th>
                                <th>Edad</th>
                                <th>Sexo</th>
                                <th>Categoría</th>
                                <th>Acción</th>
                            </tr>
                        </thead>
                        <tbody>
                            {citas.map((cita) => (
                                <tr key={cita.id} className={cita.prioridad?.toLowerCase().includes('urgente') ? 'cita-urgente' : ''}>
                                    <td>{cita.id}</td>
                                    {/* Usamos la función de renderizado para manejar el formato */}
                                    <td style={{ whiteSpace: 'pre-wrap' }}>{renderListContent(cita.sintomas)}</td>
                                    <td style={{ whiteSpace: 'pre-wrap' }}>{renderListContent(cita.zona_afectada)}</td>
                                    <td style={{ whiteSpace: 'pre-wrap' }}>{renderListContent(cita.condiciones_previas)}</td>
                                    
                                    <td>{cita.tiempo_sintomas} días</td>
                                    <td>{cita.edad}</td>
                                    <td>{cita.sexo}</td>
                                    
                                    <td className="prioridad-cell">
                                        {cita.prioridad}
                                        {/* Muestra la estrella si la prioridad es 'Emergencia' o 'Prioritario' */}
                                        {(cita.prioridad?.toLowerCase().includes('emergencia') || cita.prioridad?.toLowerCase().includes('prioritario')) && 
                                            <FaStar className="star-icon" />
                                        }
                                    </td>
                                    <td>
                                        <button 
                                            className="delete-button" 
                                            onClick={() => handleDelete(cita.id)}
                                            disabled={loading}
                                        >
                                            <FaTrashAlt /> Eliminar
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
            
            {/* Botón Volver al Inicio */}
            <div className="historial-footer">
                <button className="back-button" onClick={handleGoToDashboard}>
                    Regresar <FaArrowRight />
                </button>
            </div>
            
        </div>
    );
}

export default HistorialPage;