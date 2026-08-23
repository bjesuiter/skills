import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "lab.py"
SPEC = importlib.util.spec_from_file_location("jb_svg_lab", MODULE_PATH)
assert SPEC and SPEC.loader
lab = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lab
SPEC.loader.exec_module(lab)


class LabTests(unittest.TestCase):
    def test_cases_are_valid(self):
        cases = lab.load_cases()
        self.assertEqual(
            {case["id"] for case in cases},
            {
                "animated-loader",
                "empty-state",
                "icon-button",
                "status-card",
            },
        )

    def test_structural_check_accepts_accessible_inline_icon(self):
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M1 1h2v2z"/></svg>"""
        report = lab.check_svg(
            svg, {"usage": "inline-decorative", "currentColor": True}
        )
        self.assertEqual(report["passed"], report["total"])

    def test_structural_check_reports_missing_reference(self):
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect fill="url(#missing)" width="10" height="10"/></svg>"""
        report = lab.check_svg(svg, {"usage": "standalone"})
        reference_check = next(
            check
            for check in report["checks"]
            if check["name"] == "resolved-references"
        )
        self.assertFalse(reference_check["passed"])

    def test_gallery_isolated_each_svg_in_an_iframe(self):
        with tempfile.TemporaryDirectory() as raw_temp:
            run_dir = Path(raw_temp)
            lab.write_json(
                run_dir / "manifest.json",
                {
                    "id": "test-run",
                    "cases": ["icon-button"],
                    "candidates": {"one": {}, "two": {}},
                },
            )
            for candidate in ("one", "two"):
                target = lab.artifact_dir(run_dir, "icon-button", candidate)
                lab.write_text(target / "output.svg", '<svg viewBox="0 0 1 1"/>')
                lab.write_json(target / "check.json", {"passed": 1, "total": 1})
            gallery = lab.build_gallery(run_dir).read_text(encoding="utf-8")
            self.assertEqual(gallery.count("<iframe"), 2)

    def test_improve_writes_a_separate_proposal(self):
        with tempfile.TemporaryDirectory() as raw_temp:
            temp = Path(raw_temp)
            run_dir = temp / "run"
            snapshot = run_dir / "candidates" / "jb-svg" / "SKILL.md"
            lab.write_text(snapshot, "---\nname: jb-svg\ndescription: Test\n---\n")
            lab.write_json(
                run_dir / "manifest.json",
                {
                    "cases": [],
                    "candidates": {
                        "jb-svg": {"snapshot": "candidates/jb-svg/SKILL.md"}
                    },
                },
            )
            old_proposals = lab.PROPOSALS_DIR
            lab.PROPOSALS_DIR = temp / "proposals"
            response = {
                "summary": "Tighten one rule.",
                "changes": ["Made the completion criterion measurable."],
                "skill_markdown": "---\nname: jb-svg\ndescription: Revised\n---\n",
            }
            try:
                with mock.patch.object(
                    lab, "invoke_codex", return_value=(response, {"exit_code": 0})
                ):
                    proposal = lab.improve_candidate(run_dir, "jb-svg", model=None)
            finally:
                lab.PROPOSALS_DIR = old_proposals
            self.assertTrue((proposal / "SKILL.md").is_file())
            self.assertEqual(
                snapshot.read_text(encoding="utf-8"),
                "---\nname: jb-svg\ndescription: Test\n---\n",
            )


if __name__ == "__main__":
    unittest.main()
