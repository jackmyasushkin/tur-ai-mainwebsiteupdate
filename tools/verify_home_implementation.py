"""Verify the saved application evidence; never calls Webflow."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'implementation/2026-10-13-enterprise-orchestration'
read = lambda name: json.loads((RUN / name).read_text(encoding='utf-8'))

def check():
    report = read('report.json')
    assert len(report['fields']) == 228
    assert sum(f['status'] == 'applied' for f in report['fields']) == 104
    assert sum(f['status'] == 'no-write' for f in report['fields']) == 124
    before = read('before-readset.json')['trees']
    after = {p['label']: p['result'][0]['data'] for p in read('after-trees.json')}
    operations = read('planned-text-operations.json')
    assert len(operations) == 122
    for item in before:
        scope = item['label']
        expected = copy.deepcopy(item['result'][0]['data'])
        nodes = {}
        def walk(node):
            nodes[(node['id']['component'], node['id']['element'])] = node
            for child in node.get('children', []):
                walk(child)
        walk(expected)
        for op in operations:
            if (op['scope'] or 'Home') == scope:
                node = nodes[(op['id']['component'], op['id']['element'])]
                assert node['textContent'] == op['before']
                node['textContent'] = op['after']
        assert expected == after[scope], scope
    for item in read('post-qa-source-trees.json'):
        assert item['result'][0]['data'] == after[item['label']]
    assert all(p['ownPageTreeUnchanged'] for p in read('after-other-pages.json'))
    assert read('placeholder-readback.json')['exact']
    assert read('ordinal-animation-decision.json')['fixApplied'] is False
    assert report['published'] is False and report['lead_submissions'] == 0
    assert report['rate_control']['rate_limit_errors'] == 0
    for item in read('MANIFEST.json')['files']:
        data = (RUN / item['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    print('IMPLEMENTATION_EVIDENCE_PASS: 104 applied; 124 no-write; exact trees; known findings retained; unpublished')

if __name__ == '__main__':
    check()
