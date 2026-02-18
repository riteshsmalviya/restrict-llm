import time
from define_restrictllm.api.schemas import GenerateRequest
from define_restrictllm.services.llm_client import LLMClient
from define_restrictllm.core.validator import Validator
from define_restrictllm.core.restrictor import Restrictor
from define_restrictllm.core.exceptions import MaxRetriesExceeded, LLMClientError
from define_restrictllm.utils.logger import setup_logger

logger = setup_logger("engine")

class Engine:
    def __init__(self):
        self.client = LLMClient()
        self.validator = Validator()
        self.restrictor = Restrictor()

    def process(self, request: GenerateRequest) -> str:
        """
        Orchestrates the request -> validate -> retry loop.
        """
        current_prompt = request.prompt
        attempts = 0
        max_attempts = request.rules.retryAttempts if request.rules else 1
        
        last_errors = []
        
        while attempts < max_attempts:
            attempts += 1
            logger.info(f"Attempt {attempts}/{max_attempts}")
            
            try:
                # Call LLM
                response_text = self.client.execute(
                    config=request.llm,
                    prompt=current_prompt,
                    timeout=request.options.timeout if request.options else 30
                )
                
                # Validate
                if request.rules:
                    validation = self.validator.validate(response_text, request.rules)
                    
                    if validation.valid:
                        logger.info("Validation passed")
                        return response_text
                    
                    logger.warning(f"Validation failed: {validation.errors}")
                    last_errors = validation.errors
                    
                    # Update prompt for retry if we have retries left
                    if attempts < max_attempts:
                        current_prompt = self.restrictor.create_retry_prompt(
                            request, 
                            validation.errors, 
                            response_text
                        )
                else:
                    # No rules, just return
                    return response_text

            except LLMClientError as e:
                # If it's a client error, we might want to retry with the same prompt or fail
                logger.error(f"LLM Client error: {e}")
                # For now, we count this as an attempt. 
                # Ideally, network errors should have their own retry logic inside client, 
                # but validation retries are different.
                # Here we just continue to next attempt if possible, but maybe delay?
                last_errors = [str(e)]
                time.sleep(1) # Simple backoff

        # If we exit loop, we failed
        error_msg = f"Max retries exceeded. Last errors: {last_errors}"
        logger.error(error_msg)
        raise MaxRetriesExceeded(error_msg)
