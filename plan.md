## Project: LLM + Computer Vision Browser Automation

### Mission
Build a production-minded agent that translates natural-language goals into deterministic browser action programs (DSL), executes them reliably via Playwright using AX -> DOM -> Vision targeting, heals selectors automatically, and validates success objectively.

### V1 Success Criteria
- >=85% task success across a 30-run evaluation suite (3 workflows, 3 distinct sites).
- <=2 vision resolver invocations per successful run on average.
- Each run produces complete, replayable traces with diffs and artifacts.

### System Pillars
1. **Planner** - LLM that turns goals into DSL, including repair mode emitting minimal diffs.
2. **Executor** - Playwright-based interpreter with AX/DOM/Vision resolvers, retries, self-healing selectors, downloads, and traces.
3. **Perception** - OCR plus grounding fallback (PaddleOCR, GroundingDINO, optional VLM).
4. **Recorder** - Guided capture of AX/DOM/screenshot traces that generalize into DSL.
5. **Judge** - Programmatic success checks (URL, text, download, table, API).
6. **API + UI** - FastAPI backend and React dashboard for jobs, runs, artifacts, and diffs.

### Targeting Policy
Prefer Accessibility roles and names, then stable DOM attributes or text, and rely on Vision only as a last resort. Persist ranked selector bundles with success decay and site hashing.

### Architecture Components
- **Automation Runtime:** Playwright (Python) with CDP for downloads and network capture.
- **Backend:** FastAPI + Postgres (SQLModel/SQLAlchemy), Redis cache/locks, MinIO/S3 artifacts.
- **Telemetry:** OpenTelemetry feeding Prometheus and Grafana.
- **Packaging:** Docker Compose orchestration (`make up`).

### Data Contract Highlights
- Postgres tables: `jobs`, `runs`, `steps`, `artifacts`, `selector_bundles`.
- Object storage for screenshots, HAR, and downloads.
- Config: allowed domains, VLM provider, budgets, timeouts, secrets vault.

### Evaluation Plan
- Metrics: TSR, flakiness, mean time to recovery after DOM change, cost per run, resolver usage mix, vision call rate.
- Eval suite: (1) Auth plus CSV export, (2) Search/filter/paginate and scrape 50 items, (3) Settings change with confirmation.
- Nightly drift runs with dashboard visualizations.

### Roadmap (8 Weeks)
- **Weeks 1-2:** DSL schemas, executor primitives (navigate/click/fill/wait), downloads, traces, success checks. Ship one end-to-end workflow.
- **Weeks 3-4:** Selector bundles with AX/DOM/Vision ranking, OCR fallback, heuristic ranker, evaluation harness baseline.
- **Weeks 5-6:** Repair mode planner, recorder generalization, widget playbooks (date picker, React-select, table export, infinite scroll).
- **Weeks 7-8:** Iframe and shadow DOM support, cost/latency budgeting, RBAC plus secrets, polish and documentation.

### Deliverables
- Docker Compose stack (backend, executor, UI, DB, MinIO).
- OpenAPI plus DSL reference docs.
- Evaluation report with metrics over 30 runs.
- Demo video and representative artifacts.

### Stretch Goals (Post-V1)
- Learned selector ranker, multi-tab orchestration, human-in-the-loop annotation for selector bundles, expanded widget playbooks, viewport canary monitors.

