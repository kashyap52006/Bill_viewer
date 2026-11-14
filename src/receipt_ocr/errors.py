class ReceiptOCRError(Exception):
    """Base exception for receipt OCR failures."""


class ConfigurationError(ReceiptOCRError):
    """Raised when provider configuration is missing or invalid."""


class ImageError(ReceiptOCRError):
    """Raised when an input image cannot be read or is unsupported."""


class ProviderError(ReceiptOCRError):
    """Raised when the language-model provider request fails."""


class ResponseError(ReceiptOCRError):
    """Raised when the provider returns no usable response."""


class ResponseParseError(ReceiptOCRError):
    """Raised when a provider response is not valid receipt JSON."""
