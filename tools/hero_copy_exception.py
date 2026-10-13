"""Validate ONE exact owner-approved heading without altering its frozen source.

The source-only validator cannot know about a later category decision. We explicitly
validate that one value and give it a no-write surrogate for the frozen validator.
The public report always discloses this scope; no other field can use this path.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCEPTION_ID = 'H1-CATEGORY-2026-10-13'
H1 = 'Enterprise Process Orchestration Platform'
TEXTS = ['Enterprise ', 'Process ', 'Orchestration ', 'Platform']
ORIGINALS = ['We ', 'Automate ', 'Enterprise Customer Operations with ', 'AI']
LIMITS = [2, 8, 35, 2]
ELEMENTS = ['370cbcb9-ca44-e3fa-3af5-ffcc49e12e2f', '2b066328-9a94-c967-16e0-a7eb5632acf0', '27e5d944-a647-2835-857a-f6cce18f23ad', 'd289d6ed-e2cb-f2c5-ed95-3ce79ffdebe2']
COMPONENT = '6899ffe04a85e00f2b8cf5ac'

def prepare_for_baseline(working, policy=None):
    flagged = [r for r in working.get('items', []) if r.get('validation_exception')]
    if not flagged:
        return working, [], []
    errors = []
    if len(flagged) != 1 or flagged[0].get('id') != 'HOME-003':
        return working, [], ['Only HOME-003 may have an exact-copy exception']
    row = flagged[0]
    if policy is None:
        try:
            policy = json.loads((ROOT / 'content/home/implementation-overrides.json').read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            return working, [], ['Missing/invalid explicit H1 exception: ' + str(exc)]
    expected = {'exception_id': EXCEPTION_ID, 'field_id': 'HOME-003', 'approved_text': H1,
                'segments': TEXTS, 'original_segment_max_chars': LIMITS,
                'replacement_segment_lengths': [10, 7, 13, 8], 'original_total_max_chars': 50,
                'new_total_chars': 41, 'visual_acceptance': 'pending'}
    if any(policy.get(k) != v for k, v in expected.items()):
        errors.append('H1 exception policy does not match the approved exact scope')
    if (row.get('validation_exception') != EXCEPTION_ID or row.get('action') != 'rewrite'
            or row.get('new_text') != H1 or row.get('max_chars') != 50
            or not row.get('claim_evidence') or row.get('layout_review') != 'pending'):
        errors.append('HOME-003: exception accepts only the exact approved heading at the original total budget')
    segments = row.get('new_segments', [])
    if len(segments) != 4:
        errors.append('HOME-003: preserve four source nodes')
    else:
        for i, seg in enumerate(segments):
            if (seg.get('source_id') != {'component': COMPONENT, 'element': ELEMENTS[i]}
                    or seg.get('original_raw') != ORIGINALS[i] or seg.get('max_chars') != LIMITS[i]
                    or seg.get('new_text') != TEXTS[i]):
                errors.append('HOME-003: source/target segment mismatch at ' + str(i + 1))
    if errors:
        return working, [], errors
    # This copy is exclusively for the frozen validator; never write it as content.
    candidate = copy.deepcopy(working)
    replacement = next(r for r in candidate['items'] if r['id'] == 'HOME-003')
    replacement.update(action='keep', new_text=None)
    replacement.pop('validation_exception', None)
    for s in replacement['new_segments']:
        s['new_text'] = None
    disclosure = {'id': EXCEPTION_ID, 'field_id': 'HOME-003', 'approved_text': H1,
                  'total_chars': 41, 'original_total_limit': 50,
                  'original_segment_limits': LIMITS, 'actual_segment_lengths': [10, 7, 13, 8],
                  'method': 'Exact-value/source-descriptor check here; frozen validator receives HOME-003 as keep only. All other 227 fields retain frozen validation.',
                  'visual_acceptance': 'pending'}
    return candidate, [disclosure], []
