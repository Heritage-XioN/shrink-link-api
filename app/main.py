from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, SQLModel
from app.api.v1.endpoints import auth

# alembic is handling the creation of the DB tables
# so you can leave this commmented out
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="portfolio api",
    description="the api for my portfolio site",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

#setup for cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routes
app.include_router(auth.router)



# root 
@app.get("/")
def read_root():
    return {"message": "running"}

# health check. might add something different later
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
