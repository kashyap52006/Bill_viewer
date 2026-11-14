
from fastapi import FastAPI, File, HTTPException, UploadFile

from .errors import ReceiptOCRError
from .main_processor import MainProcessor
from .schemas import RECEIPT_SCHEMA

app = FastAPI(
    title="Receipt OCR API",
    description="Extract structured information from receipt images.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/receipts/extract")
async def extract_receipt(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file.",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty.",
        )

    try:
        processor = MainProcessor()

        result = processor.process_receipt(
            image_path=image_bytes,
            json_schema=RECEIPT_SCHEMA,
        )

        return result

    except ReceiptOCRError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
