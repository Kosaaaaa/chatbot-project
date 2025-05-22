# Chatbot Project

A modern chatbot application built with FastAPI and powered by AI language models. This project provides a web-based chat interface that connects to AI models through the OpenAI API or local model servers like Ollama.

## Features

- Real-time chat interface with streaming responses
- Persistent chat history using PostgreSQL
- Support for OpenAI models or local models via Ollama
- RESTful API for chat interactions
- Containerized deployment with Docker and Docker Compose
- Configurable through environment variables

## Technologies Used

- **Backend**: FastAPI, Python 3.13
- **Database**: PostgreSQL, SQLModel, Alembic (migrations)
- **AI Integration**: pydantic-ai, OpenAI API
- **Development**: Poetry (dependency management), Ruff (linting), Pytest (testing)
- **Deployment**: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose
- Python 3.13 (for local development)
- Poetry (for local development)
- Ollama (optional, for local AI model deployment)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatbot-project.git
   cd chatbot-project
   ```

2. Create a `.env` file with your configuration:
   ```
   DB_HOST=db
   DB_PORT=5432
   DB_USER=chatbot
   DB_PASSWORD=chatbot
   DB_NAME=chatbot
   OPENAI_MODEL_NAME=deepseek-r1:1.5b
   OPENAI_PROVIDER_BASE_URL=http://host.docker.internal:11434/v1
   ```

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. Access the application at http://localhost:8000

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatbot-project.git
   cd chatbot-project
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file with your configuration:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=chatbot
   DB_PASSWORD=chatbot
   DB_NAME=chatbot
   OPENAI_MODEL_NAME=deepseek-r1:1.5b
   OPENAI_PROVIDER_BASE_URL=http://127.0.0.1:11434/v1
   ```

4. Start the PostgreSQL database:
   ```bash
   docker-compose up -d db
   ```

5. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

6. Start the application:
   ```bash
   poetry run python -m app.main
   ```

7. Access the application at http://localhost:8000

## Using Ollama for Local AI Models

By default, the application is configured to use Ollama with the Deepseek model. To use Ollama:

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the Deepseek model:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```
3. Start Ollama:
   ```bash
   ollama serve
   ```

## Project Structure

```
chatbot-project/
├── app/                      # Main application package
│   ├── application/          # Application layer
│   │   ├── entrypoints/      # API endpoints and routers
│   │   │   ├── dependencies/ # FastAPI dependencies
│   │   │   └── schema/       # Pydantic models for API
│   │   └── static/           # Static files for frontend
│   ├── domain/               # Domain layer
│   │   └── models/           # Domain models
│   ├── infrastructure/       # Infrastructure layer
│   │   ├── database/         # Database configuration and repositories
│   │   └── logging/          # Logging configuration
│   ├── config.py             # Application configuration
│   ├── dependencies.py       # Application dependencies
│   └── main.py               # Application entry point
├── migrations/               # Alembic migrations
├── tests/                    # Test suite
│   ├── functional/           # Functional tests
│   └── unit/                 # Unit tests
├── Dockerfile                # Docker configuration
├── docker-compose.yaml       # Docker Compose configuration
├── pyproject.toml            # Project metadata and dependencies
└── README.md                 # Project documentation
```

## API Endpoints

- `GET /`: Index page with chat interface
- `GET /chat/`: Get chat history
- `POST /chat/`: Send a message to the chatbot
- `GET /introspections/health`: Health check endpoint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
