import asyncio
import json
import sys
from pathlib import Path

from planner.service import PlannerClient


async def main() -> None:
    client = PlannerClient()
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        program = await client.plan(
            goal=payload["goal"],
            site_policy=payload["site_policy"],
            secrets=payload.get("secrets"),
            demo_trace_id=payload.get("demo_trace_id"),
        )
        print(program.model_dump_json(indent=2))
    else:
        print("Provide a JSON file containing goal and site_policy fields.")


if __name__ == "__main__":
    asyncio.run(main())

