from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="tensor-lab-145 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "tensor-lab-145"

class AnalyzeRequest(BaseModel):
    source_path: str
    language: Optional[str] = None

class AnalyzeResponse(BaseModel):
    functions: list = []
    commands: list = []
    entry_points: list = []

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse()

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    return AnalyzeResponse()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
