# pip imports
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Boolean

# local imports
from data import Base

class User_Settings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(BigInteger, ForeignKey("users.telegram_id"), unique=True, index=True, nullable=False)
    
    use_TOG = Column(Boolean, default=False)
    language = Column(String, default="en")
    translate_from = Column(String, default="auto")
    translate_to = Column(String, default="en")
    ai_assistant = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="user_settings")
    
    def __repr__(self):
        return f"<User_Settings(id={self.id}, from_user={self.from_user}, language={self.language})>"
    