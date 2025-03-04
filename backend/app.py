from fastapi import FastAPI
from backend.routes import chatbot  #double check routes and files directory at the end


app = FastAPI()
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])


@app.get("/")
def root():
    return {"message": "API is running successfully!"}
