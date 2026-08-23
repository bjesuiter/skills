#!/usr/bin/env python3
"""Reproducible test and comparison harness for SVG authoring skills."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]
CASES_DIR = LAB_DIR / "cases"
SCHEMAS_DIR = LAB_DIR / "schemas"
RUNS_DIR = LAB_DIR / "runs"
PROPOSALS_DIR = LAB_DIR / "proposals"
EXAMPLES_DIR = LAB_DIR / "examples"
DEFAULT_SKILL = REPO_ROOT / "skills" / "jb-svg" / "SKILL.md"


@dataclass(frozen=True)
class Candidate:
    name: str
    source: Path | None
    skill_text: str


def utc_stamp() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M%S")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-.")
    if not cleaned:
        raise ValueError(f"Cannot derive a safe name from {value!r}")
    return cleaned


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_cases(selected: list[str] | None = None) -> list[dict[str, Any]]:
    cases = [load_json(path) for path in sorted(CASES_DIR.glob("*.json"))]
    for case in cases:
        missing = {"id", "title", "prompt", "expect"} - set(case)
        if missing:
            raise ValueError(f"Case is missing fields {sorted(missing)}: {case}")
    if not selected or "all" in selected:
        return cases
    wanted = set(selected)
    found = {case["id"] for case in cases}
    unknown = wanted - found
    if unknown:
        raise ValueError(f"Unknown case(s): {', '.join(sorted(unknown))}")
    return [case for case in cases if case["id"] in wanted]


def parse_candidate(spec: str) -> Candidate:
    if "=" not in spec:
        raise ValueError("Candidates use NAME=PATH or NAME=none")
    raw_name, raw_source = spec.split("=", 1)
    name = slug(raw_name)
    if raw_source == "none":
        return Candidate(name, None, "No additional SVG-specific skill is available.")
    source = Path(raw_source).expanduser().resolve()
    if source.is_dir():
        source = source / "SKILL.md"
    if not source.is_file():
        raise ValueError(f"Candidate does not contain a readable SKILL.md: {source}")
    return Candidate(name, source, source.read_text(encoding="utf-8"))


def default_candidates(for_battle: bool) -> list[Candidate]:
    candidates = [parse_candidate(f"jb-svg={DEFAULT_SKILL}")]
    if for_battle:
        candidates.append(parse_candidate("baseline=none"))
    return candidates


def resolve_candidates(specs: list[str] | None, for_battle: bool) -> list[Candidate]:
    candidates = (
        [parse_candidate(spec) for spec in specs]
        if specs
        else default_candidates(for_battle)
    )
    names = [candidate.name for candidate in candidates]
    if len(names) != len(set(names)):
        raise ValueError("Candidate names must be unique")
    if for_battle and len(candidates) < 2:
        raise ValueError("Battle mode requires at least two candidates")
    return candidates


def generation_prompt(candidate: Candidate, case: dict[str, Any]) -> str:
    return f"""You are participating in a controlled SVG skill lab.

Follow only the candidate skill below as SVG-specific guidance. Complete the case without reading or invoking installed SVG skills. Return JSON matching the supplied schema. The `svg` field must contain one complete SVG with no Markdown fence. The `notes` field must briefly explain decisions and known limitations. Do not write files or call tools.

<candidate-skill name="{candidate.name}">
{candidate.skill_text}
</candidate-skill>

