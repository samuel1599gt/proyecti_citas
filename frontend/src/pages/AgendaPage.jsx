import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaArrowRight } from 'react-icons/fa';

// URL de la API de Citas (DEBE coincidir con el prefix del router: /citas)
const API_AGENDA_CITA = 'http://127.0.0.1:8000/citas/';

// --- Datos Fijos del Formulario ---
const ZONAS = ['Cabeza', 'Pecho', 'Abdomen', 'Garganta', 'Piernas', 'Brazos', 'Espalda', 'Estómago', 'Corazón', 'Pulmones', 'NINGUNA'];
const SINTOMAS = ['Fiebre', 'Dolor', 'Mareo', 'Tos', 'Náuseas', 'Inflamación', 'Dificultad Respiratoria', 'Cansancio', 'Escalofríos', 'Vómito', 'NINGUNA'];
const CONDICIONES = ['Hipertensión', 'Cardiaco', 'Diabetes', 'Obesidad', 'Artritis', 'Asma', 'Migraña', 'Alergias', 'Epilepsia', 'Colesterol Alto', 'NINGUNA'];

// Componente para Checkbox Groups (Se mantiene igual, funciona correctamente)
const CheckboxGroup = ({ title, options, state, setState, maxSelection = 3 }) => {
    const isNoneSelected = state.includes('NINGUNA');

    const handleCheck = (option) => {
        if (option === 'NINGUNA') {
            setState(isNoneSelected ? [] : ['NINGUNA']);
            return;
        }

        if (isNoneSelected) {
            setState([option]);
            return;
        }

        if (state.includes(option)) {
            setState(state.filter(item => item !== option));
        } else if (state.length < maxSelection) {
            setState([...state, option]);
        } else {
            console.warn(`Máximo de ${maxSelection} opciones alcanzado para ${title}.`);
        }
    };

    return (
        <div className="form-group-card">
            <h3 className="form-card-title">{title}</h3>
            <div className="checkbox-grid">
                {options.map(option => (
                    <label key={option} className="checkbox-label">
                        <input
                            type="checkbox"
                            checked={state.includes(option)}
                            onChange={() => handleCheck(option)}
                            disabled={option !== 'NINGUNA' && isNoneSelected}
                        />
                        {option}
                    </label>
                ))}
            </div>
        </div>
    );
};


