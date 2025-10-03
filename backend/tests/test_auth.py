from backend.app.db import Base, engine, SessionLocal
from backend.app.models.user_model import User
from backend.app.models.cita_model import Cita

print("Creando tablas...")
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Crear usuario
nuevo_usuario = User(
    nombre="Samuel",
    apellido="García",
    correo="yusamuel@test.com",
    password_hash="hashedpassword123"
)
db.add(nuevo_usuario)
db.commit()
db.refresh(nuevo_usuario)
print(f"✅ Usuario creado: {nuevo_usuario.id} - {nuevo_usuario.correo}")

# Crear cita (guardando listas como CSV)
nueva_cita = Cita(
    user_id=nuevo_usuario.id,
    sintomas="Fiebre,Tos",
    zona_afectada="Pecho",
    condiciones_previas="Asma",
    edad=25,
    sexo="male",
    tiempo_con_sintomas=3,
    prioridad="urgente"
)
db.add(nueva_cita)
db.commit()
db.refresh(nueva_cita)
print(f"✅ Cita creada con ID {nueva_cita.id} para usuario {nueva_cita.user_id}")

# Consultar
usuario = db.query(User).filter(User.id == nuevo_usuario.id).first()
print(f"📌 Usuario: {usuario.nombre} {usuario.apellido}, correo: {usuario.correo}")
for cita in usuario.citas:
    print(f"   - Cita {cita.id}, prioridad: {cita.prioridad}, síntomas: {cita.sintomas}")

db.close()