from fastapi import FastAPI
from define_restrictllm.api.routes import router
from define_restrictllm.config import settings
from define_restrictllm.utils.logger import setup_logger

logger = setup_logger("main")

app = FastAPI(
    title=settings.APP_NAME,
    description="Universal LLM Response Restriction Proxy",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("define_restrictllm.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
