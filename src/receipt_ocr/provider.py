
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Mapping, Optional, Union

from google import genai

from .prompts import SYSTEM_PROMPT, USER_PROMPT


class LLMProvider(ABC):
    @abstractmethod
    def get_response(
        self,
        image: Union[str, bytes],
        json_schema: Mapping[str, Any],
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Any:
        pass


class MyAIProvider(LLMProvider):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required.")

        self.base_url = base_url
        http_options = (
            genai.types.HttpOptions(base_url=self.base_url)
            if self.base_url
            else None
        )
        self.client = genai.Client(
            api_key=self.api_key,
            http_options=http_options,
        )

    def get_response(
        self,
        image: Union[str, bytes],
        json_schema: Mapping[str, Any],
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Any:
        selected_model = model or os.getenv("DEFAULT_MODEL")
        if not selected_model:
            raise ValueError("A model is required through the model argument or DEFAULT_MODEL.")

        response_format = response_format or "json_schema"
        if response_format not in {"json_object", "json_schema", "text"}:
            raise ValueError(
                "Invalid response_format. Expected 'json_object', "
                "'json_schema', or 'text'."
            )

        image_bytes, mime_type = self._read_image(image)
        system_prompt = SYSTEM_PROMPT.format(
            json_schema_content=json.dumps(json_schema, indent=2),
        )
        config: dict[str, Any] = {
            "system_instruction": system_prompt,
            "temperature": 0.2,
        }
        if response_format in {"json_object", "json_schema"}:
            config["response_mime_type"] = "application/json"
        if response_format == "json_schema":
            config["response_schema"] = dict(json_schema)

        return self.client.models.generate_content(
            model=selected_model,
            contents=[
                USER_PROMPT,
                genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
            config=genai.types.GenerateContentConfig(**config),
        )

    @staticmethod
    def _read_image(image: Union[str, bytes]) -> tuple[bytes, str]:
        if isinstance(image, bytes):
            mime_type = {
                b"\x89PNG\r\n\x1a\n": "image/png",
                b"\xff\xd8\xff": "image/jpeg",
                b"RIFF": "image/webp",
                b"GIF87a": "image/gif",
                b"GIF89a": "image/gif",
            }
            for signature, detected_type in mime_type.items():
                if image.startswith(signature):
                    return image, detected_type
            raise ValueError("Unsupported or unrecognized image bytes.")

        path = Path(image)
        if not path.is_file():
            raise FileNotFoundError(f"Image file does not exist: {path}")

        mime_type = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }.get(path.suffix.lower())
        if mime_type is None:
            raise ValueError(f"Unsupported image type: {path.suffix or '<none>'}")

        return path.read_bytes(), mime_type