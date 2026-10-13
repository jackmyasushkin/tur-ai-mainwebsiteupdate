"""Check handoff consistency. Read-only: never modifies Webflow or Git files."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
H1 = 'Enterprise Process Orchestration Platform'
SUBTITLE = 'Run regulated processes across existing systems. Customers trust us to help them work faster today and change faster tomorrow.'

def check():
    home = ROOT / 'content/home'
    raw = (home / 'rewrite.json').read_bytes()
    rewrite = json.loads(raw)
    plan = json.loads((home / 'apply-plan.json').read_text(encoding='utf-8'))
    base = ROOT / plan['source_inventory']
    records = json.loads(base.read_text(encoding='utf-8'))['records']
    rows = rewrite['items']
    by_id = {r['id']: r for r in rows}
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    require(len(rows) == 228 and len(by_id) == 228, 'All 228 unique decisions are required')
    require(plan['rewrite_sha256'] == hashlib.sha256(raw).hexdigest(), 'Apply plan is stale relative to rewrite')
    require(plan['inventory_sha256'] == hashlib.sha256(base.read_bytes()).hexdigest(), 'Source inventory hash mismatch')
    require([r['id'] for r in rows] == [r['id'] for r in plan['items']], 'Apply plan order/IDs differ')
    require(set(by_id) == {r['id'] for r in records}, 'Source and rewrite IDs differ')
    require(by_id['HOME-003']['new_text'] == H1, 'Approved category drift')
    require(by_id['HOME-004']['new_text'] == SUBTITLE, 'Approved customer-value copy drift')
    require(plan['site_id'] == '6899ffe04a85e00f2b8cf5ab' and plan['page_id'] == '6899ffe04a85e00f2b8cf5ac', 'Wrong Webflow target')
    for row, p in zip(rows, plan['items']):
        require(p['action'] == row['action'] and p['expected_original_text'] == row['original_text'], row['id'] + ': apply plan decision/source mismatch')
        require(p['source_record_id'] == row['id'], row['id'] + ': bad target source pointer')
        expected = row['new_text'] if row['action'] == 'rewrite' else None
        require(p['target_text'] == expected and p['segments'] == row['new_segments'], row['id'] + ': apply values mismatch')
        require(p.get('validation_exception') == row.get('validation_exception'), row['id'] + ': exception drift')
        require(row.get('layout_review') == 'pending', row['id'] + ': no visual approval exists')
    for a, b in [(44, 56), (47, 59), (48, 60), (51, 63), (69, 70), (89, 98), (91, 101), (93, 104), (95, 100), (96, 103), (97, 106)]:
        aa, bb = by_id[f'HOME-{a:03d}'], by_id[f'HOME-{b:03d}']
        av = aa['new_text'] if aa['action'] == 'rewrite' else aa['original_text']
        bv = bb['new_text'] if bb['action'] == 'rewrite' else bb['original_text']
        require(av == bv, f'Paired copy differs: {a}/{b}')
    required_holds = [53, 54, 55, 177, 178, 179, 194, 207] + list(range(160, 177)) + list(range(216, 227))
    for n in required_holds:
        require(by_id[f'HOME-{n:03d}']['action'] == 'hold', f'Protected field {n} not held')
    for n, expected in [(9, '62'), (13, '82'), (17, '83'), (21, '3'), (22, '\u00d7')]:
        require(by_id[f'HOME-{n:03d}']['new_text'] == expected, f'Metric drift in {n}')
    require('token spend' in by_id['HOME-019']['new_text'], 'Token denominator missing')
    for n in (3, 4):
        require(by_id[f'HOME-{n:03d}']['new_text'] in (home / 'proposal.md').read_text(encoding='utf-8'), 'Proposal is stale')
    require('The operational plane' in by_id['HOME-068']['new_text'], 'Architectural distinction disappeared')
    for path in ['docs/IMPLEMENTATION_HANDOFF.md', 'content/home/decisions.md', 'content/home/implementation-overrides.json']:
        require((ROOT / path).is_file(), 'Missing handoff asset: ' + path)
    counts = {a: sum(r['action'] == a for r in rows) for a in ('rewrite', 'keep', 'hold')}
    require(plan['counts'] == counts, 'Action counts differ')
    return {'status': 'FAIL' if errors else 'HANDOFF_CONSISTENCY_PASS', 'validation_scope': 'Prepared copy only; live application evidence is in implementation/report.json', 'errors': errors, 'decisions': counts,
            'webflow_changed': False, 'visual_acceptance': 'NOT_CHECKED', 'publication': 'NOT_PERFORMED'}

if __name__ == '__main__':
    try:
        result = check()
    except (KeyError, OSError, TypeError, ValueError) as exc:
        result = {'status': 'FAIL', 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(int(result['status'] == 'FAIL'))
