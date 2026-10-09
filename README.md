# Agentic Trading System

A paper-first, LangGraph-based multi-agent system for equity-market research,
risk-validated trade proposals, human approval, audit logging, and broker abstraction.

> This project is educational software. It does not provide investment advice.
> Backtest and paper trade before considering any live broker integration.

## Architecture

```text
Market Data
  -> Portfolio Snapshot
  -> Technical / Fundamental / Sentiment Analysis
  -> Consensus / Debate
  -> Trading Signal
  -> Deterministic Risk Validation
  -> Human Approval
  -> Paper or Live Broker Adapter
  -> Audit Store
```

## Local setup

```bash
cp .env.example .env

uv add -r requirements.txt
uv add --dev pytest pytest-asyncio pytest-cov ruff mypy pre-commit ipykernel
uv sync
```

## Start LiteLLM Gateway

```bash
uv run litellm --config gateway/config.yaml --port 4000
```

## Run API

```bash
uv run uvicorn api.main:app --reload
```

Open the API docs at:

```text
http://127.0.0.1:8000/docs
```

## Run a paper analysis

```bash
uv run python scripts/run_analysis.py RELIANCE.NS
```

## Tests

```bash
uv run pytest
uv run ruff check .
uv run mypy src api
```

## Safety defaults

```env
TRADING_MODE=paper
BROKER_PROVIDER=paper
REQUIRE_HUMAN_APPROVAL=true
```

Never put real broker credentials in source code.