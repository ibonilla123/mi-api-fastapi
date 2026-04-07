from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, create_db_and_tables, get_session
from models import Usuario, Libro
from typing import List

app = FastAPI(
    title="API de Gestión de Biblioteca",
    description="API CRUD para Usuarios y Libros desplegada en AWS EC2",
    version="1.0.0"
)

# Crear tablas al iniciar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- ENDPOINTS DE USUARIOS ---
@app.post("/usuarios/", response_model=Usuario, tags=["Usuarios"])
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@app.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
def leer_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()

# --- ENDPOINTS DE LIBROS ---
@app.post("/libros/", response_model=Libro, tags=["Libros"])
def crear_libro(libro: Libro, session: Session = Depends(get_session)):
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

@app.get("/libros/", response_model=List[Libro], tags=["Libros"])
def leer_libros(session: Session = Depends(get_session)):
    return session.exec(select(Libro)).all()

@app.delete("/libros/{libro_id}", tags=["Libros"])
def borrar_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(libro)
    session.commit()
    return {"mensaje": "Libro eliminado correctamente"}