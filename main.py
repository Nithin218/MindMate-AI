from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from MindMateAI.Workflow.workflow import GraphBuilder
from starlette.responses import JSONResponse
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
from MindMateAI.logger import logger
import traceback
import os

load_dotenv()

app = FastAPI(
    title="MindMateAI API",
    description="CBT-powered mental health support API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("question must not be empty")
        if len(v) > 2000:
            raise ValueError("question must be under 2000 characters")
        return v


def _build_initial_state(question: str) -> dict:
    """
    Clean initial state aligned with the current MentalHealthState schema.
    Pipeline: emotion -> cbt -> ethical -> writer -> END
    """
    return {
        "user_query":      question,
        "emotion":         "",
        "cbt_response":    "",
        "final_output":    "",
        "ethical_check":   False,
        "messages":        [],
        "retry_count":     0,
        "remaining_steps": 20,
    }


@app.post("/query")
async def query_endpoint(query: QueryRequest):
    logger.info(f"Received query: {query.question[:80]}...")
    try:
        graph_builder = GraphBuilder()
        react_app = graph_builder()

        initial_state = _build_initial_state(query.question)
        output = react_app.invoke(initial_state)

        if isinstance(output, dict) and output.get("final_output"):
            final_output = output["final_output"]
        else:
            logger.error(f"Unexpected output shape: {output}")
            final_output = (
                "Something went wrong while generating your response. "
                "If you're in distress, please reach out to a mental health professional "
                "or call/text 988 (Suicide & Crisis Lifeline)."
            )

        logger.info(
            f"Pipeline complete | emotion={output.get('emotion')} | "
            f"ethical={'PASS' if output.get('ethical_check') else 'FAIL'} | "
            f"retries={output.get('retry_count', 0)}"
        )

        return {
            "answer": final_output,
            "meta": {
                "emotion": output.get("emotion"),
                "retries": output.get("retry_count", 0),
            }
        }

    except Exception as e:
        logger.error(f"Pipeline error: {e}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "An internal error occurred. Please try again.",
                "detail": str(e),
            },
        )


@app.get("/health")
async def health():
    return {"status": "ok"}