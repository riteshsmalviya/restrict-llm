import json
import requests
from typing import Any, Dict
from define_restrictllm.api.schemas import LLMConfig
from define_restrictllm.utils.logger import setup_logger
from define_restrictllm.utils.helpers import extract_json_path
from define_restrictllm.core.exceptions import LLMClientError

logger = setup_logger("llm_client")

class LLMClient:
    def execute(self, config: LLMConfig, prompt: str, timeout: int = 30) -> str:
        """
        Executes the LLM request based on configuration and prompt.
        """
        try:
            # 1. Prepare URL and Headers
            url = config.url
            headers = config.headers
            
            # 2. Prepare Body
            # Deep copy to avoid modifying the original template in place for subsequent requests if reused
            # But here config is per request usually.
            body = self._replace_template(config.bodyTemplate, prompt)
            
            logger.debug(f"Calling LLM: {url} | Method: {config.method}")
            
            # 3. Make Request
            response = requests.request(
                method=config.method,
                url=url,
                headers=headers,
                json=body,
                timeout=timeout
            )
            
            response.raise_for_status()
            response_json = response.json()
            
            # 4. Extract Response
            extracted_text = extract_json_path(response_json, config.responsePath)
            
            if extracted_text is None:
                raise LLMClientError(f"Failed to extract response using path: {config.responsePath}. Response: {json.dumps(response_json)[:200]}...")
                
            if not isinstance(extracted_text, str):
                # Attempt to convert to string if it's not
                extracted_text = str(extracted_text)
                
            return extracted_text

        except requests.RequestException as e:
            logger.error(f"HTTP Request failed: {e}")
            raise LLMClientError(f"External LLM request failed: {str(e)}")
        except ValueError as e: # JSON decode error
            logger.error(f"Invalid JSON response: {e}")
            raise LLMClientError("External LLM returned invalid JSON")
        except Exception as e:
            logger.error(f"Unexpected error in LLMClient: {e}")
            raise LLMClientError(f"Unexpected error: {str(e)}")

    def _replace_template(self, template: Any, prompt: str) -> Any:
        """
        Recursively replaces {{prompt}} in the body template.
        """
        if isinstance(template, str):
            return template.replace("{{prompt}}", prompt)
        elif isinstance(template, dict):
            return {k: self._replace_template(v, prompt) for k, v in template.items()}
        elif isinstance(template, list):
            return [self._replace_template(i, prompt) for i in template]
        else:
            return template
