from fastapi import APIRouter, HTTPException, Depends
from define_restrictllm.api.schemas import GenerateRequest
from define_restrictllm.core.engine import Engine
from define_restrictllm.core.exceptions import MaxRetriesExceeded, LLMClientError

router = APIRouter()

def get_engine():
    return Engine()

@router.post("/v1/restrictllm/generate")
async def generate(request: GenerateRequest, engine: Engine = Depends(get_engine)):
    """
    Main endpoint to generate restricted LLM responses.
    """
    try:
        result = engine.process(request)
        return {"result": result}
    except MaxRetriesExceeded as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LLMClientError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
