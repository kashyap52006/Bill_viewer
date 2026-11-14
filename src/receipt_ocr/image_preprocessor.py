
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError

from .errors import ImageError


class ImagePreprocessor:
    def __init__(self, max_dimension: int = 2000, quality: int = 90):
        self.max_dimension = max_dimension
        self.quality = quality

    def preprocess(self, image_bytes: bytes) -> tuple[bytes, str]:
        try:
            with Image.open(BytesIO(image_bytes)) as image:

                # Correct orientation using EXIF metadata.
                image = ImageOps.exif_transpose(image)

                # Use the first frame for animated images.
                image.seek(0)

                # Convert transparent images to a white background.
                if image.mode in ("RGBA", "LA") or "transparency" in image.info:
                    image = image.convert("RGBA")
                    background = Image.new("RGB", image.size, "white")
                    background.paste(image, mask=image.getchannel("A"))
                    image = background
                else:
                    image = image.convert("RGB")

                # Resize only if an image dimension is too large.
                image.thumbnail(
                    (self.max_dimension, self.max_dimension),
                    Image.Resampling.LANCZOS,
                )

                # Standardize the output format to JPEG.
                output = BytesIO()
                image.save(
                    output,
                    format="JPEG",
                    quality=self.quality,
                    optimize=True,
                )

                return output.getvalue(), "image/jpeg"

        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise ImageError(
                f"Unable to preprocess image: {exc}"
            ) from exc
