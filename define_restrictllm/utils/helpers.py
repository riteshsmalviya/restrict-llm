from typing import Any, Dict

def extract_json_path(data: Dict[str, Any], path: str) -> Any:
    """
    Extracts a value from a nested dictionary using a dot-notation path.
    Supports array indexing like 'choices[0].message.content'.
    """
    keys = path.replace("]", "").replace("[", ".").split(".")
    current = data
    
    try:
        for key in keys:
            if not key:  # Handle consecutive dots or empty parts
                continue
            if key.isdigit():
                key = int(key)
                if isinstance(current, list) and 0 <= key < len(current):
                    current = current[key]
                else:
                    return None
            else:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
        return current
    except Exception:
        return None
