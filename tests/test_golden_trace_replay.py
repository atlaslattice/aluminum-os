"""Stdlib regression tests for GoldenTrace read-only replay and claim review."""
from __future__ import annotations
import copy
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from uuid import UUID

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'kintsugi' / 'sdk'))
from golden_trace_replay import main, review_claim_packet, verify_trace_chain


def event(prev="GENESIS", **overrides):
    v={
      "trace_id":"223d5f6d-e830-4c02-8f89-16754c1a21d2",
      "timestamp":"2026-11-22T17:57:00+00:00",
      "source":{"repo":"atlaslattice/aluminum-os","module":"synthetic.py","function":"fixture"},
      "event_type":"invariant_check","severity":"info","sphere_tag":"H1.S1",
      "aluminum_layer":"L3-Engine","payload":{"synthetic":True,"result":"sample"},
    }
    v.update(overrides)
    hashed=hashlib.sha3_256(json.dumps(v,sort_keys=True).encode()).hexdigest()
    v['integrity']={"hash_algorithm":"sha3-256","hash":hashed,"previous_trace_hash":prev}
    return v


def claim(**changes):
    v={"claim_id":"C-001","statement_id":"statement://sample","source_revision":"fixture-v1",
       "review_lane":"SOURCE_CHECK","source_refs":["source://1"],"evidence_refs":["evidence://1"],
       "receipt_refs":["receipt://1"],"rights_status":"AUTHORIZED_WORK_METADATA",
       "evidence_status":"SOURCE_LINKED","authority":"NONE","status":"CANDIDATE",
       "private_mode":"NONE","deployment":False}
    v.update(changes)
    return v


