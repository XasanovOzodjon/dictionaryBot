from data import Base
from sqlalchemy import Column, Integer, String, Boolean, BigInteger

class Admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    add_admin = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Admin(id={self.id}, name={self.name}, telegram_id={self.telegram_id})>"

   
class Chanels(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    channel_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    
    def __repr__(self):
        return f"<Channel(id={self.id}, name={self.name}, channel_id={self.channel_id})>"