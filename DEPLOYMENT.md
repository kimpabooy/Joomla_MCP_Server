# Deployment Checklist for Joomla MCP Server

A practical deployment guide for running the Joomla MCP Server in local development and production environments.

![icon](static/favicon.ico)

This project has two intended runtime modes:

- Local development: `uv run main.py`
- Production: `docker compose up -d --build`

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/kimpabooy/Joomla_MCP_Server /opt/joomla-mcp-server
cd /opt/joomla-mcp-server
```

### 2. Install uv

```bash
pip install uv
```

### 3. Create `.env`

```bash
cp .env.example .env
```

### 4. Edit `.env`

Set these values for your environment:

- `JOOMLA_SITE_URL`: Joomla site URL
  - Local development: `http://localhost:8080`
  - Production: `https://joomla.example.com`
  - Do not add a trailing slash
- `JOOMLA_API_URL`: Joomla API base URL
  - Local development: `http://localhost:8080/api/index.php/v1`
  - Production: `https://joomla.example.com/api/index.php/v1`
  - Do not add a trailing slash
- `JOOMLA_API_TOKEN`: Joomla API token from System > Users > Create API Token
- `OPENAI_API_KEY`: Your OpenAI API key

## Run the project

### Local development

```bash
uv sync
uv run main.py
```

Open the app at http://127.0.0.1:8000.

### Production

```bash
docker compose up -d --build
```

Open the app at http://localhost:8000 or your server domain.

## Verify the setup

Check that the app starts and the Joomla status endpoint responds:

- Main app: http://localhost:8000
- Status: http://localhost:8000/joomla-status

The status endpoint should return `"online": true` when Joomla is reachable.

## Troubleshooting

### `/joomla-status` returns `online=false`

This usually means the Joomla site URL cannot be reached from the environment you are running in.

- In local development, make sure `JOOMLA_SITE_URL` points to your local Joomla instance.
- In Docker, if Joomla runs on your machine, use `http://host.docker.internal:8080`.
- In production, use the real server domain or IP.

### Tools cannot connect to Joomla

This usually means `JOOMLA_API_URL` is wrong or Joomla is unreachable.

Test the API from inside the container:

```bash
docker compose exec app uv run python -c "import requests; print(requests.get('https://joomla.example.com/api/index.php/v1', timeout=5).status_code)"
```

The request should return a valid Joomla response, not a timeout or 404.

### API token is invalid

If Joomla rejects requests, regenerate the token:

1. Open Joomla admin
2. Go to Users
3. Open your user
4. Open the API Tokens tab
5. Create a new token
6. Update `.env`

## Production notes

- Use `docker compose up -d --build` on the server
- Keep secrets out of Git
- Use HTTPS in production
- Rotate API tokens regularly
