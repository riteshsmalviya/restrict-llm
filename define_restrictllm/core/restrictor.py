from typing import List
from define_restrictllm.api.schemas import GenerateRequest

class Restrictor:
    def create_retry_prompt(self, original_request: GenerateRequest, errors: List[str], current_response: str) -> str:
        """
        Creates a prompt to fix the errors in the response.
        """
        error_msg = "\n- ".join(errors)
        
        # We append the original prompt context and the errors
        # This is a meta-prompt strategy.
        
        retry_instruction = (
            f"The previous response was invalid. \n"
            f"Errors found:\n- {error_msg}\n\n"
            f"Please generate a new response for the original prompt: '{original_request.prompt}' \n"
            f"that strictly follows these rules:\n"
        )
        
        if original_request.rules.maxLength:
            retry_instruction += f"- Max length: {original_request.rules.maxLength}\n"
        if original_request.rules.minLength:
            retry_instruction += f"- Min length: {original_request.rules.minLength}\n"
        if original_request.rules.blockedWords:
            retry_instruction += f"- Do not use words: {', '.join(original_request.rules.blockedWords)}\n"
        if original_request.rules.format == "json":
            retry_instruction += "- Output valid JSON\n"
        if original_request.rules.requiredKeys:
            retry_instruction += f"- JSON must contain keys: {', '.join(original_request.rules.requiredKeys)}\n"
            
        retry_instruction += "\nProvide ONLY the corrected response."
        
        return retry_instruction
