import re
import json
from typing import List, Optional
from define_restrictllm.api.schemas import Rules
from define_restrictllm.utils.logger import setup_logger

logger = setup_logger("validator")

class ValidationResult:
    def __init__(self, valid: bool, errors: List[str]):
        self.valid = valid
        self.errors = errors

class Validator:
    def validate(self, content: str, rules: Rules) -> ValidationResult:
        errors = []

        # 1. Max Length
        if rules.maxLength is not None and len(content) > rules.maxLength:
            errors.append(f"Content length {len(content)} exceeds maximum of {rules.maxLength}")

        # 2. Min Length
        if rules.minLength is not None and len(content) < rules.minLength:
            errors.append(f"Content length {len(content)} is less than minimum of {rules.minLength}")

        # 3. Blocked Words
        if rules.blockedWords:
            for word in rules.blockedWords:
                if word.lower() in content.lower():
                    errors.append(f"Content contains blocked word: '{word}'")

        # 4. Regex
        if rules.regex:
            if not re.search(rules.regex, content):
                errors.append(f"Content does not match regex: {rules.regex}")

        # 5. Format and Required Keys (JSON)
        if rules.format == "json":
            try:
                # Strip markdown code fences LLMs often wrap JSON in
                cleaned = content.strip()
                if cleaned.startswith("```"):
                    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
                data = json.loads(cleaned)
                if rules.requiredKeys:
                    missing_keys = [key for key in rules.requiredKeys if key not in data]
                    if missing_keys:
                        errors.append(f"Missing required keys in JSON: {', '.join(missing_keys)}")
            except json.JSONDecodeError:
                errors.append("Content is not valid JSON")

        return ValidationResult(valid=len(errors) == 0, errors=errors)
