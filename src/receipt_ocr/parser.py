import json
from typing import Any, Dict


class DefaultParser:
    def parse_response(self, content: str) -> Dict[str, Any]:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError("The provider returned invalid JSON.") from error

        if not isinstance(parsed, dict):
            raise ValueError("The provider response must be a JSON object.")

        return parsed