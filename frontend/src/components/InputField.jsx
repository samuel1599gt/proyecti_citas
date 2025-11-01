import React from "react";

const InputField = ({ id, name, type = "text", value, onChange, placeholder, icon }) => {
  return (
    <div className="flex items-center bg-azulito rounded-lg p-3 mb-4">
      {icon && <span className="mr-3 text-rey text-xl">{icon}</span>}
      <div className="flex-1">
        {/* label con sr-only para accesibilidad (lectores de pantalla) */}
        <label htmlFor={id} className="sr-only">{placeholder}</label>
        <input
          id={id}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="bg-transparent outline-none w-full text-rey placeholder-crema font-never"
        />
      </div>
    </div>
  );
};

export default InputField;
