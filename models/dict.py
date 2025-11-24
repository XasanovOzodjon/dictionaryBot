# pip imports
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text

# local imports
from data import Base


class TOG(Base):
    __tablename__ = 'TOG'
    
    id = Column(Integer, primary_key=True, index=True)
    dict_id = Column(ForeignKey('dicts.id'), nullable=False)
    obraz = Column(String, nullable=False)
    garm = Column(Text, nullable=False)
    
    dict = relationship("Dict", back_populates="tog")

class Dict(Base):
    __tablename__ = 'dicts'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(String, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    
    tog = relationship("TOG", back_populates='dict')
    user = relationship("User", back_populates='dicts')
    

    