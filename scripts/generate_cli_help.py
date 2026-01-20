from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "doc" / "CLI_HELP.md"

COMMANDS = [
    ["python", "-m", "api_test_hub", "--help"],
    ["python", "-m", "api_test_hub", "generate", "--help"],
    ["python", "-m", "api_test_hub", "run", "--help"],
    ["python", "-m", "api_test_hub", "init", "--help"],
]


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main() -> None:
    lines = ["# CLI Help", ""]
    for cmd in COMMANDS:
        rendered = " ".join(cmd)
        lines.append(f"## `{rendered}`")
        lines.append("")
        output = run(cmd)
        lines.append("```text")
        lines.append(output)
        lines.append("```")
        lines.append("")

    OUTPUT.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
