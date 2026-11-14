import argparse
import sys
import json

from .main_processor import MainProcessor
from .errors import ReceiptOCRError
from .schemas import RECEIPT_SCHEMA

def main():
    parser = argparse.ArgumentParser(
        description="Process a receipt image and extract information."
        )
    parser.add_argument(
        "image_path",
        help = "Path to the receipt image file."
    )
    parser.add_argument(
        "--model",
        help = "Gemini model to use. Defaults to your configured model."
    )
    parser.add_argument(
        "--response_format",    
        help = "Format of the response. Defaults to JSON."
    )

    args = parser.parse_args()

    try : 
        processor = MainProcessor()
        result = processor.process_receipt(
            image_path=args.image_path,
            json_schema=RECEIPT_SCHEMA,
            model=args.model,
            response_format=args.response_format,
        )
        print(json.dumps(result, indent=4 , ensure_ascii=False))

    except ReceiptOCRError as e:
        print(f"Receipt processing failed: {e}" , file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()