<case id="{case["id"]}">
{case["prompt"]}
</case>
"""


def invoke_codex(
    prompt: str,
    schema: Path,
    *,
    model: str | None,
    images: list[Path] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("codex is not on PATH")
    with tempfile.TemporaryDirectory(prefix="jb-svg-lab-") as raw_temp:
        temp = Path(raw_temp)
        response_path = temp / "response.json"
        command = [
            codex,
            "exec",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "--disable",
            "skill_search",
            "--disable",
            "plugins",
            "--disable",
            "apps",
            "--output-schema",
            str(schema.resolve()),
            "--output-last-message",
            str(response_path),
            "--color",
            "never",
        ]
        if model:
            command.extend(["--model", model])
        for image_path in images or []:
            command.extend(["--image", str(image_path.resolve())])
        command.append("-")
        completed = subprocess.run(
            command,
            cwd=temp,
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
        )
        logs = {
            "command": command,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        if completed.returncode != 0:
            raise RuntimeError(
                f"Codex exited {completed.returncode}: {completed.stderr.strip() or completed.stdout.strip()}"
            )
        if not response_path.is_file():
            raise RuntimeError("Codex did not create its structured response")
        return load_json(response_path), logs


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def check_svg(svg_text: str, expect: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as error:
        record("xml", False, str(error))
        return {"passed": 0, "total": 1, "checks": checks}

    record("xml", True, "Markup parses as XML")
    record("root", local_name(root.tag) == "svg", "Root element is <svg>")
    view_box = root.attrib.get("viewBox", "").split()
    valid_view_box = len(view_box) == 4
    if valid_view_box:
        try:
            valid_view_box = float(view_box[2]) > 0 and float(view_box[3]) > 0
        except ValueError:
            valid_view_box = False
    record("viewBox", valid_view_box, "viewBox has four values and positive dimensions")

    elements = list(root.iter())
    ids = [element.attrib["id"] for element in elements if "id" in element.attrib]
    record("unique-ids", len(ids) == len(set(ids)), "Every id is unique")
    references = set(re.findall(r"url\(#([^)]+)\)", svg_text))
    references.update(re.findall(r"(?:href|xlink:href)=[\"']#([^\"']+)", svg_text))
    missing_references = sorted(references - set(ids))
    record(
        "resolved-references",
        not missing_references,
        "All local references resolve"
        if not missing_references
        else f"Missing ids: {missing_references}",
    )

    has_script = any(local_name(element.tag) == "script" for element in elements)
    has_handlers = any(
        attribute.lower().startswith("on")
        for element in elements
        for attribute in element.attrib
    )
    record(
        "passive-markup",
        not has_script and not has_handlers,
        "No scripts or event-handler attributes",
    )

    external_refs = re.findall(r"(?:href|xlink:href)=[\"'](https?://[^\"']+)", svg_text)
    record(
        "self-contained", not external_refs, "No remote image or document references"
    )

    usage = expect.get("usage")
    if usage == "standalone":
        record(
            "namespace",
            'xmlns="http://www.w3.org/2000/svg"' in svg_text
            or "xmlns='http://www.w3.org/2000/svg'" in svg_text,
            "Standalone SVG declares the SVG namespace",
        )
    elif usage == "inline-decorative":
        record(
            "decorative-a11y",
            root.attrib.get("aria-hidden") == "true"
            and root.attrib.get("focusable") == "false",
            "Decorative SVG is hidden from assistive technology and cannot take focus",
        )
    elif usage == "inline-meaningful":
        labelled_by = root.attrib.get("aria-labelledby", "").split()
        has_label = bool(root.attrib.get("aria-label")) or bool(
            labelled_by and set(labelled_by) <= set(ids)
        )
        has_title = any(local_name(element.tag) == "title" for element in elements)
        record(
            "meaningful-a11y",
            root.attrib.get("role") == "img" and has_label and has_title,
            "Meaningful SVG has role=img, a title, and a resolvable accessible name",
        )

    if expect.get("currentColor"):
        record(
            "currentColor",
            "currentColor" in svg_text,
            "Inline icon inherits its host color",
        )
    if expect.get("reducedMotion"):
        record(
            "reduced-motion",
            "prefers-reduced-motion" in svg_text,
            "Animated SVG contains an explicit reduced-motion path",
        )

    passed = sum(1 for check in checks if check["passed"])
    return {"passed": passed, "total": len(checks), "checks": checks}


def render_svg(svg_path: Path, png_path: Path) -> dict[str, Any]:
    magick = shutil.which("magick")
    if not magick:
        return {"rendered": False, "detail": "ImageMagick is not installed"}
    completed = subprocess.run(
        [
            magick,
            "-background",
            "white",
            str(svg_path),
            "-resize",
            "768x768",
            "-alpha",
            "remove",
            "-alpha",
            "off",
            str(png_path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "rendered": completed.returncode == 0,
        "detail": completed.stderr.strip()
        or completed.stdout.strip()
        or "Rendered with ImageMagick",
    }


def create_run(
    candidates: list[Candidate], cases: list[dict[str, Any]], model: str | None
) -> Path:
    run_dir = RUNS_DIR / utc_stamp()
    suffix = 1
    while run_dir.exists():
        run_dir = RUNS_DIR / f"{utc_stamp()}-{suffix}"
        suffix += 1
    run_dir.mkdir(parents=True)
    manifest: dict[str, Any] = {
        "id": run_dir.name,
        "created_at": dt.datetime.now(dt.UTC).isoformat(),
        "model": model,
        "cases": [case["id"] for case in cases],
        "candidates": {},
    }
    for candidate in candidates:
        snapshot_path = run_dir / "candidates" / candidate.name / "SKILL.md"
        write_text(snapshot_path, candidate.skill_text)
        manifest["candidates"][candidate.name] = {
            "source": str(candidate.source) if candidate.source else None,
            "snapshot": str(snapshot_path.relative_to(run_dir)),
            "sha256": hashlib.sha256(candidate.skill_text.encode()).hexdigest(),
        }
    write_json(run_dir / "manifest.json", manifest)
    return run_dir


def artifact_dir(run_dir: Path, case_id: str, candidate_name: str) -> Path:
    return run_dir / "artifacts" / case_id / candidate_name


def candidate_labels(manifest: dict[str, Any], case_id: str) -> dict[str, str]:
    names = list(manifest["candidates"])
    rng = random.Random(f"{manifest['id']}:{case_id}")
    rng.shuffle(names)
    return {name: chr(65 + index) for index, name in enumerate(names)}


def generate_run(
    candidates: list[Candidate],
    cases: list[dict[str, Any]],
    *,
    model: str | None,
    dry_run: bool,
) -> Path:
    run_dir = create_run(candidates, cases, model)
    for case in cases:
        for candidate in candidates:
            target = artifact_dir(run_dir, case["id"], candidate.name)
            prompt = generation_prompt(candidate, case)
            write_text(target / "prompt.md", prompt)
            if dry_run:
                continue
            print(f"generate: {case['id']} × {candidate.name}", flush=True)
            try:
                response, logs = invoke_codex(
                    prompt,
                    SCHEMAS_DIR / "generation.schema.json",
                    model=model,
                )
                svg_text = response["svg"].strip() + "\n"
                write_text(target / "output.svg", svg_text)
                write_text(target / "notes.md", response["notes"].strip() + "\n")
                write_json(target / "codex.json", logs)
                check = check_svg(svg_text, case["expect"])
                render = render_svg(target / "output.svg", target / "preview.png")
                write_json(target / "check.json", {**check, "render": render})
            except (
                OSError,
                RuntimeError,
                ValueError,
                KeyError,
                json.JSONDecodeError,
            ) as error:  # Keep a multi-case run useful after one failure.
                write_text(target / "error.txt", f"{type(error).__name__}: {error}\n")
                print(
                    f"failed: {case['id']} × {candidate.name}: {error}", file=sys.stderr
                )
    build_gallery(run_dir)
    return run_dir


def build_gallery(run_dir: Path) -> Path:
    manifest = load_json(run_dir / "manifest.json")
    cards: list[str] = []
    for case_id in manifest["cases"]:
        labels = candidate_labels(manifest, case_id)
        cards.append(f'<section><h2>{html.escape(case_id)}</h2><div class="grid">')
        for candidate_name in manifest["candidates"]:
            target = artifact_dir(run_dir, case_id, candidate_name)
            output = target / "output.svg"
            if output.is_file():
                check = load_json(target / "check.json")
                score = f"{check['passed']}/{check['total']} structural checks"
                relative = output.relative_to(run_dir)
                preview = f'<iframe title="{html.escape(candidate_name)}" src="{html.escape(str(relative))}"></iframe>'
            else:
                score = "No output"
                preview = '<div class="missing">No generated SVG</div>'
            cards.append(
                f"<article><h3>Entry {labels[candidate_name]}</h3>{preview}<p>{html.escape(score)}</p></article>"
            )
        identity = "".join(
            f"<li>{label}: {html.escape(name)}</li>"
            for name, label in sorted(labels.items(), key=lambda item: item[1])
        )
        cards.append(
            f"</div><details><summary>Reveal candidate identities</summary><ul>{identity}</ul></details></section>"
        )
    document = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>JB SVG lab {html.escape(manifest["id"])}</title>
<style>
  :root {{ color-scheme: light dark; font-family: ui-sans-serif, system-ui, sans-serif; }}
  body {{ max-width: 1440px; margin: 0 auto; padding: 32px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
  article {{ border: 1px solid color-mix(in srgb, currentColor 22%, transparent); padding: 16px; }}
  iframe, .missing {{ box-sizing: border-box; width: 100%; height: 320px; border: 0; background: #fff; }}
  .missing {{ display: grid; place-items: center; color: #777; }}
  h2 {{ margin-top: 48px; }}
</style>
<h1>JB SVG lab</h1>
<p>Run {html.escape(manifest["id"])}. Compare shape, spacing, clarity, and behavior before revealing candidate identities or reading evaluator output.</p>
{"".join(cards)}
</html>
"""
    gallery_path = run_dir / "gallery.html"
    write_text(gallery_path, document)
    return gallery_path


