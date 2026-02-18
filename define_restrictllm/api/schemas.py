from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl

class LLMConfig(BaseModel):
    url: str
    method: str = "POST"
    headers: Dict[str, str] = Field(default_factory=dict)
    bodyTemplate: Dict[str, Any]
    responsePath: str

class Rules(BaseModel):
    maxLength: Optional[int] = None
    minLength: Optional[int] = None
    format: Optional[str] = None
    blockedWords: List[str] = Field(default_factory=list)
    requiredKeys: List[str] = Field(default_factory=list)
    regex: Optional[str] = None
    strict: bool = True
    retryAttempts: int = 3

class Options(BaseModel):
    timeout: int = 30

class GenerateRequest(BaseModel):
    llm: LLMConfig
    prompt: str
    rules: Optional[Rules] = Field(default_factory=Rules)
    options: Optional[Options] = Field(default_factory=Options)
