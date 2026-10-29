from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class APIHistory(Base):
    __tablename__ = 'api_history'
    id = Column(Integer, primary_key=True, index=True)
    api_url = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer)
    response_time = Column(Float)
    content_type = Column(String(150))
    response_headers = Column(Text)
    response_body = Column(Text)
    security_score = Column(Float, default=0)
    present_security_headers = Column(Text)
    missing_security_headers = Column(Text)
    missing_header_percentage = Column(Float, default=0)
    ai_recommendation = Column(Text)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
