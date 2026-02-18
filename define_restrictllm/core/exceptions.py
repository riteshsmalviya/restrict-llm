class RestrictLLMException(Exception):
    """Base exception for restrict-llm"""
    pass

class LLMClientError(RestrictLLMException):
    """Raised when the LLM client fails to get a response"""
    pass

class ValidationException(RestrictLLMException):
    """Raised when response validation fails"""
    pass

class MaxRetriesExceeded(RestrictLLMException):
    """Raised when maximum retries are exceeded"""
    pass
