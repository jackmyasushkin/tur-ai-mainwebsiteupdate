"""One-time, hash-guarded content amendment; never touches Webflow or baseline."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'content/home'
REV = 'card-captions-2026-10-13'
EXPECTED_BLOB = '5578f2fbe717f2b592cf0729084a092489d7cc37'
UPDATES = {
    'HOME-019': {
        'before': 'Banking case: annual token spend fell from \u20ac1.8M to \u20ac300K.',
        'after': 'Banking case: lower annual token spend with task-specific models.',
        'screenshot': 'Banking case: annual token spend fell due to large to specialized models use.',
        'reason': 'Owner screenshot revision: explain task-specific model use; retain annual token-spend denominator. Absolute amounts remain in FAQ/evidence.',
    },
    'HOME-023': {
        'before': 'A European bank: 3x faster process delivery; 2-3 to 12+ processes automated per year.',
        'after': 'A European bank: processes delivered 3x faster by the same transformation team.',
        'screenshot': 'A European bank: 3x faster process delivery within same transformation team.',
        'reason': 'Owner screenshot explicitly supplies the same-transformation-team context. Do not infer unchanged budget, FTE count, workload or quality.',
    },
}

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def normal(value):
    return re.sub(r'\s+', ' ', value).strip()

def append(path, text):
    current = path.read_text(encoding='utf-8')
    assert REV not in current, f'Already amended: {path.name}'
    path.write_text(current.rstrip() + '\n\n' + text.strip() + '\n', encoding='utf-8')

def run(*args):
    p = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stdout + '\n' + p.stderr)
    return p.stdout, p.stderr

def main():
    path = HOME / 'rewrite.json'
    raw = path.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert blob == EXPECTED_BLOB, 'Rewrite changed; reconcile before applying this amendment'
    original = json.loads(raw)
    working = copy.deepcopy(original)
    rows = {r['id']: r for r in working['items']}
    assert len(rows) == 228
    for rid, change in UPDATES.items():
        row = rows[rid]
        assert row['action'] == 'rewrite' and row['new_text'] == change['before'] and row['new_segments'] == [], rid
        assert len(normal(change['after'])) <= row['max_chars'], rid
        row['new_text'] = change['after']
        row['reason'] = change['reason']
    for before, after in zip(original['items'], working['items']):
        assert before['id'] == after['id']
        if before['id'] not in UPDATES:
            assert before == after, 'Unrelated content changed'
        else:
            assert {k:v for k,v in before.items() if k not in ('new_text','reason')} == {k:v for k,v in after.items() if k not in ('new_text','reason')}
    lines = raw.decode('utf-8').splitlines(keepends=True)
    counts = {rid: 0 for rid in UPDATES}
    for index, line in enumerate(lines):
        for rid in UPDATES:
            if f'"id":"{rid}"' in line:
                counts[rid] += 1
                comma = ',' if line.rstrip().endswith(',') else ''
                lines[index] = '    ' + json.dumps(rows[rid], ensure_ascii=False, separators=(',', ':')) + comma + '\n'
    assert all(n == 1 for n in counts.values()), 'Expected compact source rows'
    path.write_text(''.join(lines), encoding='utf-8')
    assert load(path) == working
    new_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    plan = load(HOME / 'apply-plan.json')
    old_hash = plan['rewrite_sha256']
    plan['rewrite_sha256'] = new_hash
    plan['content_revision'] = REV
    plan['changed_since_v1'] = sorted(set(plan['changed_since_v1']) | set(UPDATES))
    for item in plan['items']:
        if item['id'] in UPDATES:
            change = UPDATES[item['id']]
            item['target_text'] = change['after']
            item['reason'] = change['reason']
            item['accepted_intermediate_texts'] = [change['before'], change['screenshot']]
    save(HOME / 'apply-plan.json', plan)
    delta = load(HOME / 'edition-delta.json')
    delta['changed_ids'] = sorted(set(delta['changed_ids']) | set(UPDATES))
    delta['content_revision'] = REV
    save(HOME / 'edition-delta.json', delta)
    proposal = HOME / 'proposal.md'
    lines = proposal.read_text(encoding='utf-8').splitlines()
    for rid, change in UPDATES.items():
        matches = [i for i,l in enumerate(lines) if l.startswith('| ' + rid + ' |')]
        assert len(matches) == 1, rid
        lines[matches[0]] = f"| {rid} | rewrite | {change['after']} | {len(change['after'])} / {rows[rid]['max_chars']} |"
    proposal.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    note = f'''## {REV}: mechanism and team context

Owner supplied a screenshot requesting two caption changes. The English was edited without changing the headline metrics or inventing a new result.

- HOME-019: **{UPDATES['HOME-019']['after']}**
- HOME-023: **{UPDATES['HOME-023']['after']}**

Task-specific models is the edited wording for the owner's specialized-model mechanism. It does not claim all large models were removed, that specialized means small or fine-tuned, or that model selection alone accounts for all 83% of savings. Annual token spend remains the metric; EUR 1.8M to EUR 300K remains in the FAQs and evidence.

The same transformation team is a new owner-supplied case clarification from this screenshot, not a conclusion derived from annual process counts. It does not independently establish equal headcount, budget, workload, quality or no external assistance. The 2-3 to 12+ annual-capacity result remains supporting evidence, not the derivation of the 3x delivery result.

The owner requested the meaning; these polished sentences are an editorial implementation of that request. No claim of word-for-word owner approval, independent audit, Webflow read/write or visual acceptance is made.
'''
    for name in ('decisions.md', 'evidence.md', 'business-brief.md'):
        append(HOME / name, note)
    append(proposal, f'## {REV}\n\nOnly HOME-019 and HOME-023 were amended in this pass. Absolute token-spend amounts remain in the FAQs and evidence. The screenshot adds the same-transformation-team context. See decisions.md for provenance and boundaries.')
    handoff = ROOT / 'docs/IMPLEMENTATION_HANDOFF.md'
    original_handoff = handoff.read_text(encoding='utf-8')
    heading, rest = original_handoff.split('\n', 1)
    amendment = f'''\n\n## Latest content revision: {REV}

The authoritative rewrite and apply plan include the two new captions. Read `content/home/card-caption-delta.json` before implementation. Preserve the headline values 83% and 3x; all other page text remains unchanged by this revision.

For HOME-019 and HOME-023 only, the immediately preceding prepared text and the owner's screenshot wording are authorized intermediate states, listed in the delta and apply plan. If found live, capture the actual value for rollback and replace with the new target. An unknown third value still requires reconciliation. Do not assume the screenshot verifies any current Webflow state. No writes were performed by this content revision.

The same-team clarification belongs to this one bank case; do not turn it into a general same-budget or same-headcount guarantee. Both captions fit the original field budgets; no new exceptions are introduced.
'''
    handoff.write_text(heading + amendment + rest, encoding='utf-8')
    save(HOME / 'card-caption-delta.json', {
        'revision': REV, 'base_commit': '086ce563960473a70221dccb8c7092507fa93e3b',
        'previous_rewrite_blob': EXPECTED_BLOB, 'rewrite_sha256': new_hash,
        'source': 'Owner-provided card screenshot in the homepage conversation, 13 October 2026',
        'scope': 'Two captions only; other 226 item records unchanged; no Webflow writes',
        'items': [dict(id=rid, previous_prepared_text=c['before'], owner_screenshot_text=c['screenshot'], new_text=c['after'], chars=len(c['after']), max_chars=rows[rid]['max_chars']) for rid,c in UPDATES.items()],
    })
    output, _ = run('tools/check.py', '--complete')
    report = json.loads(output)
    assert report['status'] == 'EDITORIAL_LIMITS_PASS' and report['errors'] == []
    test_out, test_err = run('-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py')
    handoff_out, _ = run('tools/verify_home_handoff.py')
    handoff_check = json.loads(handoff_out)
    assert handoff_check['status'] == 'HANDOFF_CONSISTENCY_PASS'
    run_url = f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    previous_report = load(HOME / 'preparation-report.json')
    report.update(edition=plan['edition'], content_revision=REV, execution_environment='GitHub Actions',
        source_rewrite_blob=EXPECTED_BLOB, rewrite_sha256=new_hash, regression_tests=(test_out+test_err).strip(),
        handoff_check=handoff_check, run_url=run_url, unchanged_item_records=226,
        changed_ids=list(UPDATES), recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save(HOME / 'preparation-report.json', report)
    status = HOME / 'STATUS.md'
    text = status.read_text(encoding='utf-8').replace(old_hash, new_hash).replace(previous_report['run_url'], run_url)
    status.write_text(text, encoding='utf-8')
    append(status, f'## {REV}\n\nTwo caption replacements completed and synchronized with apply-plan.json, proposal.md, evidence and the implementation handoff. The remaining 226 item records are unchanged. Full editorial and handoff checks pass; regression tests pass. {len(report["warnings"])} warnings remain for visual review. Webflow was not read or changed in this revision.')
    validation = '# Current validation\n\nRevision: `' + REV + '`.\n\n[Actual run](' + run_url + ')\n\n'
    validation += 'Full checker: EDITORIAL_LIMITS_PASS. Handoff: HANDOFF_CONSISTENCY_PASS. Original baseline and budgets preserved, including the previously documented H1 exception. No new exceptions.\n\n'
    validation += 'Two caption changes; other 226 item records unchanged. 104 rewrite / 88 keep / 36 hold.\n\n```text\n' + (test_out+test_err).strip() + '\n```\n\n## Visual-review warnings\n\n'
    validation += '\n'.join('- ' + w for w in report['warnings']) + '\n\nNo Webflow write or browser acceptance was performed.\n'
    (HOME / 'validation.md').write_text(validation, encoding='utf-8')
    subprocess.run(['git', 'diff', '--exit-code', '--', 'baseline/', '.github/workflows/'], cwd=ROOT, check=True)
    print(json.dumps({'revision':REV, 'status':'PASS', 'rewrite_sha256':new_hash, 'changed_ids':list(UPDATES), 'warnings':len(report['warnings']), 'run_url':run_url}, indent=2))

if __name__ == '__main__':
    main()
