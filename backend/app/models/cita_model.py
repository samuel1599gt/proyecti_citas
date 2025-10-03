from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db import Base

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sintomas = Column(String, nullable=False)
    zona_afectada = Column(String, nullable=False)
    condiciones_previas = Column(String, nullable=True)
    tiempo_con_sintomas = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(String, nullable=False)

    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    prioridad = Column(String, nullable=True)  # Clasificación del modelo

    # Relación con el usuario
    usuario = relationship("User", back_populates="citas")

    def _repr_(self):
        return f"<Cita(id={self.id}, user_id={self.user_id}, prioridad={self.prioridad})>"