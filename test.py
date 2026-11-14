
import json

from src.receipt_ocr.main_processor import MainProcessor


# Define the expected receipt output.
receipt_schema = {
    "type": "object",
    "properties": {
        "merchant_name": {
            "type": "string"
        },
        "transaction_date": {
            "type": "string"
        },
        "total_amount": {
            "type": "number"
        },
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string"
                    },
                    "item_quantity": {
                        "type": "number"
                    },
                    "item_price": {
                        "type": "number"
                    },
                    "item_total": {
                        "type": "number"
                    }
                },
                "required": [
                    "item_name",
                    "item_quantity",
                    "item_price",
                    "item_total"
                ]
            }
        }
    },
    "required": [
        "merchant_name",
        "transaction_date",
        "total_amount",
        "line_items"
    ]
}


def main():
    processor = MainProcessor()

    result = processor.process_receipt(
        image_path="images/receipt.jpg",
        json_schema=receipt_schema,
    )

    print("\nExtracted receipt information:")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
