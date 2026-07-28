from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UrlCreate, UrlResponse
from app.services import url as url_service

router = APIRouter()

@router.post("/api/shorten", response_model=UrlResponse)
def shorten_url(request_data: UrlCreate, request: Request, db: Session = Depends(get_db)):
    try:
        url_obj = url_service.create_short_url(db, str(request_data.url))
        # Build the short url based on the incoming request base url
        base_url = str(request.base_url)
        short_url = f"{base_url}api/{url_obj.short_code}"
        return UrlResponse(short_url=short_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url_obj = url_service.get_original_url(db, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_obj.original_url, status_code=302)
