# LiteLLM Gateway

This directory provides the LLM gateway for the Agentic Trading System.

## Start locally

```bash
uv run litellm --config gateway/config.yaml --port 4000
```

## Start with Docker Compose

```bash
docker compose up --build llm-gateway
```

## Gateway endpoint

The application accesses the gateway using:

```text
http://localhost:4000/v1
```

Do not expose the gateway publicly. Keep provider keys in `.env` or a proper secret manager.