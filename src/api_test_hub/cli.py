from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from api_test_hub.cases import (
    generate_pytest_file,
    generate_pytest_project_file,
    load_cases,
)
from api_test_hub.config import load_project
from api_test_hub.core import run_case
from api_test_hub.core.auth import perform_login
from api_test_hub.utils import configure_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="api-test-hub")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Generate pytest file from config")
    gen.add_argument("-c", "--config", required=True, help="Config file path")
    gen.add_argument("-o", "--output", required=True, help="Output pytest file path")

    run = subparsers.add_parser("run", help="Run cases from config file")
    run_group = run.add_mutually_exclusive_group(required=True)
    run_group.add_argument("-c", "--config", help="Config file path")
    run_group.add_argument("-p", "--project", help="Project directory")
    run.add_argument("--log-dir", default="reports", help="Log directory path")
    run.add_argument("--timeout", type=float, default=10.0, help="Request timeout")
    run.add_argument(
        "--no-allure",
        action="store_true",
        help="Run directly without generating Allure results/report",
    )
    run.add_argument(
        "--allure-results",
        default="reports/allure-results",
        help="Allure results directory",
    )
    run.add_argument(
        "--allure-report",
        default="reports/allure-report",
        help="Allure HTML report directory",
    )

    init = subparsers.add_parser("init", help="Generate template project")
    init.add_argument("-o", "--output", required=True, help="Target directory")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        generate_pytest_file(args.config, args.output)
        return 0
    if args.command == "run":
        logger = configure_logging(args.log_dir)
        try:
            if not args.no_allure:
                return _run_with_allure(args)
            if args.project:
                config = load_project(args.project)
            else:
                config, _params = load_cases(args.config)
            context = {}
            perform_login(
                config.base_url,
                config.auth,
                config.variables,
                context,
                timeout=args.timeout,
                logger=logger,
            )
            for case in config.cases:
                run_case(
                    config.base_url,
                    case,
                    timeout=args.timeout,
                    logger=logger,
                    variables=config.variables,
                    context=context,
                    auth=config.auth,
                )
        except Exception as exc:
            print(f"run failed: {exc}", file=sys.stderr)
            return 1
        return 0
    if args.command == "init":
        template_dir = Path(__file__).resolve().parent / "templates" / "init"
        target_dir = Path(args.output)
        if target_dir.exists() and any(target_dir.iterdir()):
            print(f"init failed: target not empty: {target_dir}", file=sys.stderr)
            return 1
        target_dir.mkdir(parents=True, exist_ok=True)
        for root, dirs, files in os.walk(template_dir):
            root_path = Path(root)
            for name in dirs:
                dest_dir = target_dir / root_path.relative_to(template_dir) / name
                dest_dir.mkdir(parents=True, exist_ok=True)
            for name in files:
                src = root_path / name
                dest = target_dir / root_path.relative_to(template_dir) / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest)
        return 0

    parser.error("Unknown command")
    return 1


def _run_with_allure(args: argparse.Namespace) -> int:
    results_dir = Path(args.allure_results)
    report_dir = Path(args.allure_report)
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    report_dir.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir) / "test_generated.py"
        if args.project:
            generate_pytest_project_file(args.project, test_file)
        else:
            config_path = Path(args.config)
            generate_pytest_file(config_path, test_file)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(test_file),
                "-q",
                "--tb=short",
                "--alluredir",
                str(results_dir),
            ],
            check=False,
        )

    if shutil.which("allure") is None:
        print(
            "allure CLI not found; results saved to "
            f"{results_dir}. Install allure to generate HTML.",
            file=sys.stderr,
        )
        return result.returncode

    subprocess.run(
        ["allure", "generate", str(results_dir), "-o", str(report_dir), "--clean"],
        check=True,
    )
    if result.returncode != 0:
        print("tests failed; Allure report still generated.", file=sys.stderr)
    return result.returncode
