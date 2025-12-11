import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // <-- ¡AÑADIDA useNavigate!
// Importa íconos
import { FaLock } from 'react-icons/fa';
import { MdEmail, MdLogin } from 'react-icons/md';

// URL del endpoint de Login de tu Backend (FastAPI)
const API_LOGIN_URL = 'http://127.0.0.1:8000/auth/login'; 

// Componente de Input Reutilizable (MOVIDO FUERA DE LA FUNCIÓN PRINCIPAL para optimización)
const StyledInput = ({ icon: Icon, placeholder, name, type = 'text', value, onChange }) => (
  <div className="input-container">
    <div className="icon-wrapper">
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
  </div>
);

function LoginPage() {
  // Inicializamos la función de navegación
  const navigate = useNavigate(); 
    
  const [formData, setFormData] = useState({
    correo: '',
    password: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Función para manejar el envío y obtener el token JWT
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // *** INICIO DE LA CORRECCIÓN ***
      
      // 1. Enviar los datos como JSON
      const loginPayload = {
        // La clave debe ser 'correo' (como espera UserLogin), NO 'username'
        correo: formData.correo, 
        password: formData.password,
      };

      const response = await fetch(API_LOGIN_URL, {
        method: 'POST',
        headers: {
          // 2. Cambiar el Content-Type a application/json
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify(loginPayload), // 3. Serializar el objeto JSON
      });
      
      // *** FIN DE LA CORRECCIÓN ***


      if (response.ok) {
        const data = await response.json();
        
        // 1. Guardar el token para futuras peticiones
        localStorage.setItem('access_token', data.access_token);
        
        // 2. Redirigir al usuario al dashboard
        console.log('Login exitoso. Token obtenido:', data.access_token);
        navigate('/dashboard'); // <-- ¡REDIRECCIÓN CLAVE!
        
      } else {
        const errorData = await response.json();
        // Muestra el error del backend (ej: Credenciales incorrectas)
        setError(errorData.detail || 'Error de inicio de sesión. Credenciales incorrectas.');
      }
    } catch (err) {
      setError('Error de conexión con el servidor. Verifica que FastAPI esté activo.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="register-page-container"> 
      <h1 className="register-title">INICIAR SESIÓN</h1>
      
      <form className="register-form" onSubmit={handleSubmit}>
        
        {/* Correo */}
        <StyledInput 
          icon={MdEmail} 
          placeholder="ejemplo@tucorreo.com" 
          name="correo" 
          type="email"
          value={formData.correo} 
          onChange={handleChange} 
        />
        
        {/* Contraseña */}
        <StyledInput 
          icon={FaLock} 
          placeholder="Tu contraseña segura aquí********" 
          name="password" 
          type="password"
          value={formData.password} 
          onChange={handleChange} 
        />
        
        {/* Mensaje de error */}
        {error && <p className="error-message">{error}</p>}

        {/* Botón Aceptar (Login) */}
        <button type="submit" className="login-button" disabled={loading}>
          {loading ? 'Verificando...' : (
            <>
              Aceptar <MdLogin style={{ marginLeft: '5px' }} />
            </>
          )}
        </button>
      </form>

      {/* Enlace de Registro (usa Link para navegar a la ruta raíz '/') */}
        <p className="login-register-link">
          No tengo cuenta, deseo registrarme 
          <Link to="/" style={{ marginLeft: '15px' }}>&rarr;</Link>
        </p>
    </div>
  );
}

export default LoginPage;