# URL Shortener Application

A modern, fast, and secure URL shortener built with Python (FastAPI) on the backend and pure HTML/CSS/JavaScript on the frontend. The application uses PostgreSQL for data storage and is fully containerized using Docker, making it ready for Kubernetes deployment.

## Architecture

This project is separated into two microservices, managed locally via Docker Compose:

1. **Frontend**: A static single-page application served via Nginx. It features a modern, responsive UI with glassmorphism effects without relying on any CSS frameworks like Tailwind or Bootstrap.
2. **Backend**: A REST API built with FastAPI, interacting with a PostgreSQL database via SQLAlchemy and Alembic.

### Folder Structure
```text
.
├── backend/
│   ├── alembic/            # Database migrations
│   ├── app/                # Application source code
│   │   ├── main.py         # Entry point
│   │   ├── config.py       # Environment variables setup
│   │   ├── database.py     # SQLAlchemy setup
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic validation schemas
│   │   ├── routers/        # API route definitions
│   │   └── services/       # Business logic (URL generation, etc.)
│   ├── Dockerfile
│   ├── entrypoint.sh       # Script to run migrations before startup
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Main HTML structure
│   ├── style.css           # Custom modern CSS
│   ├── script.js           # Fetch API logic
│   ├── nginx.conf          # Nginx routing configuration
│   └── Dockerfile
├── docker-compose.yml      # Local orchestration
└── README.md
```

## How to Run Locally

Prerequisites: Make sure you have [Docker](https://www.docker.com/) and Docker Compose installed on your machine.

1. **Start the Application**
   Run the following command at the root of the project:
   ```bash
   docker compose up -d --build
   ```

2. **Access the Services**
   - **Frontend UI**: [http://localhost:8080](http://localhost:8080)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

3. **Stop the Application**
   To stop the containers and remove the networks:
   ```bash
   docker compose down
   ```
   *Note: Add `-v` if you also want to delete the PostgreSQL data volume.*

## API Endpoints

### 1. Create a Short URL
- **Endpoint:** `POST /api/shorten`
- **Body:**
  ```json
  {
      "url": "https://example.com"
  }
  ```
- **Response:**
  ```json
  {
      "short_url": "http://localhost:8000/aB3dE5"
  }
  ```

### 2. Redirect to Original URL
- **Endpoint:** `GET /{short_code}`
- **Description:** Redirects the user to the original URL (HTTP 302).
- **Error:** Returns 404 JSON if the code does not exist.

### 3. Health Check
- **Endpoint:** `GET /health`
- **Response:**
  ```json
  {
      "status": "ok"
  }
  ```

## Environment Variables

Configuration is handled entirely through environment variables. Defaults are provided in the `docker-compose.yml` for local development.

- `DB_HOST`: Hostname of the PostgreSQL database.
- `DB_PORT`: Port of the PostgreSQL database.
- `DB_USER`: Database username.
- `DB_PASSWORD`: Database password.
- `DB_NAME`: Name of the database to use.

These can be effortlessly overridden when deploying to a self-managed Kubernetes cluster using ConfigMaps and Secrets.
