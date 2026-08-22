from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(6), unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