def evaluation_prompt(
    case: dict[str, Any],
    labelled: list[tuple[str, str, Path]],
    rubric: str,
) -> str:
    entries = []
    for label, _, target in labelled:
        svg_text = (target / "output.svg").read_text(encoding="utf-8")
        check = load_json(target / "check.json")
        entries.append(
            f'<entry label="{label}">\n<svg>\n{svg_text}\n</svg>\n'
            f"<structural-checks>{json.dumps(check, ensure_ascii=False)}</structural-checks>\n</entry>"
        )
    image_map = ", ".join(
        f"image {index + 1} = {label}" for index, (label, _, _) in enumerate(labelled)
    )
    return f"""Act as a strict SVG craft evaluator. The candidate identities are hidden. Judge the supplied outputs against the case and rubric. Attached previews follow this order: {image_map}. Use markup evidence when a preview cannot reveal semantics or responsive behavior. Return JSON matching the supplied schema. Scores are integers from 0 to each rubric maximum and total is 0 to 100. Rank every label exactly once. Do not reward verbose notes.

<case>
{case["prompt"]}
</case>

<rubric>
{rubric}
</rubric>

{"".join(entries)}
"""


def evaluate_run(run_dir: Path, *, model: str | None) -> None:
    manifest = load_json(run_dir / "manifest.json")
    cases_by_id = {case["id"]: case for case in load_cases()}
    rubric = (LAB_DIR / "rubric.md").read_text(encoding="utf-8")
    evaluations: list[dict[str, Any]] = []
    for case_id in manifest["cases"]:
        available = [
            candidate_name
            for candidate_name in manifest["candidates"]
            if (artifact_dir(run_dir, case_id, candidate_name) / "output.svg").is_file()
        ]
        if len(available) < 2:
            print(
                f"skip evaluation: {case_id} has fewer than two outputs",
                file=sys.stderr,
            )
            continue
        labels = candidate_labels(manifest, case_id)
        labelled = sorted(
            [
                (
                    labels[candidate_name],
                    candidate_name,
                    artifact_dir(run_dir, case_id, candidate_name),
                )
                for candidate_name in available
            ],
            key=lambda item: item[0],
        )
        images = [target / "preview.png" for _, _, target in labelled]
        usable_images = images if all(path.is_file() for path in images) else []
        prompt = evaluation_prompt(cases_by_id[case_id], labelled, rubric)
        print(f"evaluate: {case_id}", flush=True)
        response, logs = invoke_codex(
            prompt,
            SCHEMAS_DIR / "evaluation.schema.json",
            model=model,
            images=usable_images,
        )
        identity = {label: candidate_name for label, candidate_name, _ in labelled}
        response["identity"] = identity
        response["case"] = case_id
        for score in response["scores"]:
            score["candidate"] = identity.get(score["label"], "unknown")
        response["ranking_candidates"] = [
            identity.get(label, "unknown") for label in response["ranking"]
        ]
        write_json(run_dir / "evaluations" / f"{case_id}.json", response)
        write_json(run_dir / "evaluations" / f"{case_id}.codex.json", logs)
        evaluations.append(response)
    write_summary(run_dir, evaluations)


