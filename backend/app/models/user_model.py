from sqlalchemy import  Column,Integer,String,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db import Base 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key =True)
    nombre = Column(String,nullable=False)
    apellido = Column(String,nullable=False)
    correo = Column(String,unique=True,index=True,nullable=False)
    password_hash = Column(String,nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    citas = relationship("Cita",back_populates = "usuario")

    def __repr__(self):
        return f"<User(id={self.id}, correo={self.correo})>"