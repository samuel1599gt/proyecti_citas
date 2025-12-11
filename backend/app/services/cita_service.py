from sqlalchemy.orm import Session
import joblib 
import os 
import pandas as pd 
import numpy as np
from fastapi import HTTPException, status
from app.schemas.cita_schema import CitaBase, CitaCreate # Asegúrate de que CitaCreate sea consistente
from app.models.cita_model import Cita
from typing import List 
from app.schemas.cita_schema import CitaOut

# Mapeo de la salida del modelo a texto (basado en el análisis)
PRIORIDAD_MAP = {
    0: "Normal",
    1: "Prioritario",
    2: "Emergencia"
}

# ----------------------------------------------------
# CONFIGURACIÓN Y CARGA DEL MODELO (Solo una vez)
# ----------------------------------------------------

# Rutas de los archivos
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml')
MODEL_PATH = os.path.join(MODEL_DIR, 'model_sin_fuga.joblib')

MODELO_ML = None
try:
    MODELO_ML = joblib.load(MODEL_PATH)
    print("Modelo de ML cargado exitosamente.")
except Exception as e:
    print(f"ERROR FATAL: No se pudo cargar el modelo de ML en: {MODEL_PATH}. {e}")


# ----------------------------------------------------
# NOMBRES DE COLUMNAS ESPERADAS POR EL MODELO
# ----------------------------------------------------
# Nota: La columna en el DF debe ser 'tiempo_sintomas' si así lo entrenaste
COLUMNAS_MODELO = [
    'Edad', 'Tiempo_Sintomas_dias', 'sexo_binario', 'Zona_Cabeza', 'Zona_Pecho', 
    'Zona_Abdomen', 'Zona_Garganta', 'Zona_Piernas', 'Zona_Brazos', 'Zona_Espalda', 
    'Zona_Estómago', 'Zona_Corazón', 'Zona_Pulmones', 'Zona_Ninguna', 
    'Sintoma_Fiebre', 'Sintoma_Dolor', 'Sintoma_Mareo', 'Sintoma_Tos', 'Sintoma_Náuseas', 
    'Sintoma_Inflamación', 
    'Sintoma_Dificultad_respiratoria', 
    'Sintoma_Cansancio', 
    'Sintoma_Escalofríos', 'Sintoma_Vómito', 'Sintoma_Ninguno', 
    'Cond_Hipertensión', 'Cond_Cardiaco', 'Cond_Diabetes', 'Cond_Asma', 'Cond_Obesidad', 
    'Cond_Artritis', 'Cond_Migraña', 'Cond_Alergias', 'Cond_Epilepsia', 
    'Cond_Colesterol_alto', 
    'Cond_Ninguna'
]


# ----------------------------------------------------
# FUNCIÓN DE PREPROCESAMIENTO Y CLASIFICACIÓN
# ----------------------------------------------------

def _normalize_name(name: str) -> str:
    """Convierte el nombre a minúsculas y reemplaza espacios por guiones bajos para coincidir con las columnas."""
    return name.lower().replace(" ", "_")

def clasificar_prioridad(data: CitaBase):
    """
    Transforma los datos del cuestionario en el formato esperado por el modelo ML 
    y predice la prioridad de la cita.
    """
    if MODELO_ML is None:
        print("ADVERTENCIA: Modelo ML no disponible. Asignando prioridad 'Normal'.")
        return PRIORIDAD_MAP[0] 

    input_df = pd.DataFrame(np.zeros((1, len(COLUMNAS_MODELO))), columns=COLUMNAS_MODELO)

    # 1. ESCALADO DE VARIABLES NUMÉRICAS
    # Normalización de Edad: Asumiendo rango (1-100)
    input_df['Edad'] = (data.edad - 1) / (100 - 1) 
    
    # 🚨 CORRECCIÓN CRÍTICA: Usar data.tiempo_sintomas
    # Normalización de Tiempo con Síntomas: Asumiendo rango (0-30)
    input_df['Tiempo_Sintomas_dias'] = data.tiempo_sintomas / 30 
    
    # 2. CODIFICACIÓN BINARIA (sexo)
    input_df['sexo_binario'] = 1 if data.sexo.lower() == 'male' else 0 
    
    # 3. ONE-HOT ENCODING DE LISTAS DE OPCIONES
    
    # Zonas afectadas
    for zona in data.zona_afectada:
        # 🚨 ROBUSTEZ: Limpieza del nombre para coincidir (ej: 'Cabeza' -> 'zona_cabeza')
        normalized_zona = _normalize_name(zona)
        if normalized_zona == 'ninguna':
            input_df['Zona_Ninguna'] = 1
        else:
            col_name = f'Zona_{normalized_zona}'.capitalize() # Mantiene la mayúscula inicial para coincidir con COLUMNAS_MODELO
            if col_name in input_df.columns:
                 input_df[col_name] = 1

    # Síntomas
    for sintoma in data.sintomas:
        normalized_sintoma = _normalize_name(sintoma)
        if normalized_sintoma == 'ninguna':
            input_df['Sintoma_Ninguno'] = 1
        else:
            col_name = f'Sintoma_{normalized_sintoma}'.capitalize()
            if col_name in input_df.columns:
                 input_df[col_name] = 1

    # Condiciones Previas
    if data.condiciones_previas:
        for cond in data.condiciones_previas:
            normalized_cond = _normalize_name(cond)
            if normalized_cond == 'ninguna':
                input_df['Cond_Ninguna'] = 1
            else:
                col_name = f'Cond_{normalized_cond}'.capitalize()
                if col_name in input_df.columns:
                    input_df[col_name] = 1

    # 4. Predicción
    prioridad_int = MODELO_ML.predict(input_df[COLUMNAS_MODELO])[0]
    
    return PRIORIDAD_MAP.get(prioridad_int, "Normal")


