from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, create_db_and_tables, get_session
from models import Product
from typing import List

app = FastAPI(
    title="API Ecommerce Isaac",
    description="API para gestión de productos conectada a Amazon RDS (Postgres)",
    version="2.0.0"
)

# Crear las tablas en RDS
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 1. Crear un producto (POST)
@app.post("/products", response_model=Product, tags=["Ecommerce"])
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# 2. Listar todos los productos (GET)
@app.get("/products", response_model=List[Product], tags=["Ecommerce"])
def read_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

# 3. Consultar un producto por ID (GET)
@app.get("/products/{id}", response_model=Product, tags=["Ecommerce"])
def read_product(id: int, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

# 4. Actualizar un producto (PUT)
@app.put("/products/{id}", response_model=Product, tags=["Ecommerce"])
def update_product(id: int, product_data: Product, session: Session = Depends(get_session)):
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Extraer datos nuevos
    new_data = product_data.model_dump(exclude_unset=True)
    for key, value in new_data.items():
        setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

# 5. Eliminar un producto (DELETE)
@app.delete("/products/{id}", tags=["Ecommerce"])
def delete_product(id: int, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(product)
    session.commit()
    return {"mensaje": f"Producto con ID {id} eliminado correctamente"}