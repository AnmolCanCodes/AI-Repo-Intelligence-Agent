from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title="AI Repo Intelligence Agent",
    description="Backend API to index GitHub repositories and answer codebase questions using LangGraph RAG.",
    version= "1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server and common React port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router,prefix="/api/v1")

@app.get("/",tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "AI Repo Intelligence Agent service running."}