"""Synthetic regression: JSON decoder recursion must not escape the CLI."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

CLI = pathlib.Path(__file__).resolve().parents[1] / 'kintsugi/sdk/golden_trace_replay.py'


class TestGoldenTraceCLIDepth(unittest.TestCase):
    def run_input(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / 'synthetic-trace.json'
            path.write_text(text, encoding='utf-8')
            result = subprocess.run([sys.executable, *(['-O'] if sys.flags.optimize else []),
                                     str(CLI), str(path)], capture_output=True,
                                    text=True, timeout=10, check=False)
            self.assertNotIn(str(path), result.stdout + result.stderr)
            self.assertEqual(result.stderr, '')
            return result.returncode, json.loads(result.stdout)

    def test_nested_arrays_fail_closed(self):
        code, report = self.run_input('[' * 10000 + '0' + ']' * 10000)
        self.assertEqual(code, 1)
        self.assertEqual(report['status'], 'HELD_INVALID')
        self.assertEqual(report['authority_effect'], 'NONE')

    def test_nested_objects_fail_closed(self):
        code, report = self.run_input('{"x":' * 10000 + '0' + '}' * 10000)
        self.assertEqual(code, 1)
        self.assertEqual(report['status'], 'HELD_INVALID')
        self.assertEqual(report['authority_effect'], 'NONE')

    def test_shallow_invalid_trace_still_reports_structured_hold(self):
        code, report = self.run_input('[]')
        self.assertEqual(code, 1)
        self.assertEqual(report['status'], 'HELD_INVALID')
        self.assertIn('empty_trace_no_evidence', [e['code'] for e in report['errors']])


if __name__ == '__main__':
    unittest.main()
