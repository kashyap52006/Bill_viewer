
import json
import sys

from src.receipt_ocr.main_processor import MainProcessor
from src.receipt_ocr.errors import ReceiptOCRError


# Define the expected receipt output.
from src.receipt_ocr.schemas import RECEIPT_SCHEMA


def main():
    processor = MainProcessor()

    result = processor.process_receipt(
        image_path="images/receipt.jpg",
        json_schema=RECEIPT_SCHEMA,
    )

    print("\nExtracted receipt information:")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    try:
        main()
    except ReceiptOCRError as error:
        print(f"Receipt processing failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
