from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError # Usamos 'jose' ya que tu servicio de login lo usa

# Importar las dependencias y modelos necesarios
from app.db import get_db
from app.models.user_model import User

# --- Sincronización de Claves Secretas ---
# La clave debe coincidir con la usada en tu servicio de login.
JWT_SECRET = "MI_SUPER_SECRETO"
JWT_ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    # Añadimos la dependencia de la DB para poder buscar al usuario
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403, 
                    detail="Esquema de autenticación inválido. Use Bearer."
                )
            
            token = credentials.credentials
            
            # 1. Validar y decodificar el token
            try:
                # Usamos el SECRET_KEY y ALGORITHM sincronizados
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                correo = payload.get("sub")
            except JWTError:
                raise HTTPException(status_code=401, detail="Token de autenticación inválido o corrupto.")
            except Exception as e:
                 raise HTTPException(status_code=403, detail=f"Error al validar el token: {e}")

            # 2. Buscar el objeto User en la DB
            user = db.query(User).filter(User.correo == correo).first()
            
            if not user:
                raise HTTPException(status_code=404, detail="Usuario asociado al token no encontrado.")

            # 3. Devolver el objeto User (¡esto resuelve el AttributeError!)
            return user
        
        else:
            raise HTTPException(
                status_code=403, 
                detail="No se proporcionaron credenciales de autenticación."
            )

    # La función verify_jwt ya no es necesaria, su lógica está en __call__
    # para tener acceso a la DB y devolver el objeto User.