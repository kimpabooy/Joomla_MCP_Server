# Deployment Checklist for Joomla MCP Server

When deploying to a new environment (server, team member, production)

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/kimpabooy/Joomla_MCP_Server /opt/joomla-mcp-server
cd /opt/joomla-mcp-server
```

### 2. Create Local `.env`

```bash
cp .env.example .env
```

### 3. Edit `.env` with Your Values

- **`JOOMLA_SITE_URL`**: Must match your Joomla installation URL
  - Local: `http://localhost:8080` or `http://host.docker.internal:8080`
  - Server: `https://joomla.example.com`
  - **IMPORTANT**: No trailing slash
- **`JOOMLA_API_URL`**: Base API endpoint
  - Local: `http://localhost:8080/api/index.php/v1`
  - Server: `https://joomla.example.com/api/index.php/v1`
- **`JOOMLA_SITE_CHECK_URL`**: Optional URL used by `/joomla-status`
  - Local prod-compose test: `http://host.docker.internal:8080`
  - Server: usually not needed (leave unset unless you want explicit health target)
- **`JOOMLA_API_TOKEN`**: Get from Joomla System > Users > Create API Token
- **`OPENAI_API_KEY`**: Get from https://platform.openai.com/api-keys

### 4. Choose Deployment Method

#### Option A: Docker (Recommended)

```bash
docker compose up --build
```

Access: http://localhost:8000

#### Option B: Local Python

```bash
pip install uv
uv sync
uv run main.py
```

Access: http://127.0.0.1:8000

### 5. Verify Connection

Open browser and check:

- Main app: `http://localhost:8000`
- Status: `http://localhost:8000/joomla-status` (should show `"online": true`)

## Common Issues

### Status Shows online=false

**Cause:** `JOOMLA_SITE_URL` cannot be reached from inside the container.

**Fix (Local):** Ensure `.env` has:

```
JOOMLA_SITE_URL=http://localhost:8080
```

or `http://host.docker.internal:8080` if Joomla-site runs locally.

If you specifically run `docker-compose.prod.yml` locally, set:

```
JOOMLA_SITE_CHECK_URL=http://host.docker.internal:8080
```

because `localhost` inside the container points to the container itself.

**Fix (Server):** Use your actual domain or server IP:

```
JOOMLA_SITE_URL=https://joomla.example.com
```

### Tools Cannot Connect to Joomla

**Cause:** API URL unreachable or wrong path.

**Debug:** Inside container, run:

```bash
docker compose -f docker-compose.prod.yml exec app uv run python -c "import requests; print(requests.get('https://joomla.example.com/api/index.php/v1', timeout=5).status_code)"
```

Should return API response (not 404 or connection error).

### API Token Invalid

**Cause:** Token has no API permissions or is expired.

**Fix:** Regenerate token:

1. Joomla System > Users
2. Click your user
3. API Tokens tab
4. Create new token
5. Copy and paste into `.env`

## Production Deployment

For production servers, use `docker-compose.prod.yml`:

```bash
docker compose -f docker-compose.prod.yml up -d
```

Key differences:

- No development reload
- No local volume mounts
- Health checks enabled
- Automatic restart on failure
- All env vars read from `.env` only

## Security Notes

- **Never commit `.env`** to Git
- Use HTTPS for `JOOMLA_SITE_URL` on production
- Use strong, rotated API tokens
- Keep OpenAI keys private
- Use environment secrets in CI/CD pipelines
