from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from MindMateAI.Workflow.workflow import GraphBuilder
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_endpoint(query: QueryRequest):
    try:
        print(query)
        graph_builder = GraphBuilder()
        react_app = graph_builder()

        initial_state = {
        "user_query": query.question,
        "rewritten_query": "",
        "emotion": "",
        "cbt_response": "",
        "schedule_recommendation": "",
        "ethical_check": True,
        "ethical_feedback": "",
        "final_output": "",
        "messages": [],
        "retry_count": 0,
        "remaining_steps": 5
    }
        # Assuming request is a pydantic object like: {"question": "your text"}
        output = react_app.invoke(initial_state)

        # If result is dict with messages:
        if isinstance(output, dict) and "final_output" in output:
            final_output = output["final_output"]  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})