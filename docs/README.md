# LLM + Computer Vision Browser Automation

This repository contains the foundational implementation for the production-minded automation agent described in `plan.md`.

## Components

- **backend/** - FastAPI service exposing planner, job/run lifecycle, and artifact endpoints.
- **executor/** - Playwright runtime that interprets the DSL and gathers metrics/artifacts.
- **planner/** - Planner client providing deterministic fallbacks until LLM integration is wired.
- **ui/** - Vite + React dashboard for jobs, runs, and artifacts.
- **infra/** - Docker Compose stack plus helper scripts for local orchestration.
- **shared/** - Pydantic DSL schemas shared across services.

## Quickstart

```bash
make up
```

The command above (defined in `Makefile`) starts Postgres, Redis, MinIO, backend, planner, executor, and UI containers. The UI is available at <http://localhost:5173>, while the backend swagger docs live at <http://localhost:8000/v1/docs>.

## Development Notes

- Python services use Poetry; run `poetry install` inside each service directory.
- The executor currently implements AX/DOM targeting with Playwright APIs. Vision fallback hooks are scaffolded for future integration.
- Planner defaults to a heuristic plan generator to unblock end-to-end testing.
- API schemas rely on the shared DSL package; regenerate JSON schema via `/v1/dsl/schema`.

## Testing

- Backend: `poetry run pytest`
- Executor: `poetry run pytest`
- Planner: `poetry run pytest`
- UI: `npm test` (Jest configuration forthcoming)

## Next Steps

Refer to `task.md` for the prioritized backlog, including selector self-healing, recorder generalization, judge library, evaluation harness, and observability work.