def write_summary(run_dir: Path, evaluations: list[dict[str, Any]]) -> None:
    totals: dict[str, list[int]] = {}
    lines = [f"# Battle summary: {run_dir.name}", ""]
    for evaluation in evaluations:
        lines.extend([f"## {evaluation['case']}", "", evaluation["verdict"], ""])
        for score in sorted(
            evaluation["scores"], key=lambda item: item["total"], reverse=True
        ):
            totals.setdefault(score["candidate"], []).append(score["total"])
            lines.append(f"- {score['candidate']}: {score['total']}/100")
        lines.append("")
    lines.extend(["## Aggregate", ""])
    aggregate = []
    for candidate, values in totals.items():
        average = round(sum(values) / len(values), 1)
        aggregate.append(
            {"candidate": candidate, "average": average, "cases": len(values)}
        )
    for item in sorted(aggregate, key=lambda entry: entry["average"], reverse=True):
        lines.append(
            f"- {item['candidate']}: {item['average']}/100 across {item['cases']} case(s)"
        )
    write_text(run_dir / "summary.md", "\n".join(lines) + "\n")
    write_json(
        run_dir / "summary.json", {"aggregate": aggregate, "evaluations": evaluations}
    )


def improve_candidate(run_dir: Path, candidate_name: str, *, model: str | None) -> Path:
    manifest = load_json(run_dir / "manifest.json")
    if candidate_name not in manifest["candidates"]:
        raise ValueError(f"Unknown candidate {candidate_name!r}")
    snapshot = run_dir / manifest["candidates"][candidate_name]["snapshot"]
    evidence: dict[str, Any] = {"checks": {}, "evaluations": {}}
    for case_id in manifest["cases"]:
        check_path = artifact_dir(run_dir, case_id, candidate_name) / "check.json"
        if check_path.is_file():
            evidence["checks"][case_id] = load_json(check_path)
        evaluation_path = run_dir / "evaluations" / f"{case_id}.json"
        if evaluation_path.is_file():
            evidence["evaluations"][case_id] = load_json(evaluation_path)
    prompt = f"""Revise the SVG skill using only recurring, evidenced weaknesses in the lab results. Preserve useful existing guidance. Reject one-off aesthetic preferences and avoid growing the skill without a behavioral reason. Return a complete revised SKILL.md plus a concise summary and change list. Do not edit files or call tools.

<current-skill>
{snapshot.read_text(encoding="utf-8")}
</current-skill>

<lab-evidence>
{json.dumps(evidence, ensure_ascii=False)}
</lab-evidence>
"""
    response, logs = invoke_codex(
        prompt,
        SCHEMAS_DIR / "improvement.schema.json",
        model=model,
    )
    proposal_dir = PROPOSALS_DIR / f"{utc_stamp()}-{slug(candidate_name)}"
    write_text(proposal_dir / "SKILL.md", response["skill_markdown"].strip() + "\n")
    rationale = (
        "# Improvement proposal\n\n"
        + response["summary"].strip()
        + "\n\n## Changes\n\n"
    )
    rationale += "\n".join(f"- {change}" for change in response["changes"]) + "\n"
    write_text(proposal_dir / "RATIONALE.md", rationale)
    write_json(proposal_dir / "codex.json", logs)
    return proposal_dir


