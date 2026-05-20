from sqlalchemy import Column, Integer, String
from database.connection import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    projects = relationship("Project", backref="owner")
