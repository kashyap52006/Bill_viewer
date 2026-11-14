


from typing import Any, Dict, Optional, Union

from pathlib import Path

from .errors import ConfigurationError, ResponseError
from .provider import LLMProvider, MyAIProvider
from .parser import DefaultParser


class MainProcessor:
    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        parser: Optional[DefaultParser] = None,
    ):
        self.provider = provider if provider is not None else MyAIProvider()
        self.parser = parser if parser is not None else DefaultParser()

    def process_receipt(
        self,
        image_path: Union[str, Path, bytes],
        json_schema: Dict[str, Any],
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        if response_format == "text":
            raise ConfigurationError("MainProcessor requires a JSON response format.")

        response = self.provider.get_response(
            image=image_path,
            json_schema=json_schema,
            model=model,
            response_format=response_format,
        )

        try:
            content = response.text
        except AttributeError as error:
            raise ResponseError("The provider returned an invalid response object.") from error

        if not isinstance(content, str) or not content.strip():
            raise ResponseError("The provider returned no usable content.")

        return self.parser.parse_response(content)

