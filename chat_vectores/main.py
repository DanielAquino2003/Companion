from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, IA, Messages
from vector_store import add_memory, search_memory
import openai
import os
from dotenv import load_dotenv

Base.metadata.create_all(bind=engine)
app = FastAPI()

""" openai.api_key = ""
"""
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat/{ia_name}")
def chat(ia_name: str, user_message: str, db: Session = Depends(get_db)):
    # Busca o crea la IA
    ia = db.query(IA).filter(IA.name == ia_name).first()
    if not ia:
        ia = IA(name=ia_name, description=f"IA especializada en {ia_name}")
        db.add(ia)
        db.commit()
        db.refresh(ia)

    # Guarda el mensaje del usuario
    msg = Messages(ia_id=ia.id, role="user", content=user_message)
    db.add(msg)
    db.commit()

    # Agrega a la memoria vectorial
    add_memory(ia_name, user_message)

    # Busca contexto relevante
    recuerdos = search_memory(ia_name, user_message)
    contexto = "\n".join(recuerdos[-5:])  # Últimos recuerdos relevantes

    prompt = f"""
    Eres un asistente experto en {ia_name}.
    Esto es lo que ya sabes sobre esta conversación:
    {contexto}

    Usuario: {user_message}
    Asistente:
    """

    completion = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ] 
    )


    respuesta = completion.choices[0].message["content"]

    # Guarda respuesta
    db.add(Messages(ia_id=ia.id, role="assistant", content=respuesta))
    db.commit()

    return {"response": respuesta}
