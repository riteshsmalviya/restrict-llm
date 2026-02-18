import time
from functools import wraps
import logging

logger = logging.getLogger("restrict-llm.timers")

def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"Function {func.__name__} took {execution_time:.4f} seconds")
        return result
    return wrapper
