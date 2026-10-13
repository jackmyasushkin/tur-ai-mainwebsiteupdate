"""Validate saved evidence for issue #3; no network or Webflow writes."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'implementation/2026-10-13-ordinal-animation'
read = lambda name: json.loads((RUN / name).read_text())
app = read('application.json')
ids = app['markerIds']
before, after = read('before-home.json'), read('after-home.json')
expected = copy.deepcopy(before)
found = []
def walk(node):
    if node['id']['element'] in ids:
        assert node['attributes'] == {'fs-numbercount-element': 'number'}
        assert node['children'][0]['textContent'] == f'0{len(found)+1}'
        node['attributes']['data-tur-number-format'] = 'ordinal-2'
        found.append(node['id']['element'])
    for child in node.get('children', []):
        walk(child)
walk(expected)
assert found == ids and expected == after, 'Unexpected Home source diff'
assert app['application']['scripts'] == [{
    'id': 'turaihomeordinalformatterissue3', 'displayName': 'TuraiHomeOrdinalFormatterIssue3',
    'version': '1.0.0', 'location': 'footer', 'attributes': {}}]
assert app['freeformHomeUnchanged'] and app['freeformSiteUnchanged']
assert app['publishedByAgent'] is False
assert read('before-site.json')['lastPublished'] == read('after-site.json')['lastPublished']
assert read('compiled-code-check.json')['exactFormatterIgnoringTerminalWhitespace']
assert (RUN/'compiled-formatter.js').read_text().rstrip() == (ROOT/'webflow/home-ordinal-format.js').read_text().rstrip()
assert read('responsive-check.json')['result'] == 'PASS'

for name in ['chrome-fixture-scroll.json', 'chrome-fixture-in-view-delayed.json']:
    evidence = read(name)
    assert evidence['visibleFrames'] > 60 and not evidence['badFrames']
    assert evidence['final'] == ['01','02','03','04']
    assert evidence['metrics'] == ['62','82','83','3']
    assert any('00' in frame['ordinals'] for frame in evidence['frames']), 'Animation did not run'
fallback = read('chrome-fixture-missing.json')
assert fallback['final'] == ['01','02','03','04'] and not fallback['badFrames']
samples = read('preview-desktop-animation-samples.json')
assert any('00' in sample['ordinals'] for sample in samples), 'Actual Home animation not sampled'
assert all(len(sample['ordinals']) == 4 and all(len(v)==2 and v.isdigit() for v in sample['ordinals']) for sample in samples)
assert samples[-1]['ordinals'] == ['01','02','03','04']
assert read('preview-mobile-toggle-check.json')['numberOpacity'] == ['0']*4
assert read('preview-mobile-toggle-check.json')['values'] == ['01','02','03','04']

calls = [entry for entry in read('rate-log.json') if entry['type'] == 'call']
from datetime import datetime
stamp = lambda value: datetime.fromisoformat(value.replace('Z','+00:00')).timestamp()
for i,entry in enumerate(calls):
    assert 1 <= entry['weight'] <= 10 and not entry['is429']
    if i: assert stamp(entry['startedAt']) - stamp(calls[i-1]['endedAt']) >= 1.99
    now = stamp(entry['endedAt'])
    assert sum(e['weight'] for e in calls[:i+1] if now-stamp(e['endedAt'])<60) <= 30
for item in read('MANIFEST.json')['files']:
    assert hashlib.sha256((RUN/item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
print('PASS: four-marker-only source diff, Home-only formatter, exact compiled code, 12 widths, real Chrome frames, source fallback, Home animation/toggle, rate policy and publication boundary')
