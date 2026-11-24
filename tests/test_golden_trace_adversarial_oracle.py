"""Regression: optimized Python must retain the 500-case runner's oracles.

Synthetic injected validator failures exercise the test harness, not the host.
"""
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'tests' / 'run_golden_trace_adversarial_500.py'


class TestAdversarialOracle(unittest.TestCase):
    def run_runner(self, optimization, mutation=''):
        script = '''
import importlib.util
import json
import pathlib
import sys
path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('adversarial_runner', path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
mutation = sys.argv[2]
if mutation:
    def corrupt(function):
        def wrapped(value):
            report = function(value)
            if mutation in ('status', 'claim_status'):
                report['status'] = 'INCORRECTLY_ACCEPTED'
            elif mutation == 'authority':
                report['authority_effect'] = 'UNAUTHORIZED'
            return report
        return wrapped
    if mutation != 'claim_status':
        runner.verify_trace_chain = corrupt(runner.verify_trace_chain)
    runner.review_claim_packet = corrupt(runner.review_claim_packet)
try:
    receipt = runner.execute()
except AssertionError:
    print('ORACLE_REJECTED')
    raise SystemExit(3)
print(json.dumps(receipt, sort_keys=True))
'''
        return subprocess.run(
            [sys.executable, *(['-O'] if optimization else []), '-c', script,
             str(RUNNER), mutation], capture_output=True, text=True,
            check=False, timeout=10)

    def test_incorrect_status_rejected_in_both_modes(self):
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                result = self.run_runner(optimized, 'status')
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertEqual(result.stdout.strip(), 'ORACLE_REJECTED')
                self.assertEqual(result.stderr, '')

    def test_incorrect_authority_rejected_in_both_modes(self):
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                result = self.run_runner(optimized, 'authority')
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertEqual(result.stdout.strip(), 'ORACLE_REJECTED')
                self.assertEqual(result.stderr, '')

    def test_incorrect_claim_status_rejected_in_both_modes(self):
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                result = self.run_runner(optimized, 'claim_status')
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertEqual(result.stdout.strip(), 'ORACLE_REJECTED')
                self.assertEqual(result.stderr, '')

    def test_unmodified_validators_preserve_receipt_in_both_modes(self):
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                result = self.run_runner(optimized)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                receipt = json.loads(result.stdout)
                self.assertEqual(receipt['case_count'], 500)
                self.assertEqual(receipt['passed'], 500)
                self.assertEqual(receipt['failed'], 0)
                self.assertEqual(receipt['cases_sha256'],
                    '1fb0bd14d8518a2a75b5712c236a68a6777930b71c2ab6e07d21fe60bac1a9ff')


if __name__ == '__main__':
    unittest.main()
