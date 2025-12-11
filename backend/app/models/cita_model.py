# backend/app/models/cita_model.py (VERSIÓN FINAL)

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sintomas = Column(String, nullable=False)
    zona_afectada = Column(String, nullable=False)
    condiciones_previas = Column(String, nullable=True)
    
    # 🚨 CORRECCIÓN CRÍTICA: Cambiar String a Integer
    tiempo_sintomas = Column(Integer, nullable=False) # <-- ¡ESTO DEBE SER INTEGER!
    
    edad = Column(Integer, nullable=False)
    sexo = Column(String, nullable=False)

    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    prioridad = Column(String, nullable=True)

    # Relación con el usuario
    usuario = relationship("User", back_populates="citas")

    def __repr__(self):
        return f"<Cita(id={self.id}, user_id={self.user_id}, prioridad={self.prioridad})>"