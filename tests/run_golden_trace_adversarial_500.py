"""Exactly 500 deterministic local adversarial VALIDATION CASES, NOT AI turns.

All inputs are synthetic. No model, network, browser, timers, credentials,
GitHub writes, external services, private mode content, or background agent.
"""
from __future__ import annotations
import collections
import hashlib
import json
import pathlib
import sys
from uuid import uuid5, NAMESPACE_DNS
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'kintsugi'/'sdk'))
from golden_trace_replay import verify_trace_chain, review_claim_packet


def trace(index):
    obj={
     'trace_id':str(uuid5(NAMESPACE_DNS,f'atlas-golden-neg-{index}')),
     'timestamp':'2026-11-22T18:00:00+00:00',
     'source':{'repo':'atlaslattice/aluminum-os','module':'synthetic','function':'fixture'},
     'event_type':'classification','severity':'info','sphere_tag':'H1.S1',
     'aluminum_layer':'L3-Engine','payload':{'case':index,'synthetic':True},
    }
    obj['integrity']={'hash_algorithm':'sha3-256','previous_trace_hash':'GENESIS', 'hash':digest(obj)}
    return obj


def digest(obj):
    return hashlib.sha3_256(json.dumps({k:v for k,v in obj.items() if k!='integrity'},sort_keys=True,allow_nan=False).encode('utf-8')).hexdigest()


def claim(index):
    return {'claim_id':f'SYN-{index:03d}','statement_id':'statement://synthetic',
       'source_revision':'synthetic-v1','review_lane':'NEGATIVE_TEST',
       'source_refs':['source://fixture'],'evidence_refs':['evidence://fixture'],
       'receipt_refs':['receipt://fixture'],'rights_status':'AUTHORIZED_WORK_METADATA',
       'evidence_status':'SOURCE_LINKED','authority':'NONE','status':'CANDIDATE',
       'private_mode':'NONE','deployment':False,'synthetic_case':index}


TRACE_MUTATIONS=(
 ('invalid_id',lambda e:e.update(trace_id='not-a-uuid')),
 ('naive_time',lambda e:e.update(timestamp='2026-11-22T18:00:00')),
 ('unknown_type',lambda e:e.update(event_type='AUTHORITY_GRANTED')),
 ('wrong_type',lambda e:e.update(event_type=[])),
 ('wrong_layer',lambda e:e.update(aluminum_layer=['L3-Engine'])),
 ('invalid_sphere',lambda e:e.update(sphere_tag='H999.NOT_SPHERE')),
 ('wrong_source',lambda e:e.update(source={'repo':None,'module':'synthetic'})),
 ('wrong_payload',lambda e:e.update(payload='not an object')),
 ('unsupported_hash',lambda e:e['integrity'].update(hash_algorithm='fn-dsa-512')),
 ('broken_origin',lambda e:e['integrity'].update(previous_trace_hash='NOPE')),
 ('false_digest',lambda e:e['integrity'].update(hash='0'*64)),
 ('missing_integrity',lambda e:e.pop('integrity')),
)
CLAIM_MUTATIONS=(
 ('no_source',lambda p:p.update(source_refs=[])),
 ('no_evidence',lambda p:p.update(evidence_refs=[])),
 ('no_receipt',lambda p:p.update(receipt_refs=[])),
 ('revoked',lambda p:p.update(revoked=True)),
 ('private',lambda p:p.update(private_mode='PALACE')),
 ('bad_rights',lambda p:p.update(rights_status='UNAUTHORIZED')),
 ('bad_evidence',lambda p:p.update(evidence_status='PREPARED')),
 ('nonstring_evidence',lambda p:p.update(evidence_status=[])),
 ('fake_canon',lambda p:p.update(status='CANON')),
 ('fake_deploy',lambda p:p.update(deployment=True)),
 ('fake_authority',lambda p:p.update(authority='HUMAN_ROOT')),
 ('missing_lane',lambda p:p.update(review_lane='')),
)


def _require(condition, detail):
    """Keep validation oracles active when Python is run with -O."""
    if not condition:
        raise AssertionError(detail)


def execute():
    labels=collections.Counter()
    errs=collections.Counter()
    receipts=[]
    for i in range(500):
        if i%2==0:
            obj=trace(i);name,mutation=TRACE_MUTATIONS[(i//2)%len(TRACE_MUTATIONS)]
            mutation(obj)
            if 'integrity' in obj and name not in {'false_digest','missing_integrity'}:
                obj['integrity']['hash']=digest(obj)
            result=verify_trace_chain([obj]);expected='HELD_INVALID'; label='TRACE/'+name
            errors=[x['code'] for x in result['errors']]
        else:
            obj=claim(i);name,mutation=CLAIM_MUTATIONS[(i//2)%len(CLAIM_MUTATIONS)]
            mutation(obj)
            result=review_claim_packet(obj);expected='HELD_REVIEW';label='CLAIM/'+name
            errors=result['reasons']
        _require(result['status']==expected, (i,label,result))
        _require(result['authority_effect']=='NONE', (i,label,result))
        _require(errors, (i,label,'accepted invalid input'))
        _require(obj['claim_id'].startswith('SYN-') if i%2 else obj['trace_id'],
                 'case identifier missing')
        labels[label]+=1
        errs[errors[0]]+=1
        receipts.append({'case':i,'type':label,'status':result['status'],'first_error':errors[0]})
    _require(len(receipts)==500 and len({r['case'] for r in receipts})==500,
             'case count or uniqueness invalid')
    return {'schema':'atlas.local-adversarial-validation/v1','mode':'SYNTHETIC_TEST_EXECUTION_NOT_MACROTURNS',
      'case_count':500,'passed':500,'failed':0,'executed_model_turns':0,'hosted':False,
      'network_requests':0,'work_room_posts':0,'authority_effect':'NONE',
      'test_groups':dict(sorted(labels.items())), 'error_groups':dict(sorted(errs.items())),
      'cases_sha256':hashlib.sha256(json.dumps(receipts,sort_keys=True).encode()).hexdigest(),
      'input_provenance':'DETERMINISTIC_SYNTHETIC_GENERATORS_IN_THIS_SOURCE','positive_controls':'37 unit tests separate'}


if __name__=='__main__':
    obj=execute()
    print(json.dumps(obj,sort_keys=True,indent=2))
