# Receipt OCR — AI-Powered Receipt Extraction

An AI-powered receipt processing application built with Python, FastAPI, Google Gemini, and Pillow. It extracts structured information from receipt images and provides both a command-line interface (CLI) and a REST API.

## Features

- **AI-powered extraction:** Uses Google Gemini to understand and extract information from receipt images.
- **Image preprocessing:** Uses Pillow to correct image orientation, handle transparency, resize large images, and convert images to JPEG.
- **REST API:** Provides receipt extraction through FastAPI.
- **Interactive API documentation:** Explore and test endpoints using Swagger UI.
- **Command-line interface:** Process receipt images directly from the terminal.
- **Configurable:** Centralized application settings using environment variables.
- **Docker support:** Build and run the application in a container.
- **Docker Compose:** Manage the application using a Compose configuration.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google Gemini | AI-powered receipt understanding |
| Google Gen AI SDK | Communication with Gemini |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Pillow | Image processing |
| Pydantic / Python schemas | Structured data handling |
| python-dotenv | Local environment configuration |
| Docker | Application containerization |
| Docker Compose | Container orchestration |

## Project Structure

```text
first_bill_viewer/
│
├── images/
│   └── receipt.jpg
│
├── src/
│   └── receipt_ocr/
│       ├── __init__.py
│       ├── api.py
│       ├── cli.py
│       ├── config.py
│       ├── errors.py
│       ├── image_preprocessor.py
│       ├── logging_config.py
│       ├── main_processor.py
│       ├── parser.py
│       ├── prompts.py
│       ├── provider.py
│       └── schemas.py
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Architecture Overview

The application follows a modular architecture:

1. **CLI / API:** Accepts receipt images from the user.
2. **Main Processor:** Coordinates the receipt extraction workflow.
3. **Image Preprocessor:** Prepares images for AI processing.
4. **LLM Provider:** Communicates with Google Gemini.
5. **Prompts and Schemas:** Define extraction instructions and expected structured output.
6. **Parser:** Processes the model response into application data.
7. **Error Handling:** Provides application-specific exception classes.

## Prerequisites

- Python 3.13 or a compatible Python version.
- A Google Gemini API key.
- Git.
- Docker Desktop (for containerized execution).

## Installation — Local Development

### 1. Clone the repository

```bash
git clone https://github.com/kashyap52006/Bill_viewer.git
cd first_bill_viewer
```

Replace the URL with your existing GitHub repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the project

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

If you prefer installing from the requirements file:

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

```env
GEMINI_API_KEY=your_gemini_api_key
DEFAULT_MODEL=your_gemini_model
```

Replace the placeholders with your own configuration.

**Security:** Never commit `.env` or expose your Gemini API key. The `.env.example` file should contain placeholders only.

## Running the Application

### Option 1 — Command-Line Interface

Run the CLI with a receipt image:

```powershell
receipt-ocr images/receipt.jpg
```

The CLI provides a way to process receipts without starting the REST API.

### Option 2 — FastAPI REST API

Start the API server:

```powershell
uvicorn receipt_ocr.api:app --reload
```

Open the following URLs:

| Resource | URL |
|---|---|
| API server | http://localhost:8000 |
| Swagger documentation | http://localhost:8000/docs |
| Health endpoint | http://localhost:8000/health |

### Receipt Extraction

Use the `POST /receipts/extract` endpoint to upload a receipt image.

The easiest way to test it is through Swagger:

1. Open http://localhost:8000/docs.
2. Expand `POST /receipts/extract`.
3. Select **Try it out**.
4. Upload a receipt image.
5. Click **Execute**.
6. Inspect the JSON response.

## Running with Docker

### 1. Build the Docker image

```powershell
docker build -t receipt-ocr:1.0 .
```

### 2. Run the container

```powershell
docker run -d `
  --name receipt-ocr-api `
  -p 8000:8000 `
  --env-file .env `
  receipt-ocr:1.0
```

### 3. Check container status

```powershell
docker ps
```

### 4. View application logs

```powershell
docker logs receipt-ocr-api
```

### 5. Stop and remove the container

```powershell
docker stop receipt-ocr-api
docker rm receipt-ocr-api
```

## Running with Docker Compose

Docker Compose provides a convenient way to build and manage the application.

Start the application:

```powershell
docker compose up --build -d
```

Check service status:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs -f
```

Stop the application:

```powershell
docker compose down
```

After startup, the API is available at:

http://localhost:8000/docs

## Configuration

Application configuration is centralized in `config.py` and supplied through environment variables.

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `DEFAULT_MODEL` | Default Gemini model identifier |

Keep credentials in your local `.env` file or in your deployment platform's secret configuration.

## Error Handling

The application defines custom exceptions to distinguish common failure categories:

- `ReceiptOCRError`
- `ConfigurationError`
- `ImageError`
- `ProviderError`
- `ResponseError`
- `ResponseParseError`

These help separate configuration, image, provider, and response-processing failures.

## Development Notes

- The project uses the `src/` package layout.
- The package can be installed in editable mode using `pip install -e .`.
- The CLI is registered through the project configuration.
- Application settings are centralized.
- Docker configuration is maintained separately from application source code.

## Security Notes

- Do not commit API keys or `.env` files.
- Keep `.env.example` free of real credentials.
- Avoid embedding secrets in Dockerfiles or container images.
- Review environment variables and permissions before deploying publicly.

## Future Improvements

Potential areas for future development:

- Automated unit and integration tests.
- Receipt extraction accuracy evaluation.
- More robust response validation.
- Additional AI provider support.
- Persistent receipt storage and history.
- Authentication and API rate limiting.
- CI/CD automation.
- Cloud deployment and production monitoring.

## License

See the [LICENSE](LICENSE) file in this repository for licensing terms.