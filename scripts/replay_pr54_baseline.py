#!/usr/bin/env python3
"""Run and record the pinned PR 54 verification commands."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time


PINNED_COMMIT = "7210de7d0f9ccaeb64c3f60f188419e02be08d95"
SOURCE_PATHS = (
    "README.md",
    "Makefile",
    ".github/workflows/pr54-baseline.yml",
    "docs/research/pr54-integration-map.md",
    "scripts/replay_pr54_baseline.py",
    "tests/test_pr54_baseline.py",
    "research/skip-clones/SOURCE.json",
    "research/skip-clones/PROOF.md",
    "research/skip-clones/clone-jobs-23.json",
    "research/skip-clones/clone-jobs-25.json",
    "research/skip-clones/producer.py",
    "research/skip-clones/witness.py",
    "research/skip-clones/certificate.json",
    "research/skip-clones/producer-receipt.json",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def research_summary(root: Path) -> dict[str, int | str]:
    certificate = json.loads((root / "research/skip-clones/certificate.json").read_text())
    producer = json.loads((root / "research/skip-clones/producer-receipt.json").read_text())
    return {
        "R23": producer["23"]["full_timeline"]["roles"],
        "R25": producer["25"]["full_timeline"]["roles"],
        "W": certificate["bit"]["counts"]["W"],
        "kappa": certificate["kappa"],
    }


def write_receipt(path: Path, receipt: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def run_check(root: Path, run_dir: Path, command: list[str], timeout: int) -> dict:
    name = command[-1].replace(" ", "-")
    log_path = run_dir / f"{name}.log"
    started_at = datetime.now(timezone.utc)
    started = time.monotonic()
    timed_out = False
    with log_path.open("wb") as log:
        log.write(("$ " + " ".join(command) + "\n").encode())
        try:
            process = subprocess.Popen(
                command,
                cwd=root,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                status = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait()
                status = 124
                log.write(f"\nTimed out after {timeout} seconds.\n".encode())
        except OSError as error:
            status = 127
            log.write(f"\nCould not start command: {error}\n".encode())
        log.write(f"\nExit status: {status}\n".encode())
    return {
        "command": command,
        "started_at_utc": started_at.isoformat(),
        "duration_seconds": round(time.monotonic() - started, 3),
        "exit_status": status,
        "timed_out": timed_out,
        "log": log_path.name,
        "log_sha256": sha256(log_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="also run make verify")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--output-root", type=Path, default=Path("build/pr54-baseline"))
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be positive")

    root = Path(__file__).resolve().parents[1]
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", PINNED_COMMIT, "HEAD"], cwd=root
    ).returncode:
        parser.error(f"HEAD must descend from pinned candidate {PINNED_COMMIT}")

    output_root = args.output_root if args.output_root.is_absolute() else root / args.output_root
    run_dir = output_root / datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%S%fZ")
    run_dir.mkdir(parents=True)
    receipt_path = run_dir / "receipt.json"
    commands = [["make", "skip-clones-verify"]]
    if args.full:
        commands.append(["make", "verify"])

    status = git(root, "status", "--porcelain")
    receipt = {
        "schema_version": 1,
        "candidate": {
            "issue_number": 5,
            "pull_request": 54,
            "pinned_commit": PINNED_COMMIT,
        },
        "checkout": {
            "branch": git(root, "rev-parse", "--abbrev-ref", "HEAD"),
            "head": git(root, "rev-parse", "HEAD"),
            "tree": git(root, "rev-parse", "HEAD^{tree}"),
            "worktree_status_sha256": hashlib.sha256(status.encode()).hexdigest(),
        },
        "environment": {
            "started_at_utc": datetime.now(timezone.utc).isoformat(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": sys.version,
            "cpu_count": os.cpu_count(),
            "cxx": shutil.which("g++") or shutil.which("c++"),
            "disk_free_bytes": shutil.disk_usage(root).free,
        },
        "plan": {"commands": commands, "timeout_seconds_per_command": args.timeout_seconds},
        "research_result": research_summary(root),
        "source_sha256": {},
        "checks": [],
    }

    def refresh_hashes() -> None:
        receipt["source_sha256"] = {
            name: sha256(root / name) for name in SOURCE_PATHS if (root / name).is_file()
        }

    refresh_hashes()
    write_receipt(receipt_path, receipt)
    print(f"Receipt directory: {run_dir.relative_to(root)}", flush=True)
    failed = False
    for command in commands:
        check = run_check(root, run_dir, command, args.timeout_seconds)
        receipt["checks"].append(check)
        receipt["environment"]["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        receipt["research_result"] = research_summary(root)
        refresh_hashes()
        write_receipt(receipt_path, receipt)
        print(
            f"{'PASS' if check['exit_status'] == 0 else 'FAIL'}: "
            f"{' '.join(command)} in {check['duration_seconds']}s "
            f"(exit {check['exit_status']}); log: {check['log']}",
            flush=True,
        )
        failed |= check["exit_status"] != 0
    status_after = git(root, "status", "--porcelain")
    receipt["checkout"]["worktree_status_after"] = status_after.splitlines()
    receipt["checkout"]["worktree_status_after_sha256"] = hashlib.sha256(
        status_after.encode()
    ).hexdigest()
    receipt["environment"]["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    refresh_hashes()
    write_receipt(receipt_path, receipt)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
