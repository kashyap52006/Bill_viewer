
from io import BytesIO

from PIL import Image, UnidentifiedImageError

from fastapi import FastAPI, File, HTTPException, UploadFile

from .errors import ReceiptOCRError
from .main_processor import MainProcessor
from .schemas import RECEIPT_SCHEMA

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

app = FastAPI(
    title="Receipt OCR API",
    description="Extract structured information from receipt images.",
    version="1.0.0",
)


def validate_image_content(image_bytes: bytes) -> None:
    try:
        with Image.open(BytesIO(image_bytes)) as image:

            allowed_formats = {"JPEG", "PNG", "WEBP", "GIF"}

            if image.format not in allowed_formats:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported image format.",
                )

            # Verify that the image data is structurally valid.
            image.verify()

    except HTTPException:
        raise

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image file.",
        ) from exc



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

    image_bytes = file.file.read(MAX_UPLOAD_SIZE + 1)

    if len(image_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image file is too large. Maximum allowed size is 10 MB.",
        )

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty.",
        )

    validate_image_content(image_bytes)

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
