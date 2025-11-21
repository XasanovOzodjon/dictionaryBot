from data import Base
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    
    user_settings = relationship("User_Settings", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"
    