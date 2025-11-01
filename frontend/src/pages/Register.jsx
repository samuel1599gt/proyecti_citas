// src/pages/Register.jsx
import React, { useState } from "react";
import InputField from "../components/InputField";
import { register as apiRegister } from "../services/authService";
import { useNavigate } from "react-router-dom";
import candadoIcon from "../assets/iconos/candado.svg";
import mailIcon from "../assets/iconos/mail.svg";
import userIcon from "../assets/iconos/user.svg";

const Register = () => {
  const navigate = useNavigate(); // para redirigir después del registro
  const [form, setForm] = useState({
    nombre: "",
    apellido: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [serverError, setServerError] = useState("");

  // actualiza el estado del formulario
  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  // validaciones simples en frontend
  const validate = () => {
    const err = {};
    if (!form.nombre.trim()) err.nombre = "El nombre es requerido";
    if (!form.apellido.trim()) err.apellido = "El apellido es requerido";
    if (!form.email) err.email = "El correo es requerido";
    else {
      // regex simple para email
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!re.test(form.email)) err.email = "Email inválido";
    }
    if (!form.password) err.password = "La contraseña es requerida";
    else if (form.password.length < 8) err.password = "Mínimo 8 caracteres";
    if (form.password !== form.confirmPassword) err.confirmPassword = "Las contraseñas no coinciden";
    return err;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError("");
    const v = validate();
    setErrors(v);
    if (Object.keys(v).length > 0) return; // hay errores -> no enviar

    setLoading(true);
    try {
      // arma el payload según lo que espera el backend
      const payload = {
        nombre: form.nombre,
        apellido: form.apellido,
        email: form.email,
        password: form.password,
      };

      const res = await apiRegister(payload);
      // si backend devuelve token o éxito:
      // localStorage.setItem("token", res.data.token)  // opcional según tu API
      setLoading(false);
      // redirigir a login o dashboard
      navigate("/login", { replace: true });
    } catch (err) {
      setLoading(false);
      // manejo simple de errores del servidor
      if (err?.response?.data?.message) setServerError(err.response.data.message);
      else setServerError("Error en el servidor. Intenta de nuevo.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-lila p-4">
      <div className="bg-crema/80 backdrop-blur-md rounded-2xl shadow-xl p-8 w-full max-w-md">
        {/* Header: logo opcional y título */}
        <div className="mb-6 text-center">
          {/* aquí puedes poner tu logo: src/assets/images/logo.svg */}
          <h1 className="text-3xl font-never font-bold text-rey">Crear cuenta</h1>
          <p className="text-sm text-rey/70 mt-2">Regístrate para agendar tus citas</p>
        </div>

        {/* Mensaje de error del servidor */}
        {serverError && (
          <div className="mb-4 text-sm text-red-600 bg-red-100 p-2 rounded">
            {serverError}
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <InputField
            id="nombre"
            name="nombre"
            type="text"
            value={form.nombre}
            onChange={handleChange}
            placeholder="Nombre"
            icon={<img src={userIcon} alt="user" className="w-5 h-5" />}
          />
          {errors.nombre && <p className="text-xs text-red-600 mb-2">{errors.nombre}</p>}

          <InputField
            id="apellido"
            name="apellido"
            type="text"
            value={form.apellido}
            onChange={handleChange}
            placeholder="Apellido"
            icon={<img src={userIcon} alt="user" className="w-5 h-5"/>}
          />
          {errors.apellido && <p className="text-xs text-red-600 mb-2">{errors.apellido}</p>}

          <InputField
            id="email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            placeholder="Correo electrónico"
            icon={<img src={mailIcon} alt="mail" className="w-5 h-5" />}
          />
          {errors.email && <p className="text-xs text-red-600 mb-2">{errors.email}</p>}

          <InputField
            id="password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Contraseña"
            icon={<img src={candadoIcon} alt="candado" className="w-5 h-5"/>}
          />
          {errors.password && <p className="text-xs text-red-600 mb-2">{errors.password}</p>}

          <InputField
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            value={form.confirmPassword}
            onChange={handleChange}
            placeholder="Confirmar contraseña"
            icon={<img src={candadoIcon} alt="candado" className="w-5 h-5"/>}
          />
          {errors.confirmPassword && <p className="text-xs text-red-600 mb-2">{errors.confirmPassword}</p>}

          <button
            type="submit"
            disabled={loading}
            className={`mt-4 w-full py-3 rounded-lg font-never font-semibold transition ${
              loading ? "bg-rey/60 cursor-not-allowed" : "bg-rey hover:bg-rey/90 text-crema"
            }`}
          >
            {loading ? "Creando cuenta..." : "Registrarme"}
          </button>
        </form>

        {/* Pie: link a login */}
        <div className="mt-4 text-center text-sm text-rey/70">
          ¿Ya tienes cuenta?{" "}
          <button onClick={() => navigate("/login")} className="text-rey underline">
            Iniciar sesión
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;
