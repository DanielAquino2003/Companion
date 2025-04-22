from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Messages(Base):
    __tablename__= "messages"
    id = Column(Integer, primary_key=True, index=True) # Primary key for the Messages table
    ia_id = Column(Integer, ForeignKey("ias.id")) # Foreign key referencing the IA table
    role = Column(String) # "User" or "Assistant"
    content = Column(Text) # Content of the message
    timestamp = Column(DateTime, default=datetime.utcnow) # Timestamp of when the message was created

    ia = relationship("IA", back_populates="messages") # Relationship to the IA table

class IA(Base):
    __tablename__ = "ias"
    id = Column(Integer, primary_key=True, index=True) # Primary key for the IA table
    name = Column(String, index=True, unique=True) # Name of the IA, must be unique
    description = Column(Text) # Description of the IA

    messages = relationship("Messages", back_populates="ia") # Relationship to the Message table

