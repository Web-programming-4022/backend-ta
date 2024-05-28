from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

class USER(Base):
    __tablename__ = "USER"
    username =  Column(String,primary_key=True)
    password = Column(String)
    