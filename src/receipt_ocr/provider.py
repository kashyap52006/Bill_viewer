import json
from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import Any, Mapping, Optional, Union

from PIL import Image
from google import genai
from google.genai import errors as genai_errors

from .config import get_settings
from .errors import ConfigurationError, ImageError, ProviderError
from .image_preprocessor import ImagePreprocessor
from .prompts import SYSTEM_PROMPT, USER_PROMPT


class LLMProvider(ABC):
    @abstractmethod
    def get_response(
        self,
        image: Union[str, Path, bytes],
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
        self.image_preprocessor = ImagePreprocessor()
        settings = get_settings()

        self.api_key = api_key or settings.gemini_api_key

        if not self.api_key:
            raise ConfigurationError("GEMINI_API_KEY is required.")

        self.default_model = settings.default_model

        self.base_url = base_url
        http_options = genai.types.HttpOptions(
            api_version="v1beta",
            base_url=self.base_url,
        )
        try:
            self.client = genai.Client(
                api_key=self.api_key,
                http_options=http_options,
            )
        except (TypeError, ValueError) as error:
            raise ConfigurationError(
                "Unable to initialize the Gemini client. Check its configuration."
            ) from error

        
    
    def _read_image(
            self,
            image: Union[str, Path, bytes],
        ) -> tuple[bytes, str]:

        if isinstance(image, bytes):
            if not image:
                raise ImageError("Image data cannot be empty.")

            image_bytes = image

        else:
            path = Path(image)

            if not path.is_file():
                raise ImageError(f"Image file does not exist: {path}")

            try:
                image_bytes = path.read_bytes()
            except OSError as error:
                raise ImageError(
                    f"Unable to read image file: {path}"
                ) from error

            if not image_bytes:
                raise ImageError(f"Image file is empty: {path}")

        # Validate and identify the image using Pillow.
        try:
            from PIL import Image
            from io import BytesIO

            with Image.open(BytesIO(image_bytes)) as img:
                mime_type = Image.MIME.get(img.format)

        except Exception as error:
            raise ImageError("Unsupported or invalid image.") from error

        if not mime_type:
            raise ImageError("Unable to identify image format.")

        return image_bytes, mime_type


    def get_response(
        self,
        image: Union[str, Path, bytes],
        json_schema: Mapping[str, Any],
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Any:
        selected_model = model or self.default_model
        if not selected_model:
            raise ConfigurationError(
                "A model is required through the model argument or DEFAULT_MODEL."
            )
        if not isinstance(json_schema, Mapping) or not json_schema:
            raise ConfigurationError("json_schema must be a non-empty mapping.")

        response_format = response_format or "json_schema"
        if response_format not in {"json_object", "json_schema", "text"}:
            raise ConfigurationError(
                "Invalid response_format. Expected 'json_object', "
                "'json_schema', or 'text'."
            )

        image_bytes, mime_type = self._read_image(image)
        image_bytes, mime_type = self.image_preprocessor.preprocess(
            image_bytes
        )

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

        try:
            return self.client.models.generate_content(
                model=selected_model,
                contents=[
                    USER_PROMPT,
                    genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                ],
                config=genai.types.GenerateContentConfig(**config),
            )
        except genai_errors.APIError as error:
            raise ProviderError(
                f"Gemini request failed ({error.code}): {error.message}"
            ) from error
        except (TypeError, ValueError) as error:
            raise ProviderError("Unable to create the Gemini request.") from error

    