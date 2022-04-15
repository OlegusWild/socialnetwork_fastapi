from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine

from .routers import posts, users, auth, votes


# No longer necessary - use alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# allowed domain which cam talk to our API 
origins = [
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Weclome to my API!"}


# redirect to separeted files
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
