from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

""" 
- create_engine: Función para crear un motor de conexión a la base de datos.
- declarative_base: Función que genera una clase base para definir modelos (tablas) en SQLAlchemy.
- sessionmaker: Función para crear una fábrica de sesiones que permite interactuar con la base de datos. 
"""

DATABASE_URL = "sqlite:///./ia_chat.db"  # Replace with your database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
""" 
create_engine crea un objeto engine que gestiona la conexión a la base de datos especificada en DATABASE_URL.
connect_args={"check_same_thread": False}: Este argumento es específico para SQLite. 
Por defecto, SQLite restringe el acceso a la base de datos al hilo que la creó. Este parámetro deshabilita esa restricción, 
permitiendo que múltiples hilos accedan a la base de datos (útil en aplicaciones web como FastAPI).
"""
SessionLocal = sessionmaker(autoflush=False, bind=engine)
"""
sessionmaker crea una fábrica de sesiones (SessionLocal) que se vincula al motor (engine).
Las sesiones son objetos que permiten realizar operaciones en la base de datos (como consultas, inserciones, etc.).
autoflush=False: Desactiva el vaciado automático de cambios a la base de datos antes de ejecutar consultas, 
lo que da más control al desarrollador sobre cuándo se confirman los cambios.
"""
Base = declarative_base()

"""
declarative_base() crea una clase base (Base) que será usada para definir modelos (tablas) en la base de datos.
Los modelos son clases de Python que heredan de Base y representan tablas en la base de datos. 
Por ejemplo, podrías definir una clase User para una tabla de usuarios.
"""

