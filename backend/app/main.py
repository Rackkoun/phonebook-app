# file backend/app/main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import os
from pathlib import Path
from backend.config import backend_config

# create engine
engine = create_engine(backend_config.POSTGRES_DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

# model
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone = Column(String)
    email = Column(String)

# schema
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str

class ContactResponse(ContactCreate):
    id: int
    class Config:
        from_attributes = True


########### api #####################
app = FastAPI(title="Phonebook API")

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session= Depends(get_db)):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    return db_contact

@app.get("/contacts/", response_model=list[ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Contact).offset(skip).limit(limit).all()


@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}