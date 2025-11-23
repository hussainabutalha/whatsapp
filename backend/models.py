from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(String, index=True)
    user_name = Column(String)
    product_name = Column(String)
    product_review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ConversationState(Base):
    __tablename__ = "conversation_states"

    contact_number = Column(String, primary_key=True, index=True)
    state = Column(String) # INIT, ASKED_PRODUCT, ASKED_NAME, ASKED_REVIEW
    temp_data = Column(JSON, default={})