class TestTraceReplay(unittest.TestCase):
    def test_valid_single(self): self.assertEqual(verify_trace_chain([event()])["status"],"LOCAL_HASH_CHAIN_VALID_NOT_AUTHORITY")
    def test_valid_chain(self):
        a=event();b=event(a['integrity']['hash'],trace_id="d76a9bf5-dfe5-4e72-b15f-f68e12e68fbd")
        self.assertEqual(verify_trace_chain([a,b])["status"],"LOCAL_HASH_CHAIN_VALID_NOT_AUTHORITY")
    def test_pure_and_nonmutating(self):
        a=[event()]; before=copy.deepcopy(a)
        self.assertFalse(verify_trace_chain(a)['hosted']);self.assertEqual(a,before)
    def test_no_payload_echo(self):
        a=event();a['payload']['private']='PRIVATE_DO_NOT_REPORT'
        x=verify_trace_chain([a]);self.assertNotIn('PRIVATE_DO_NOT_REPORT',repr(x))
    def test_not_list(self):self.assertEqual(verify_trace_chain({})['status'],'HELD_INVALID')
    def test_empty(self):self.assertEqual(verify_trace_chain([])['status'],'HELD_INVALID')
    def test_wrong_type(self):self.assertEqual(verify_trace_chain([None])['status'],'HELD_INVALID')
    def test_missing_integrity(self):
        a=event();del a['integrity'];self.assertIn('integrity_missing_or_invalid',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_hash_tampering(self):
        a=event();a['payload']['result']='changed';self.assertIn('hash_mismatch',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_bad_algorithm(self):
        a=event();a['integrity']['hash_algorithm']='sha256';self.assertEqual(verify_trace_chain([a])['status'],'HELD_INVALID')
    def test_broken_genesis(self):
        a=event();a['integrity']['previous_trace_hash']='wrong';self.assertEqual(verify_trace_chain([a])['status'],'HELD_INVALID')
    def test_broken_link(self):
        a=event();b=event('GENESIS',trace_id='d76a9bf5-dfe5-4e72-b15f-f68e12e68fbd')
        self.assertIn('broken_previous_link',[x['code'] for x in verify_trace_chain([a,b])['errors']])
    def test_duplicate_id(self):
        a=event();b=event(a['integrity']['hash']);self.assertIn('duplicate_trace_id',[x['code'] for x in verify_trace_chain([a,b])['errors']])
    def test_nonfinite_value(self):
        a=event();a['payload']['bad']=float('nan')
        self.assertIn('unhashable_or_nonfinite_body',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_bad_source(self):
        a=event(source={});self.assertIn('source_shape_invalid',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_bad_id(self):
        a=event(trace_id='not-uuid');self.assertIn('invalid_trace_id',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_aware_timestamp(self):
        a=event(timestamp='2026-11-22T00:00:00');self.assertIn('timestamp_not_offset_aware',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_budget(self):
        a=event();self.assertIn('event_budget_exceeded',[x['code'] for x in verify_trace_chain([a,a],max_events=1)['errors']])
    def test_invalid_signature_field(self):
        a=event();a['integrity']['signature']=False
        self.assertIn('invalid_signature_field',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_claimable_signatures_not_trusted(self):
        a=event();a['integrity']['signature']='claimed-sig'
        r=verify_trace_chain([a]);self.assertEqual(r['signed_identity'],'UNVERIFIED')
    def test_unhashable_event_type_fail_closed(self):
        a=event(event_type=[])
        self.assertIn('invalid_event_type',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_unhashable_layer_fail_closed(self):
        a=event(aluminum_layer={})
        self.assertIn('invalid_layer',[x['code'] for x in verify_trace_chain([a])['errors']])
    def test_real_world_scope_unverified(self):
        a=verify_trace_chain([event()]);self.assertEqual(a['source_completeness'],'UNVERIFIED')

class TestClaimReview(unittest.TestCase):
    def test_valid_candidate(self):self.assertEqual(review_claim_packet(claim())['status'],'CANDIDATE_REVIEWABLE_NOT_APPROVED')
    def test_missing_evidence(self):self.assertEqual(review_claim_packet(claim(evidence_refs=[]))['status'],'HELD_REVIEW')
    def test_missing_receipt(self):self.assertEqual(review_claim_packet(claim(receipt_refs=[]))['status'],'HELD_REVIEW')
    def test_missing_source(self):self.assertEqual(review_claim_packet(claim(source_refs=[]))['status'],'HELD_REVIEW')
    def test_revocation(self):self.assertEqual(review_claim_packet(claim(revoked=True))['status'],'HELD_REVIEW')
    def test_no_rights(self):self.assertEqual(review_claim_packet(claim(rights_status='MISSING'))['status'],'HELD_REVIEW')
    def test_private_mode(self):self.assertEqual(review_claim_packet(claim(private_mode='PLAY'))['status'],'HELD_REVIEW')
    def test_forged_canon(self):self.assertEqual(review_claim_packet(claim(status='CANON'))['status'],'HELD_REVIEW')
    def test_forged_deployment(self):self.assertEqual(review_claim_packet(claim(deployment=True))['status'],'HELD_REVIEW')
    def test_forged_authority(self):self.assertEqual(review_claim_packet(claim(authority='human_root'))['status'],'HELD_REVIEW')
    def test_unreviewed_evidence(self):self.assertEqual(review_claim_packet(claim(evidence_status='PREPARED'))['status'],'HELD_REVIEW')
    def test_unhashable_evidence_status_fail_closed(self):
        self.assertIn('evidence_status_unverified',review_claim_packet(claim(evidence_status=[]))['reasons'])
    def test_nonobject(self):self.assertEqual(review_claim_packet(None)['status'],'HELD_REVIEW')
    def test_no_promotion(self):
        result=review_claim_packet(claim());self.assertFalse(result['deployment']);self.assertFalse(result['semantic_acceptance'])


class TestFailClosedAmbiguities(unittest.TestCase):
    def test_ambiguous_revocation_flags_held(self):
        for flag in (0, 1, None, 'false', [], {}, 1.0):
            with self.subTest(flag=repr(flag)):
                result = review_claim_packet(claim(revoked=flag))
                self.assertEqual(result['status'], 'HELD_REVIEW')
                self.assertIn('source_revoked', result['reasons'])

    def test_ambiguous_deployment_flags_held(self):
        for flag in (0, 1, None, 'false', [], {}, 1.0):
            with self.subTest(flag=repr(flag)):
                result = review_claim_packet(claim(deployment=flag))
                self.assertEqual(result['status'], 'HELD_REVIEW')
                self.assertIn('promotion_requires_external_gate', result['reasons'])

    def test_unknown_claim_status_held(self):
        for status in (None, '', 'PUBLISHED', 'RELEASED', 'HOSTED', [], {}, 0):
            with self.subTest(status=repr(status)):
                self.assertEqual(review_claim_packet(claim(status=status))['status'], 'HELD_REVIEW')
        for status in ('CANDIDATE', 'DRAFT', 'PREPARED', 'SOURCE_LINKED', 'HELD_REVIEW'):
            with self.subTest(accepted_status=status):
                self.assertEqual(review_claim_packet(claim(status=status))['status'], 'CANDIDATE_REVIEWABLE_NOT_APPROVED')

    def test_cli_duplicate_keys_rejected_at_any_depth(self):
        import contextlib
        import io
        sample = json.dumps([event()], sort_keys=True)
        variants = (
            sample.replace('"event_type": "invariant_check"', '"event_type": "SHADOW", "event_type": "invariant_check"'),
            sample.replace('"event_type": "invariant_check"', '"event_\\u0074ype": "SHADOW", "event_type": "invariant_check"'),
            sample.replace('"repo": "atlaslattice/aluminum-os"', '"repo": "SHADOW", "repo": "atlaslattice/aluminum-os"'),
        )
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)/'synthetic.json'
            p.write_text(sample, encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(p)]), 0)
            for raw in variants:
                p.write_text(raw, encoding='utf-8')
                out=io.StringIO()
                with contextlib.redirect_stdout(out):
                    self.assertEqual(main([str(p)]), 1)
                self.assertEqual(json.loads(out.getvalue())['status'], 'HELD_INVALID')
                self.assertNotIn(str(p), out.getvalue())

if __name__=='__main__':unittest.main()