from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    # Relación: Un usuario puede tener muchos libros
    libros: List["Libro"] = Relationship(back_populates="usuario")

class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    autor: str
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    # Relación: El libro pertenece a un usuario
    usuario: Optional[Usuario] = Relationship(back_populates="libros")