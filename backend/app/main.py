from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import url

app = FastAPI(title="URL Shortener API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(url.router)
