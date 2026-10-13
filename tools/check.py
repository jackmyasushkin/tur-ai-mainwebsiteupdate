"""Check the immutable export and the working copy; never write to Webflow."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from hero_copy_exception import prepare_for_baseline

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "baseline/home/2026-10-12"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check(complete=False, candidate=None):
    errors = []
    manifest = load(BASELINE / "MANIFEST.json")["files"]
    expected_files = {entry["path"] for entry in manifest} | {"MANIFEST.json"}
    actual_files = {str(p.relative_to(BASELINE)) for p in BASELINE.rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts}
    if expected_files != actual_files:
        errors.append("Baseline file set differs from its manifest")
    for entry in manifest:
        path = BASELINE / entry["path"]
        if not path.is_file():
            errors.append("Missing baseline file: " + entry["path"])
            continue
        data = path.read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            errors.append("Baseline checksum mismatch: " + entry["path"])

    source = load(BASELINE / "02_REWRITE_TEMPLATE.json")["items"]
    working = load(candidate or ROOT / "content/home/rewrite.json")
    items = working.get("items") if isinstance(working, dict) else None
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        errors.append("Working copy must contain an items array of objects")
        items = []
    if [i.get("id") for i in items] != [i["id"] for i in source]:
        errors.append("Preserve all 228 source IDs in their original order")

    by_id = {i["id"]: i for i in source}
    pending = []
    counts = {"keep": 0, "rewrite": 0, "hold": 0, "pending": 0}
    for item in items:
        rid = item.get("id")
        original = by_id.get(rid) if isinstance(rid, str) else None
        if original is None:
            errors.append("Unknown or invalid ID: " + str(rid))
            continue
        for key in ("original_text", "max_chars"):
            if item.get(key) != original[key]:
                errors.append(f"{rid}: protected {key} changed")
        segments = item.get("new_segments")
        if not isinstance(segments, list) or any(not isinstance(s, dict) for s in segments):
            errors.append(f"{rid}: new_segments must be an array of objects")
            segments = []
        old_segments = original["new_segments"]
        if len(segments) != len(old_segments):
            errors.append(f"{rid}: preserve the source segment structure")
        for seg, old in zip(segments, old_segments):
            for key in ("source_id", "original_raw", "max_chars"):
                if seg.get(key) != old[key]:
                    errors.append(f"{rid}: protected segment {key} changed")
        action = item.get("action")
        if action is None:
            pending.append(rid)
            counts["pending"] += 1
            # The frozen validator expects a complete set. For draft checks only,
            # substitute keep in memory, after confirming there is no new copy.
            if item.get("new_text") not in (None, "") or any(s.get("new_text") not in (None, "") for s in segments):
                errors.append(f"{rid}: choose an action for proposed copy")
            if not complete:
                item["action"] = "keep"
        elif action in ("keep", "rewrite", "hold"):
            counts[action] += 1
            if action in ("keep", "hold") and any(s.get("new_text") not in (None, "") for s in segments):
                errors.append(f"{rid}: keep/hold must not carry segment replacements")
        else:
            errors.append(f"{rid}: action must be keep, rewrite, hold or null")

    validation = {}
    exceptions = []
    validator_working = working
    if complete and pending:
        errors.append(f"Incomplete editorial decisions: {len(pending)} fields")
    if not errors:
        validator_working, exceptions, exception_errors = prepare_for_baseline(working)
        errors.extend(exception_errors)
    if not errors:
        with tempfile.TemporaryDirectory(prefix="turai-content-check-") as temp:
            candidate_path = Path(temp) / "rewrite.json"
            candidate_path.write_text(json.dumps(validator_working, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(BASELINE / "validate_rewrite.py"), str(candidate_path)],
                text=True, capture_output=True, check=False,
            )
        if result.returncode not in (0, 1):
            errors.append("Source validator failed: " + result.stderr.strip())
        else:
            validation = json.loads(result.stdout)
            errors.extend(validation.get("errors", []))

    return {
        "status": "FAIL" if errors else ("EDITORIAL_LIMITS_PASS" if not pending else "DRAFT_CHECK_PASS"),
        "complete_required": complete,
        "decisions": counts,
        "pending_ids": pending,
        "errors": errors,
        "warnings": validation.get("warnings", []) + (["HOME-003: exact approved H1 uses a documented segment-budget exception; visual review required"] if exceptions else []),
        "approved_copy_exceptions": exceptions,
        "visual_acceptance": "NOT_CHECKED",
        "claim_truth": "NOT_CHECKED",
        "webflow_changed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete", action="store_true", help="Require decisions for every field")
    parser.add_argument("--file", type=Path, help="Validate an alternate rewrite file")
    args = parser.parse_args()
    try:
        report = check(args.complete, args.file)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {"status": "FAIL", "errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(report["status"] == "FAIL")


if __name__ == "__main__":
    sys.exit(main())
