import argparse
import sys
import json

from .main_processor import MainProcessor
from .errors import ReceiptOCRError
from .schemas import RECEIPT_SCHEMA

import logging

from .logging_config import configure_logging

logger = logging.getLogger(__name__)

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
        "--response-format",
        choices=["json_object", "json_schema"],
        default="json_schema",
        help="Response format. Defaults to JSON schema.",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the application logging level.",
    )

    args = parser.parse_args()
    configure_logging(args.log_level)


    try : 
        logger.info("Starting receipt processing.")
        processor = MainProcessor()
        result = processor.process_receipt(
            image_path=args.image_path,
            json_schema=RECEIPT_SCHEMA,
            model=args.model,
            response_format=args.response_format,
        )
        print(json.dumps(result, indent=4 , ensure_ascii=False))
        logger.info("Receipt processing completed successfully.")

    except ReceiptOCRError as exc:
        logger.error("Receipt processing failed: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()