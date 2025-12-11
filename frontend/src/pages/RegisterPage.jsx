import React, { useState } from 'react';
import { FaUser, FaLock } from 'react-icons/fa';
import { MdEmail } from 'react-icons/md';
import { Link, useNavigate } from 'react-router-dom';

// URL de tu backend de FastAPI
const API_REGISTER_URL = 'http://127.0.0.1:8000/auth/register'; 

// REQUISITOS MÍNIMOS DE VALIDACIÓN
const MIN_LENGTH_NAME = 5;
const MIN_LENGTH_PASSWORD = 8;

// DEFINICIÓN DEL INPUT REUTILIZABLE
const StyledInput = ({ icon: Icon, placeholder, name, type = 'text', value, onChange, error }) => (
  <div className="input-container">
    <div className="icon-wrapper" style={{ color: error ? 'var(--title-color)' : '' }}>
      <Icon />
    </div>
    <input
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="styled-input"
      required
    />
    {/* Mostrar mensaje de error debajo del input si existe */}
    {error && <p className="input-error-message">{error}</p>} 
  </div>
);


function RegisterPage() {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    correo: '',
    password: '',
    confirmPassword: '',
  });

  const [validationErrors, setValidationErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  const [apiSuccess, setApiSuccess] = useState('');

  // Función para validar campos individuales o todo el formulario
  const validateField = (name, value) => {
    let error = '';

    if (name === 'nombre' && value.length > 0 && value.length < MIN_LENGTH_NAME) {
      error = `El nombre debe tener al menos ${MIN_LENGTH_NAME} caracteres.`;
    }
    if (name === 'apellido' && value.length > 0 && value.length < MIN_LENGTH_NAME) {
      error = `El apellido debe tener al menos ${MIN_LENGTH_NAME} caracteres.`;
    }
    if (name === 'password' && value.length > 0 && value.length < MIN_LENGTH_PASSWORD) {
      error = `La contraseña debe tener al menos ${MIN_LENGTH_PASSWORD} caracteres.`;
    }
    if (name === 'correo' && value.length > 0 && !/\S+@\S+\.\S+/.test(value)) {
        error = 'Formato de correo electrónico no válido.';
    }
    
    // Actualiza solo el error del campo actual para la visualización en tiempo real
    setValidationErrors(prev => ({ ...prev, [name]: error }));
    return error === '';
  };

  const validateAll = () => {
    let isValid = true;
    const errors = {};
    let allFieldsFilled = true;

    // 1. Validar campos individuales y requeridos
    Object.keys(formData).forEach(key => {
        // Validación de campos vacíos
        if (!formData[key]) {
            errors[key] = 'Este campo es obligatorio.';
            allFieldsFilled = false;
        }

        // Validación de formato (re-ejecutamos con la función de validación de campo)
        const fieldError = validateField(key, formData[key]);
        if (fieldError !== true) { // Si validateField retorna una cadena de error o false
             errors[key] = errors[key] || fieldError; // Prioriza el error de campo vacío
             isValid = false;
        }
    });

    // 2. Validación de confirmación de contraseña
    if (formData.password !== formData.confirmPassword) {
        errors.confirmPassword = 'Las contraseñas no coinciden.';
        isValid = false;
    }
    
    setValidationErrors(errors);
    return isValid && allFieldsFilled;
  };

  // Función para manejar cambios en los inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Validar en tiempo real
    validateField(name, value);
  };

  // Función para manejar el envío y la conexión al Backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    setApiSuccess('');

    // 1. VALIDACIÓN LOCAL COMPLETA
    if (!validateAll()) {
      console.log("Envío cancelado debido a fallos en la validación local.");
      return; 
    }

    console.log("Validación local OK. Enviando a la API...");
    setLoading(true);

    try {
      const response = await fetch(API_REGISTER_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nombre: formData.nombre,
          apellido: formData.apellido,
          correo: formData.correo,
          password: formData.password,
          password_repeat: formData.confirmPassword, 
        }),
      });

      if (response.ok) {
        setApiSuccess('¡Registro exitoso! Redirigiendo a Iniciar Sesión...');
        setTimeout(() => navigate('/login'), 2000); 
      } else {
        const errorData = await response.json();
        console.error("Error de API:", errorData);
        // Manejo específico del error 422
        if (response.status === 422 && errorData.detail) {
             const validationDetail = errorData.detail[0].msg || 'Datos de registro inválidos.';
             setApiError(validationDetail);
        } else {
            setApiError(errorData.detail || 'Fallo en el registro. Intenta con otro correo o revisa tus datos.');
        }
      }
    } catch (err) {
      console.error("Error de conexión:", err);
      setApiError('Error de conexión. Asegúrate de que el servidor (FastAPI) esté activo en el puerto 8000.');
    } finally {
      setLoading(false);
    }
  };

  // Renderizado del formulario
  return (
    <div className="register-page-container">
      <h1 className="register-title">REGISTRO</h1>
      
      <form className="register-form" onSubmit={handleSubmit}>
        
        <StyledInput 
          icon={FaUser} 
          placeholder="Nombre" 
          name="nombre" 
          value={formData.nombre} 
          onChange={handleChange} 
          error={validationErrors.nombre}
        />
        
        <StyledInput 
          icon={FaUser} 
          placeholder="Apellido" 
          name="apellido" 
          value={formData.apellido} 
          onChange={handleChange} 
          error={validationErrors.apellido}
        />
        
        <StyledInput 
          icon={MdEmail} 
          placeholder="ejemplo@tucorreo.com" 
          name="correo" 
          type="email"
          value={formData.correo} 
          onChange={handleChange} 
          error={validationErrors.correo}
        />
        
        <StyledInput 
          icon={FaLock} 
          placeholder={`Mínimo ${MIN_LENGTH_PASSWORD} caracteres`} 
          name="password" 
          type="password"
          value={formData.password} 
          onChange={handleChange} 
          error={validationErrors.password}
        />
        
        <StyledInput 
          icon={FaLock} 
          placeholder="Confirma tu contraseña" 
          name="confirmPassword" 
          type="password"
          value={formData.confirmPassword} 
          onChange={handleChange} 
          error={validationErrors.confirmPassword}
        />
        
        {/* Mensajes de estado (Errores de API) */}
        {apiError && <p className="error-message">{apiError}</p>}
        {apiSuccess && <p className="success-message">{apiSuccess}</p>}
        
        {/* Botón de Registro */}
        <button 
            type="submit" 
            className="register-button" 
            disabled={loading || Object.values(validationErrors).some(e => e)}
        >
          {loading ? 'Registrando...' : 'Registrarse'}
        </button>
      </form>

      {/* Enlace para Iniciar Sesión */}
        <p className="login-link">
           ¿Ya tienes cuenta? 
           <Link to="/login">Iniciar Sesión</Link>
        </p>

    </div>
  );
}

export default RegisterPage;