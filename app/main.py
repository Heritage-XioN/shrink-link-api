from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, SQLModel
from app.controllers import auth_controller, redirect_controller, urls_controller, user_controller


# Note: im really good with naming
# i really did not want to waste time thinking of good names so bare with me
# i added description in every function that should explain what its doing thanks


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

# setup for cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(auth_controller.router)
app.include_router(urls_controller.router)
app.include_router(user_controller.router)
app.include_router(redirect_controller.router)


# root
@app.get("/")
def read_root():
    return {"message": "running"}

# health check.
# might add something different later


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
