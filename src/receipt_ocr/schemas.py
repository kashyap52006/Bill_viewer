
RECEIPT_SCHEMA = {
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
