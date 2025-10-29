import asyncio
import json
from pathlib import Path

from executor.runtime.engine import ExecutorEngine
from shared.dsl import ActionProgram


async def main() -> None:
    program_path = Path("program.json")
    if not program_path.exists():
        print("program.json not found; provide a DSL program to execute.")
        return

    with program_path.open("r", encoding="utf-8") as handle:
        raw_program = json.load(handle)

    program = ActionProgram.model_validate(raw_program)

    async with ExecutorEngine() as engine:
        result = await engine.run_program(program)
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())

