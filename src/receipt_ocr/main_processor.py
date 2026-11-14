


from typing import Optional , Dict , Any

from receipt_ocr.provider import  MyAIProvider
from receipt_ocr.parser import DefaultParser


class MainProcessor:
    def __init__(
            self,
            provider : Optional[MyAIProvider] = None , 
            parser : Optional[DefaultParser] = None):
        self.provider = provider or MyAIProvider()
        self.parser = parser or DefaultParser()

    def process_receipt(
            self,
            image_path : str,
            json_schema : Dict[str , Any],
            model : Optional[str] = None,
            response_format : Optional[str] = None,
    )  -> Dict[str , Any] :
        response = self.provider.get_response(
            image = image_path , json_schema = json_schema , model = model , response_format = response_format)
        content = response.choices[0].message.content

        if content is None:
            raise ValueError("No content found in the response.")
        return self.parser.parse_response(content)

        




