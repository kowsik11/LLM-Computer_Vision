"""Placeholder evaluation harness wiring.

This script sketches how the 30-run evaluation suite will be orchestrated once
the executor and judge components are feature-complete.
"""

import asyncio
from dataclasses import dataclass
from typing import Callable, List

import httpx


@dataclass
class EvalCase:
    name: str
    goal: str
    site_policy: List[str]
    success_check: Callable[[dict], bool]


EVAL_CASES = [
    EvalCase(
        name="SiteA CSV Export",
        goal="Download last 30 days report as CSV from site A",
        site_policy=["https://site-a.example"],
        success_check=lambda run: run.get("status") == "completed",
    ),
    EvalCase(
        name="SiteB Pagination Scrape",
        goal="Search, filter, and scrape 50 items from site B",
        site_policy=["https://site-b.example"],
        success_check=lambda run: run.get("metrics", {}).get("rows", 0) >= 50,
    ),
    EvalCase(
        name="SiteC Settings Update",
        goal="Update notification settings on site C and verify confirmation",
        site_policy=["https://site-c.example"],
        success_check=lambda run: run.get("metrics", {}).get("confirmation_seen", False),
    ),
]


async def submit_job(client: httpx.AsyncClient, case: EvalCase) -> dict:
    response = await client.post(
        "/v1/jobs",
        json={"goal": case.goal, "site_policy": case.site_policy},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


async def main() -> None:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        for case in EVAL_CASES:
            job = await submit_job(client, case)
            print(f"Submitted job {job['id']} for {case.name}")


if __name__ == "__main__":
    asyncio.run(main())