# ----------------------------------------------------
# FUNCIÓN CREAR CITA (Corregida la llamada al ML)
# ----------------------------------------------------

def crear_cita(data: CitaBase, user_id: int, db: Session): 
    
    prioridad = "Sin Clasificar" 

    # 1. CLASIFICAR LA CITA USANDO EL MODELO DE ML
    try:
        prioridad = clasificar_prioridad(data) # 🎯 DESCOMENTADO: Ahora llama a la clasificación
    except Exception as e:
        print(f"Error durante la clasificación ML (Asignando Normal): {e}")
        prioridad = "Normal" 

    # 2. CREAR EL OBJETO CITA CON LA PRIORIDAD OBTENIDA
    # Los datos de lista se convierten a string para guardarse en la DB
    condiciones_str = ", ".join(data.condiciones_previas) if data.condiciones_previas else None

    try:
        nueva_cita = Cita(
            user_id=user_id,
            sintomas=", ".join(data.sintomas), 
            zona_afectada=", ".join(data.zona_afectada), 
            condiciones_previas=condiciones_str, 
            tiempo_sintomas=data.tiempo_sintomas, 
            edad=data.edad,
            sexo=data.sexo,
            prioridad=prioridad 
        )

        db.add(nueva_cita)
        db.commit()
        db.refresh(nueva_cita)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al guardar la cita en la base de datos: {e}")
    
    # 3. CONVERTIR LOS CAMPOS DE STRING A LISTA PARA LA SALIDA Pydantic (CitaOut)
    # Ya lo hace el ORM por referencia, pero se repite para claridad.
    nueva_cita.sintomas = nueva_cita.sintomas.split(", ") if nueva_cita.sintomas else []
    nueva_cita.zona_afectada = nueva_cita.zona_afectada.split(", ") if nueva_cita.zona_afectada else []
    nueva_cita.condiciones_previas = nueva_cita.condiciones_previas.split(", ") if nueva_cita.condiciones_previas else []

    return nueva_cita


# ----------------------------------------------------
# FUNCIÓN OBTENER CITAS (Lista)
# ----------------------------------------------------

# backend/app/services/cita_service.py

# ... (código anterior) ...

def obtener_citas(user_id: int, db: Session) -> List[Cita]:
    """
    Obtiene la lista de citas para un usuario específico, 
    convirtiendo los campos de string a lista para la respuesta Pydantic.
    """
    citas_orm = db.query(Cita).filter(Cita.user_id == user_id).order_by(Cita.fecha_solicitud.desc()).all()

    # Revertir la conversión de string a lista para cada cita devuelta
    for cita in citas_orm:
        # 🚨 CORRECCIÓN CRÍTICA: Si el valor es None/vacio, debe ser una lista vacía []
        cita.sintomas = cita.sintomas.split(", ") if cita.sintomas else []
        
        # 🚨 CORRECCIÓN CRÍTICA: Si el valor es None/vacio, debe ser una lista vacía []
        cita.zona_afectada = cita.zona_afectada.split(", ") if cita.zona_afectada else []
        
        # Este ya lo teníamos bien, pero se revisa por consistencia:
        cita.condiciones_previas = cita.condiciones_previas.split(", ") if cita.condiciones_previas else []

    return citas_orm


# ----------------------------------------------------
# FUNCIÓN CANCELAR CITA (Eliminar)
# ----------------------------------------------------

def cancelar_cita(cita_id: int, user_id: int, db: Session) -> bool:
    """
    Cancela (elimina) una cita específica de la base de datos, 
    verificando que el usuario sea el propietario de la misma.
    """
    cita = db.query(Cita).filter(Cita.id == cita_id).first()

    # 1. Verificar si la cita existe
    if not cita:
        # Se levanta la excepción para que la ruta DELETE devuelva 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cita con ID {cita_id} no encontrada.")

    # 2. Verificar la propiedad (seguridad)
    if cita.user_id != user_id:
        # Se levanta la excepción para que la ruta DELETE devuelva 403
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para cancelar esta cita.")

    # 3. Eliminar la cita
    db.delete(cita)
    db.commit()

    return True # Devuelve True si la cancelación fue exitosa