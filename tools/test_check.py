"""Regression checks for the editorial handoff safeguards, using temporary files."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import check


class EditorialChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "rewrite.json"
        # Tests use the original template, independent of later copy revisions.
        self.template = check.load(check.BASELINE / "02_REWRITE_TEMPLATE.json")

    def validate(self, data, complete=False):
        self.path.write_text(json.dumps(data), encoding="utf-8")
        return check.check(complete, self.path)

    def completed(self):
        data = copy.deepcopy(self.template)
        for item in data["items"]:
            if item["action"] is None:
                item["action"] = "keep"
        return data

    def test_draft_is_not_complete(self):
        result = self.validate(self.template)
        self.assertEqual(result["status"], "DRAFT_CHECK_PASS")
        self.assertEqual(result["decisions"]["pending"], 199)
        self.assertEqual(self.validate(self.template, complete=True)["status"], "FAIL")

    def test_unchanged_complete_set_is_editorial_only(self):
        result = self.validate(self.completed(), complete=True)
        self.assertEqual(result["status"], "EDITORIAL_LIMITS_PASS")
        self.assertEqual(result["visual_acceptance"], "NOT_CHECKED")

    def test_over_budget_rejected(self):
        data = self.completed()
        data["items"][0].update(action="rewrite", new_text="A" * 12)
        result = self.validate(data)
        self.assertTrue(any("exceeds" in e for e in result["errors"]))

    def test_missing_id_rejected(self):
        data = self.completed()
        data["items"].pop()
        self.assertEqual(self.validate(data)["status"], "FAIL")

    def test_original_edit_rejected(self):
        data = self.completed()
        data["items"][0]["original_text"] = "Altered original"
        self.assertEqual(self.validate(data)["status"], "FAIL")

    def test_lost_segment_space_rejected(self):
        data = self.completed()
        item = data["items"][2]
        item.update(action="rewrite", new_text=item["original_text"])
        for segment in item["new_segments"]:
            segment["new_text"] = segment["original_raw"]
        item["new_segments"][0]["new_text"] = item["new_segments"][0]["new_text"].rstrip()
        result = self.validate(data)
        self.assertTrue(any("boundary whitespace" in e for e in result["errors"]))

    def test_proposed_copy_requires_action(self):
        data = copy.deepcopy(self.template)
        data["items"][0]["new_text"] = "Demo"
        self.assertEqual(self.validate(data)["status"], "FAIL")

    def test_hold_cannot_hide_segment_replacement(self):
        data = self.completed()
        data["items"][2]["new_segments"][0]["new_text"] = "New "
        self.assertEqual(self.validate(data)["status"], "FAIL")

    def test_baseline_corruption_rejected(self):
        baseline = Path(self.temp.name) / "baseline"
        shutil.copytree(check.BASELINE, baseline)
        with (baseline / "README.md").open("a") as stream:
            stream.write("\naccidental edit\n")
        with patch.object(check, "BASELINE", baseline):
            result = self.validate(self.completed())
        self.assertTrue(any("checksum mismatch" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
