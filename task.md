## Task Backlog (Initial)

### Foundational Setup
- [ ] Repo scaffolding (`backend/`, `executor/`, `planner/`, `ui/`, `infra/`) and shared configs.
- [ ] Define DSL Pydantic schemas + JSONSchema export + validation middleware.
- [ ] Base FastAPI service skeleton with health checks and config loading.

### Executor (Playwright) Core
- [ ] Implement primitives: `navigate`, `click`, `fill`, `wait_for`, `download` handling.
- [ ] AX resolver (role/name) with visibility and interactability gating.
- [ ] DOM resolver supporting attribute whitelist, text hashing, `nearText`.
- [ ] Vision resolver integration (PaddleOCR + GroundingDINO) with crop cache and pHash.
- [ ] Candidate ranker interface + heuristic scoring (AX -> DOM -> Vision ordering).
- [ ] Selector bundle persistence + success decay/site hash updates.

### Planner & Recorder
- [ ] Planner endpoint (`/v1/plan`) with prompt skeleton; outputs YAML DSL only.
- [ ] Repair endpoint (`/v1/repair`) emitting minimal diff patches.
- [ ] Recorder that captures manual Playwright sessions -> generalized DSL trace.

### Tracing & Judging
- [ ] Trace pipeline: before/after screenshots, diff overlay, AX/DOM snippets, artifact storage.
- [ ] Judge library for URL/text/download/table/API checks; run-level aggregation.
- [ ] Metrics pipeline (TSR, retries, resolver mix, cost) surfaced via API.

### UI & Observability
- [ ] Minimal React dashboard: jobs list with status metrics, run detail with step timeline & artifacts.
- [ ] Artifact viewer, selector bundle inspector, retry/approve interactions.
- [ ] Telemetry integration (OpenTelemetry exporters, Prometheus/Grafana dashboards).

### Evaluation & Docs
- [ ] Eval harness for 3 workflow suite with seeds and expected checks; CI integration.
- [ ] Documentation: usage guide, DSL reference, security considerations, runbook.
- [ ] Demo collateral: sample traces, 30-run eval report, walkthrough video outline.
