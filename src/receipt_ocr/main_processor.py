


from typing import Any, Dict, Optional

from receipt_ocr.provider import LLMProvider, MyAIProvider
from receipt_ocr.parser import DefaultParser


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
        image_path: str,
        json_schema: Dict[str, Any],
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        if response_format == "text":
            raise ValueError("MainProcessor requires a JSON response format.")

        response = self.provider.get_response(
            image=image_path,
            json_schema=json_schema,
            model=model,
            response_format=response_format,
        )
        content = response.text

        if content is None:
            raise ValueError("No content found in the response.")
        return self.parser.parse_response(content)

