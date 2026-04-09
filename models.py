from typing import Optional
from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str # Nombre obligatorio
    description: Optional[str] = None # Descripción opcional
    price: float # Precio obligatorio
    stock: int # Stock obligatorio
    image_url: Optional[str] = None # URL de imagen opcional