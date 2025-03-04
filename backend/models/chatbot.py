from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import generate_rag_response  
import uvicorn
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str




@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    """ API endpoint for handling user queries with streaming response """
    try:
        # stream response from generate_rag_response
        def response_streamer():
            for chunk in generate_rag_response(request.query):  #use generator from rag_pipeline
                yield chunk  

        return StreamingResponse(response_streamer(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