function AgendaPage() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    
    // Estados para los Checkbox
    const [zonaAfectada, setZonaAfectada] = useState([]);
    const [sintomas, setSintomas] = useState([]);
    const [condicionesPrevias, setCondicionesPrevias] = useState([]);

    // Estados para Selectors y Radio: Usamos '' para que el selector 'disabled' funcione
    const [tiempoSintomas, setTiempoSintomas] = useState('');
    const [edad, setEdad] = useState('');
    const [sexo, setSexo] = useState('');
    
    // Generar opciones de 0 a 30 (Tiempo) y 0 a 100 (Edad)
    const timeOptions = Array.from({ length: 31 }, (_, i) => i);
    const ageOptions = Array.from({ length: 101 }, (_, i) => i);


    // Función para regresar al Dashboard (usa el estilo .logout-button)
    const handleGoToDashboard = () => {
        navigate('/dashboard'); 
    };

    const validateForm = () => {
        
        // 🚨 CORRECCIÓN CRÍTICA: La validación ahora comprueba si el valor es "" (cadena vacía)
        // Esto permite que el valor "0" (cero días o cero años) sea considerado válido.
        if (tiempoSintomas === '' || edad === '' || sexo === '') {
            setError('Por favor, selecciona una opción para Tiempo, Edad y Sexo.');
            return false;
        }

        if (zonaAfectada.length === 0 || sintomas.length === 0 || condicionesPrevias.length === 0) {
            setError('Debes seleccionar al menos una opción (o NINGUNA) en cada grupo de síntomas y condiciones.');
            return false;
        }

        const checkMax = (list) => {
            // Verifica que el número de elementos que NO son 'NINGUNA' sea <= 3
            return list.filter(item => item !== 'NINGUNA').length <= 3;
        };

        if (!checkMax(zonaAfectada) || !checkMax(sintomas) || !checkMax(condicionesPrevias)) {
            setError('El límite máximo de opciones seleccionadas es 3 por categoría.');
            return false;
        }
        
        setError('');
        return true;
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        setSuccess('');

        if (!validateForm()) {
            return;
        }

        setLoading(true);
        
        // 1. Construcción del objeto de datos
        const appointmentData = {
            // Aseguramos la conversión a Int, pero ya sabemos que no será ""
            tiempo_sintomas: parseInt(tiempoSintomas), 
            edad: parseInt(edad),
            sexo: sexo,
            
            // Los arrays vacíos o con solo 'NINGUNA' se convertirán a "" (string vacío)
            zona_afectada: zonaAfectada.filter(z => z !== 'NINGUNA').join(','),
            sintomas: sintomas.filter(s => s !== 'NINGUNA').join(','),
            condiciones_previas: condicionesPrevias.filter(c => c !== 'NINGUNA').join(','),
        };

        // 🚨 DEBUG: Imprimir la carga para ver la combinación que falla
        console.log("Carga de datos enviada:", appointmentData); 


        // 2. Activación de la llamada a la API con el token
        try {
            const token = localStorage.getItem('access_token');
            
            if (!token) {
                setError('Error de autenticación. Por favor, inicia sesión de nuevo.');
                navigate('/login');
                return;
            }

            const response = await fetch(API_AGENDA_CITA, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(appointmentData),
            });
            
            if (response.ok) {
                const data = await response.json();
                setSuccess(`¡Cita agendada con éxito! ID: ${data.id}`);
                setError('');
                // Opcional: limpiar el formulario después del éxito
                setZonaAfectada([]);
                setSintomas([]);
                setCondicionesPrevias([]);
                setTiempoSintomas('');
                setEdad('');
                setSexo('');

            } else {
                const errorData = await response.json();
                
                // 🚨 Captura el error 422 de Pydantic y lo formatea
                let errorMessage = errorData.detail || 'Fallo al agendar la cita. Verifica el estado del servidor.';
                
                if (Array.isArray(errorData.detail) && response.status === 422) {
                     // Formatea los errores de validación de Pydantic
                     errorMessage = "Error de validación: " + errorData.detail.map(err => 
                         `${err.loc.join('->')}: ${err.msg}`
                     ).join(' | ');
                }
                
                setError(errorMessage);
            }
        } catch (err) {
            setError('Error de conexión con el servidor. Verifica que FastAPI esté activo.');
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="agenda-page-container">
            <div className="agenda-header">
                <h1 className="agenda-title">Agenda tu Cita</h1>
                
                <button 
                    className="logout-button" 
                    onClick={handleGoToDashboard} 
                >
                    Regresar al Dashboard <FaArrowRight />
                </button>
                
            </div>
            
            <form onSubmit={handleSubmit} className="agenda-form">
                
                <div className="form-grid">
                    
                    {/* COLUMNA IZQUIERDA */}
                    <div className="grid-column">
                        <CheckboxGroup
                            title="Zona Afectada"
                            options={ZONAS}
                            state={zonaAfectada}
                            setState={setZonaAfectada}
                        />
                        
                        <CheckboxGroup
                            title="Condiciones Previas"
                            options={CONDICIONES}
                            state={condicionesPrevias}
                            setState={setCondicionesPrevias}
                            maxSelection={3}
                        />
                    </div>
                    
                    {/* COLUMNA DERECHA */}
                    <div className="grid-column">
                        <CheckboxGroup
                            title="Síntomas"
                            options={SINTOMAS}
                            state={sintomas}
                            setState={setSintomas}
                        />

                        {/* Tiempo con los Síntomas (0-30) */}
                        <div className="form-group-card selector-card">
                            <h3 className="form-card-title">Tiempo con los Síntomas</h3>
                            <select 
                                value={tiempoSintomas} 
                                onChange={(e) => setTiempoSintomas(e.target.value)}
                                className="styled-select"
                                required
                            >
                                <option value="" disabled>Seleccionar días</option>
                                {timeOptions.map(t => (
                                    <option key={t} value={t}>{t} días</option>
                                ))}
                            </select>
                        </div>
                        
                        {/* Edad (0-100) */}
                        <div className="form-group-card selector-card">
                            <h3 className="form-card-title">Edad</h3>
                            <select 
                                value={edad} 
                                onChange={(e) => setEdad(e.target.value)}
                                className="styled-select"
                                required
                            >
                                <option value="" disabled>Seleccionar edad</option>
                                {ageOptions.map(a => (
                                    <option key={a} value={a}>{a} años</option>
                                ))}
                            </select>
                        </div>
                        
                        {/* Sexo (Male/Female) */}
                        <div className="form-group-card selector-card">
                            <h3 className="form-card-title">Sexo</h3>
                            <select 
                                value={sexo} 
                                onChange={(e) => setSexo(e.target.value)}
                                className="styled-select"
                                required
                            >
                                <option value="" disabled>Seleccionar sexo</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Mensajes y Botón de Envio */}
                <div className="form-footer">
                    {error && <p className="error-message">{error}</p>}
                    {success && <p className="success-message">{success}</p>}
                    
                    <button type="submit" className="submit-agenda-button" disabled={loading}>
                        {loading ? 'Agendando...' : (
                            <>
                                Agendar Cita <FaArrowRight style={{ marginLeft: '10px' }} />
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}

export default AgendaPage;