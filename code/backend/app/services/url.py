import string
import random
from sqlalchemy.orm import Session
from app.models import Url

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_short_url(db: Session, original_url: str) -> Url:
    # Ensure uniqueness (simple retry logic)
    for _ in range(10):
        short_code = generate_short_code()
        existing = db.query(Url).filter(Url.short_code == short_code).first()
        if not existing:
            db_url = Url(short_code=short_code, original_url=original_url)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return db_url
    raise Exception("Could not generate a unique short code.")

def get_original_url(db: Session, short_code: str) -> Url | None:
    return db.query(Url).filter(Url.short_code == short_code).first()
