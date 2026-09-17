from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="AI Repo Intelligence Agent",
    description="Backend API to index GitHub repositories and answer codebase questions using LangGraph RAG.",
    version= "1.0.0"
)

app.include_router(api_router,prefix="/api/v1")

@app.get("/",tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "AI Repo Intelligence Agent service running."}