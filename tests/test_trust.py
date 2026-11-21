import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import trust  # noqa: E402


def run(*args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = trust.main(list(args))
    return code, buf.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["TRUSTWRIGHT_HOME"] = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()


class Log(Base):
    def test_log_and_show(self):
        run("log", "--product", "claude-code", "--version", "2.1.9", "--kind", "permission",
            "--observation", "asks before rm", "--date", "2026-11-01")
        code, out = run("show")
        self.assertEqual(code, 0)
        self.assertIn("claude-code 2.1.9 [permission]", out)

    def test_bad_kind(self):
        with self.assertRaises(SystemExit):
            run("log", "--product", "x", "--version", "1", "--kind", "nope", "--observation", "o")

    def test_stop(self):
        run("stop", "--harness", "claude-code", "--version", "2.1.9", "--task", "pentest notes",
            "--source", "provider-classifier", "--category", "security-research")
        _, out = run("show", "--product", "claude-code")
        self.assertIn("STOP claude-code 2.1.9", out)
        self.assertEqual(len(trust.load("stops.jsonl")), 1)

    def test_diff_versions(self):
        for v, o in [("2.1.9", "a"), ("2.1.10", "b"), ("2.1.10", "a"), ("2.2.0", "c")]:
            run("log", "--product", "p", "--version", v, "--kind", "mode", "--observation", o)
        _, out = run("diff", "--product", "p", "--from", "2.1.9", "--to", "2.1.10")
        self.assertIn("2 observations", out)
        self.assertIn("(new) b", out)
        self.assertIn("(same) a", out)
        self.assertNotIn(" c", out.split("\n", 1)[1])


class Scan(Base):
    def test_scan_fixture(self):
        hits = trust.scan(HERE / "fixtures" / "session.jsonl")
        self.assertEqual([h["source"] for h in hits],
                         ["provider-classifier", "harness-permission", "model-refusal"])
        self.assertEqual(hits[0]["line"], 3)


class Check(Base):
    def test_check(self):
        _, out = run("check", "--type", "code", "--type", "citation", "--high-stakes")
        self.assertIn("## code", out)
        self.assertIn("## citation", out)
        self.assertIn("chain-of-verification", out)


if __name__ == "__main__":
    unittest.main()
