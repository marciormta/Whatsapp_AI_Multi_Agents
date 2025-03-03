from fastapi import FastAPI
from app.Routers import Webhook
from app.Models.Database import engine
from app.Models.Models import Base

# Optei por nao utilizar o alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Webhook.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