def promote_examples(
    run_dir: Path, candidate_name: str, selected_cases: list[str] | None
) -> list[Path]:
    manifest = load_json(run_dir / "manifest.json")
    if candidate_name not in manifest["candidates"]:
        raise ValueError(f"Unknown candidate {candidate_name!r}")
    case_ids = (
        manifest["cases"]
        if not selected_cases or "all" in selected_cases
        else selected_cases
    )
    promoted: list[Path] = []
    for case_id in case_ids:
        source = artifact_dir(run_dir, case_id, candidate_name) / "output.svg"
        if not source.is_file():
            raise ValueError(f"No SVG output for {case_id} × {candidate_name}")
        destination = EXAMPLES_DIR / f"{slug(case_id)}--{slug(candidate_name)}.svg"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        promoted.append(destination)
    build_examples_gallery()
    return promoted


def build_examples_gallery() -> Path:
    svgs = sorted(EXAMPLES_DIR.glob("*.svg"))
    cards = "".join(
        f'<article><h2>{html.escape(path.stem)}</h2><iframe src="{html.escape(path.name)}"></iframe></article>'
        for path in svgs
    )
    document = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JB SVG examples</title><style>:root{{color-scheme:light dark;font-family:system-ui,sans-serif}}body{{max-width:1200px;margin:auto;padding:32px}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}article{{border:1px solid #8886;padding:16px}}iframe{{width:100%;height:300px;border:0;background:#fff}}</style><h1>JB SVG examples</h1><main>{cards}</main></html>\n"""
    path = EXAMPLES_DIR / "index.html"
    write_text(path, document)
    return path


def doctor() -> int:
    rows = {
        "codex": shutil.which("codex"),
        "magick": shutil.which("magick"),
        "canonical skill": str(DEFAULT_SKILL) if DEFAULT_SKILL.is_file() else None,
        "cases": len(load_cases()),
    }
    for name, value in rows.items():
        print(f"{name}: {value or 'missing'}")
    return 0 if rows["codex"] and rows["canonical skill"] and rows["cases"] else 1


def add_common_run_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--candidate", action="append", help="NAME=PATH or NAME=none; repeatable"
    )
    parser.add_argument("--case", action="append", help="Case id or all; repeatable")
    parser.add_argument("--model", help="Codex model override")
    parser.add_argument(
        "--dry-run", action="store_true", help="Write prompts without model calls"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Check local lab dependencies")
    subparsers.add_parser("list", help="List available cases")

    test_parser = subparsers.add_parser(
        "test", help="Run one or more skills without an AI judge"
    )
    add_common_run_arguments(test_parser)

    battle_parser = subparsers.add_parser(
        "battle", help="Run and blindly compare at least two skills"
    )
    add_common_run_arguments(battle_parser)

    evaluate_parser = subparsers.add_parser(
        "evaluate", help="Evaluate an existing multi-candidate run"
    )
    evaluate_parser.add_argument("run", type=Path)
    evaluate_parser.add_argument("--model")

    improve_parser = subparsers.add_parser(
        "improve", help="Draft a revised skill from run evidence"
    )
    improve_parser.add_argument("run", type=Path)
    improve_parser.add_argument("--candidate", default="jb-svg")
    improve_parser.add_argument("--model")

    promote_parser = subparsers.add_parser(
        "promote", help="Copy selected run outputs into examples"
    )
    promote_parser.add_argument("run", type=Path)
    promote_parser.add_argument("--candidate", required=True)
    promote_parser.add_argument("--case", action="append")

    check_parser = subparsers.add_parser(
        "check", help="Run structural checks on SVG files"
    )
    check_parser.add_argument("svg", type=Path, nargs="+")

    args = parser.parse_args()
    try:
        if args.command == "doctor":
            return doctor()
        if args.command == "list":
            for case in load_cases():
                print(f"{case['id']}: {case['title']}")
            return 0
        if args.command in {"test", "battle"}:
            is_battle = args.command == "battle"
            candidates = resolve_candidates(args.candidate, is_battle)
            cases = load_cases(args.case)
            run_dir = generate_run(
                candidates, cases, model=args.model, dry_run=args.dry_run
            )
            if is_battle and not args.dry_run:
                evaluate_run(run_dir, model=args.model)
            print(run_dir)
            return 0
        if args.command == "evaluate":
            evaluate_run(args.run.resolve(), model=args.model)
            return 0
        if args.command == "improve":
            print(
                improve_candidate(args.run.resolve(), args.candidate, model=args.model)
            )
            return 0
        if args.command == "promote":
            for promoted in promote_examples(
                args.run.resolve(), args.candidate, args.case
            ):
                print(promoted)
            return 0
        if args.command == "check":
            failed = False
            for svg_path in args.svg:
                report = check_svg(
                    svg_path.read_text(encoding="utf-8"), {"usage": "standalone"}
                )
                print(f"{svg_path}: {report['passed']}/{report['total']}")
                for check in report["checks"]:
                    print(
                        f"  {'PASS' if check['passed'] else 'FAIL'} {check['name']}: {check['detail']}"
                    )
                failed = failed or report["passed"] != report["total"]
            return 1 if failed else 0
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
