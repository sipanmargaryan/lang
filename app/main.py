from fastapi import FastAPI

from app.helpers.database import SessionLocal

from .routers.products import products

app = FastAPI()

app.include_router(products.router, prefix="/api/v1")


@app.middleware("http")
async def db_session_middleware(request, call_next):
    response = None
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get('/health')
def health():
    return True