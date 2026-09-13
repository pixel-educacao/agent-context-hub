"""Exercise the shipped CLI end to end with synthetic local data only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReferenceCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = Path(self.tmp.name) / "demo.jsonl"
        self.env = dict(os.environ, LEDGER_PATH=str(self.ledger),
                        CONTEXT_LEDGER_TZ="UTC", PYTHONDONTWRITEBYTECODE="1")

    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "reference" / name), *args],
            cwd=self.tmp.name, env=self.env, text=True,
            capture_output=True, timeout=15,
        )

    def produce(self):
        result = self.run_script("example_producer.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_capture_replay_and_query_same_file(self):
        self.assertIn("added=3 skipped(dedupe)=0", self.produce().stdout)
        original = self.ledger.read_bytes()
        self.assertIn("added=0 skipped(dedupe)=3", self.produce().stdout)
        self.assertEqual(original, self.ledger.read_bytes())
        rows = [json.loads(line) for line in original.decode().splitlines()]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({r["ref"] for r in rows}), 3)
        for row in rows:
            self.assertEqual(set(row), {"ts", "source", "who", "who_kind", "excerpt", "ref"})
        result = self.run_script("ledger_query.py", "--since", "7d")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("(3 items)", result.stdout)
        self.assertIn("Weekly sync", result.stdout)

    def test_who_filter_and_limit(self):
        self.produce()
        result = self.run_script("ledger_query.py", "--who", "Acme", "--limit", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("(1 items)", result.stdout)
        self.assertIn("Client call", result.stdout)
        self.assertNotIn("Weekly sync", result.stdout)

    def test_window_excludes_old_item(self):
        self.produce()
        rows = [json.loads(line) for line in self.ledger.read_text().splitlines()]
        rows[0]["ts"] = "2000-01-01T00:00:00+00:00"
        self.ledger.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        result = self.run_script("ledger_query.py", "--since", "7d")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("(2 items)", result.stdout)
        self.assertNotIn("Weekly sync", result.stdout)

    def test_empty_ledger(self):
        result = self.run_script("ledger_query.py", "--since", "7d")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no items", result.stdout)
        self.assertFalse(self.ledger.exists())

    def test_invalid_window(self):
        result = self.run_script("ledger_query.py", "--since", "yesterday")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("use --since Nd", result.stderr)


if __name__ == "__main__":
    unittest.main()
