import json
from typing import Any, Dict

from .errors import ResponseParseError


class DefaultParser:
    def parse_response(self, content: str) -> Dict[str, Any]:
        if not isinstance(content, str) or not content.strip():
            raise ResponseParseError("The provider response must be non-empty text.")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as error:
            raise ResponseParseError("The provider returned invalid JSON.") from error

        if not isinstance(parsed, dict):
            raise ResponseParseError("The provider response must be a JSON object.")

        return parsed