"""One-time, guarded content migration. Never accesses Webflow or publishes a site."""
from __future__ import annotations
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'content/home'
BASE = ROOT / 'baseline/home/2026-10-12'
SOURCE_BLOB = 'c792821fc5b6d5a2f788090748f605766544c782'
EDITION = 'enterprise-orchestration-handoff-v2'
H1 = 'Enterprise Process Orchestration Platform'
SUBTITLE = 'Run regulated processes across existing systems. Customers trust us to help them work faster today and change faster tomorrow.'
EXCEPTION = 'H1-CATEGORY-2026-10-13'
NORM = lambda s: re.sub(r'\s+', ' ', s).strip()

def put(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value, encoding='utf-8')

def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    raw = (HOME / 'rewrite.json').read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != SOURCE_BLOB:
        raise SystemExit('Stop: source rewrite changed; reconcile rather than overwrite: ' + blob)
    data = json.loads(raw)
    before = copy.deepcopy(data)
    data['instructions'] = 'Prepared edition enterprise-orchestration-handoff-v2. Preserve all source IDs and descriptors. Write only rewrite fields under a separately assigned sandbox implementation task; keep/hold are no-write. HOME-003 uses the documented exact-copy exception. Never publish without separate authorization.'
    rows = {r['id']: r for r in data['items']}
    baseline = json.loads((BASE / 'inventory.json').read_text(encoding='utf-8'))
    sources = {r['id']: r for r in baseline['records']}
    def edit(n, text=None, segments=None, evidence='evidence.md#p1'):
        row = rows[f'HOME-{n:03d}']
        row.update(action='rewrite', claim_evidence=evidence,
                   reason='V2: owner-approved enterprise orchestration category and AI/transformation buyer context.',
                   layout_review='pending')
        if segments is not None:
            assert len(segments) == len(row['new_segments'])
            for node, value in zip(row['new_segments'], segments):
                node['new_text'] = value
            text = ''.join(segments)
        assert isinstance(text, str) and len(NORM(text)) <= row['max_chars'], (row['id'], len(NORM(text)))
        row['new_text'] = text
    edit(3, segments=['Enterprise ', 'Process ', 'Orchestration ', 'Platform'])
    rows['HOME-003']['validation_exception'] = EXCEPTION
    rows['HOME-003']['reason'] = 'Exact owner-approved H1. Same four nodes/styles; explicit legacy segment-budget exception, not a larger field budget.'
    edit(4, SUBTITLE)
    edit(6, 'See how to run, control and change a process across your systems.', evidence='evidence.md#e1')
    edit(27, segments=['Coordinate', ' Systems, AI and People in One Governed Process.'])
    edit(32, 'Task routing')
    edit(33, 'Match each step to a system action, an AI model or a human decision. Use the right model for each AI task.', evidence='evidence.md#p1; evidence.md#p2')
    edit(68, segments=['The operational plane: ', 'your rules', ', across your existing systems.'])
    edit(88, segments=['One ', 'platform', ' to pilot, run and scale your processes'])
    edit(119, 'How does Tur.ai fit with our ERP, automation tools and AI?')
    edit(120, 'Tur.ai is an enterprise process orchestration platform above your systems of record. It coordinates systems, AI and people in one governed process. Keep core records where they belong while your teams run, control and change the work across them.')
    edit(126, 'Discuss process delivery, AI costs and the controls you need.', evidence='evidence.md#e1')
    edit(143, 'See a process run across systems, with controls and task-matched AI.', evidence='evidence.md#e1')
    edit(152, 'Share your details to discuss orchestration.', evidence='evidence.md#e1')
    edit(209, 'Which process needs to change, and which systems and controls are involved?', evidence='evidence.md#e1')
    edit(227, 'Tur.ai | Enterprise Process Orchestration')
    edit(228, 'Run regulated processes across existing systems. Orchestrate systems, AI and people to work faster today and change faster tomorrow.')
    # Preserve the existing compact serialization and every source descriptor.
    text = '{\n  "instructions": ' + json.dumps(data['instructions'], ensure_ascii=False) + ',\n  "items": [\n'
    text += ',\n'.join('    ' + json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in data['items'])
    text += '\n  ]\n}\n'
    put('content/home/rewrite.json', text)
    policy = {
        'exception_id': EXCEPTION, 'field_id': 'HOME-003', 'approved_text': H1,
        'approval_basis': 'Owner accepted this exact category and subtitle, then instructed preparation of the implementation handoff. Segment allocation is an implementation derivation, not visual approval.',
        'segments': ['Enterprise ', 'Process ', 'Orchestration ', 'Platform'],
        'original_segment_max_chars': [2, 8, 35, 2], 'replacement_segment_lengths': [10, 7, 13, 8],
        'original_total_max_chars': 50, 'new_total_chars': 41,
        'preserve': ['all four source IDs and order', 'all classes/styles and the existing Process highlight', 'boundary whitespace', 'DOM structure', 'total field limit'],
        'forbidden': ['enlarging original source budgets', 'splitting words to fit old slots', 'adding an AI suffix', 'shrinking fonts', 'deleting spans', 'new manual line breaks'],
        'visual_acceptance': 'pending'
    }
    put('content/home/implementation-overrides.json', dump(policy))
    # Install the explicit exception hook outside the immutable baseline.
    checker_path = ROOT / 'tools/check.py'
    checker = checker_path.read_text(encoding='utf-8')
    replacements = [
        ('import tempfile\n', 'import tempfile\nfrom hero_copy_exception import prepare_for_baseline\n'),
        ('    validation = {}\n', '    validation = {}\n    exceptions = []\n    validator_working = working\n'),
        ('    if not errors:\n        with tempfile.TemporaryDirectory', '    if not errors:\n        validator_working, exceptions, exception_errors = prepare_for_baseline(working)\n        errors.extend(exception_errors)\n    if not errors:\n        with tempfile.TemporaryDirectory'),
        ('json.dumps(working, ensure_ascii=False)', 'json.dumps(validator_working, ensure_ascii=False)'),
        ('        "warnings": validation.get("warnings", []),', '        "warnings": validation.get("warnings", []) + (["HOME-003: exact approved H1 uses a documented segment-budget exception; visual review required"] if exceptions else []),\n        "approved_copy_exceptions": exceptions,')
    ]
    for old, new in replacements:
        assert checker.count(old) == 1, 'Checker changed: ' + old
        checker = checker.replace(old, new)
    put('tools/check.py', checker)
    # Publish the self-contained human handoff and decision record shipped alongside this migration.
    for p in sorted((ROOT / 'tools/handoff_v2').glob('*.md')):
        dest = {'IMPLEMENTATION_HANDOFF.md': 'docs/IMPLEMENTATION_HANDOFF.md',
                'business-brief.md': 'content/home/business-brief.md',
                'decisions.md': 'content/home/decisions.md'}.get(p.name)
        if dest:
            put(dest, p.read_text(encoding='utf-8'))
    evidence = (HOME / 'evidence.md').read_text(encoding='utf-8')
    evidence = evidence.replace('**Product and positioning.**', '**Product and positioning.**\nCurrent homepage category: **Enterprise Process Orchestration Platform**.\nOwner approved exact hero wording and implementation preparation; see [decisions](decisions.md).\nThe operational plane is the architectural role, not a replacement headline.\nPrimary readers: Head of AI and Head of Transformation. No new product or performance certification is implied.\n')
    put('content/home/evidence.md', evidence)
    review = (HOME / 'review-questions.md').read_text(encoding='utf-8')
    start = review.index('## Q1')
    end = review.index('## Q2')
    review = review[:start] + '## Q1 - Approval scope and settled content\n\nThe exact enterprise-orchestration hero is owner-approved. The owner directed the rest of Home to be aligned and prepared for an implementation agent. Use the current edition, not the rejected AI-first hero. Do not restart positioning or invent a new headline.\n\nImplementation starts only when explicitly assigned. Keep banks anonymous and retain metric captions plus the metrics FAQ. Full visual acceptance and publication are separate; preparation does not authorize publication.\n\n' + review[end:]
    put('content/home/review-questions.md', review)
    workflow_path = ROOT / '.github/workflows/content-check.yml'
    workflow = workflow_path.read_text(encoding='utf-8')
    if 'tools/verify_home_handoff.py' not in workflow:
        workflow += "      - name: Verify implementation handoff consistency\n        if: hashFiles('content/home/apply-plan.json') != ''\n        run: python3 tools/verify_home_handoff.py\n"
    put('.github/workflows/content-check.yml', workflow)
    put('docs/NEXT_AGENT.md', '# Next agent: implement the prepared Home edition\n\nStart with [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md).\n\nContent preparation is complete for edition `'+EDITION+'`. Do not restart positioning or use the old hero from Git history. Read the branch named in the handoff; `main` can still contain the initial export until the PR is merged.\n\nThe exact approved category is **'+H1+'**. Read `content/home/rewrite.json`, the explicit H1 exception, and the baseline bindings before any write. No Webflow write or publication was performed during preparation. Site changes require an explicit implementation task; publication always requires separate authorization.\n')
    put('README.md', '# Tur.ai Home: implementation handoff\n\n**Current edition: '+EDITION+'**\n\nStart at **[the implementation handoff](docs/IMPLEMENTATION_HANDOFF.md)**.\n\n- [Exact replacements](content/home/rewrite.json) and [machine apply plan](content/home/apply-plan.json)\n- [Copy in page order](content/home/proposal.md)\n- [Approved direction](content/home/business-brief.md), [decisions](content/home/decisions.md), [evidence](content/home/evidence.md)\n- [Status](content/home/STATUS.md), [validation](content/home/validation.md), [known holds](content/home/review-questions.md)\n\nApproved hero:\n\n> **'+H1+'**\n>\n> '+SUBTITLE+'\n\nPrepare and validate, without writing to Webflow:\n\n```sh\npython3 tools/check.py --complete\npython3 -m unittest discover -s tools -p "test_*.py"\npython3 tools/verify_home_handoff.py\n```\n\nHOME-003 has one explicit exact-copy segment exception. The original baseline and budgets are unchanged. See `implementation-overrides.json`; do not silence arbitrary validation errors.\n\nWebflow changes, visual acceptance and publication have NOT been performed. PR #1 remains the review/change record; a merge does not publish the website.\n\n## Source snapshot\n\nThe immutable [baseline](baseline/home/2026-10-12/README.md) contains the original 228 fields, bindings, layout measurements and source checksums. It is not the new page copy. Do not modify it.\n')
    agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    put('AGENTS.md', '# Current task and precedence\n\nThe latest owner-approved homepage category is **'+H1+'**. First read `docs/IMPLEMENTATION_HANDOFF.md`. The exact hero is locked in `content/home/decisions.md`. This is a homepage messaging decision; do not silently rewrite the separate TechCrunch positioning repository.\n\n`HOME-003` alone has a documented, exact-value exception to legacy segment budgets. Keep original `max_chars`, IDs and raw source descriptors intact. `tools/check.py` validates it explicitly through `hero_copy_exception.py`, then validates all other fields using the frozen checker. No other exceptions are authorized.\n\nCurrent scope is a prepared implementation handoff. Do not write to Webflow without an implementation instruction; never publish without separate authorization.\n\n' + agents)
    changed = [a['id'] for a, b in zip(data['items'], before['items']) if a != b]
    counts = {a: sum(r['action'] == a for r in data['items']) for a in ['rewrite', 'keep', 'hold']}
    plan = {
        'edition': EDITION, 'site_id': '6899ffe04a85e00f2b8cf5ab', 'page_id': '6899ffe04a85e00f2b8cf5ac',
        'site_name': 'Copy of Tur.ai', 'page_name': 'Home', 'language': 'en',
        'rewrite_sha256': sha(HOME / 'rewrite.json'), 'inventory_sha256': sha(BASE / 'inventory.json'),
        'source_inventory': 'baseline/home/2026-10-12/inventory.json',
        'lookup': 'Join items[].id to inventory.records[].id; the source record contains the full Webflow target, field type, component chain and inline structure. Never use text search as a replacement for these bindings.',
        'policy': 'Write only action=rewrite after live preflight. keep/hold are no-write. All source addressing is inherited, not guessed. No publish.',
        'counts': counts, 'changed_since_v1': changed, 'exception_file': 'content/home/implementation-overrides.json',
        'items': [{'id': r['id'], 'action': r['action'], 'expected_original_text': r['original_text'],
                   'target_text': r['new_text'] if r['action'] == 'rewrite' else None,
                   'segments': r['new_segments'], 'source_record_id': r['id'],
                   'validation_exception': r.get('validation_exception'), 'reason': r['reason']} for r in data['items']]
    }
    put('content/home/apply-plan.json', dump(plan))
    sections = [(1, 6, 'Hero and navigation'), (7, 23, 'Selected work/change results'), (24, 26, 'Founder statement'),
                (27, 42, 'Process orchestration'), (43, 67, 'Existing client cases'), (68, 86, 'Operational plane and efficiency'),
                (87, 87, 'Testimonial heading'), (88, 106, 'Pilot, launch and scale'), (107, 107, 'Deployment review'),
                (108, 124, 'Buyer questions'), (125, 159, 'Contact and forms'), (160, 226, 'Protected forms, testimonial and asset text'), (227, 228, 'SEO')]
    proposal = '# Home copy: enterprise orchestration edition\n\nEdition: `'+EDITION+'`. Prepared for the implementation agent; not applied or published.\n\n> **'+H1+'**\n>\n> '+SUBTITLE+'\n\nCategory first; customer value second. Operational plane explains the architecture below. Task-matched models explain AI economics; they do not define the entire platform. Primary readers are Head of AI and Head of Transformation.\n\nThe four case metrics remain **62% cycle time, 82% required FTE, 83% annual token spend, 3x process-delivery speed**. Their denominators and case boundaries are in [evidence.md](evidence.md). None is an implementation TTV or full-TCO claim.\n\nOwner approved the exact hero and directed downstream alignment. Other wording is prepared under that instruction, not a fabricated word-for-word signoff.\n\n**H1 exception:** the four text nodes become `Enterprise ` / `Process ` / `Orchestration ` / `Platform`. Total 41/50. Two segment limits are exceeded, explicitly documented and tested; no CSS or DOM change is planned.\n\n'
    for lo, hi, heading in sections:
        proposal += '## ' + heading + '\n\n| ID | Action | Text | Characters / max |\n|---|---|---|---:|\n'
        for n in range(lo, hi + 1):
            r = rows[f'HOME-{n:03d}']
            value = r['new_text'] if r['action'] == 'rewrite' else '(unchanged; do not write)'
            value = value.replace('|', '\\|').replace('\n', '<br>')
            amount = str(len(NORM(r['new_text']))) + ' / ' + str(r['max_chars']) if r['action'] == 'rewrite' else '-'
            proposal += '| '+r['id']+' | '+r['action']+' | '+value+' | '+amount+' |\n'
        proposal += '\n'
    proposal += '## Implementation\n\nSee [handoff](../../docs/IMPLEMENTATION_HANDOFF.md), [apply plan](apply-plan.json), [validation](validation.md) and [known holds](review-questions.md). Rich-text rendering and paragraph breaks must follow source nodes, not this Markdown table.\n'
    put('content/home/proposal.md', proposal)
    put('content/home/READY_FOR_REVIEW', 'Complete prepared copy: '+EDITION+'. Exact hero approved; remaining copy aligned under owner instruction. One explicit H1 segment-budget exception. Not Webflow acceptance or permission to publish.\n')
    put('content/home/edition-delta.json', dump({'edition': EDITION, 'previous_rewrite_blob': SOURCE_BLOB, 'changed_ids': changed, 'counts': counts}))
    result = subprocess.run([sys.executable, 'tools/check.py', '--complete'], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        print(result.stdout); print(result.stderr); raise SystemExit(result.returncode)
    report = json.loads(result.stdout)
    tests = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py'], cwd=ROOT, text=True, capture_output=True)
    print(tests.stdout); print(tests.stderr)
    if tests.returncode:
        raise SystemExit(tests.returncode)
    verify = subprocess.run([sys.executable, 'tools/verify_home_handoff.py'], cwd=ROOT, text=True, capture_output=True)
    print(verify.stdout); print(verify.stderr)
    if verify.returncode:
        raise SystemExit(verify.returncode)
    report.update(edition=EDITION, execution_environment='GitHub Actions',
                  source_rewrite_blob=SOURCE_BLOB, rewrite_sha256=sha(HOME / 'rewrite.json'),
                  regression_tests=tests.stderr.strip(), handoff_check=json.loads(verify.stdout),
                  run_url='https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/actions/runs/'+os.environ.get('GITHUB_RUN_ID', 'unknown'))
    put('content/home/preparation-report.json', dump(report))
    validation = '# Validation of the current handoff\n\nActual run: '+report['run_url']+'\n\n- Complete checker: **'+report['status']+'**\n- Errors: '+str(len(report['errors']))+'\n- Pending decisions: '+str(report['decisions']['pending'])+'\n- All regression tests passed.\n- Handoff consistency check passed.\n- Source baseline manifest checked without modification.\n- Exact H1 validated separately; original segment limits not rewritten.\n\n```text\n'+tests.stderr.strip()+'\n```\n\n## Non-blocking visual warnings\n\n' + '\n'.join('- '+w for w in report['warnings']) + '\n\nNo browser layout, functional, claim-audit or publishing check was performed. These remain separate from text validation.\n'
    put('content/home/validation.md', validation)
    put('content/home/STATUS.md', '# Home handoff status\n\nEdition: `'+EDITION+'`.\n\n| Stage | Status |\n|---|---|\n| Exact category and hero | Owner approved in this conversation |\n| Rest of Home | Aligned under the owner\'s instruction |\n| All 228 decisions | '+str(counts['rewrite'])+' rewrite / '+str(counts['keep'])+' keep / '+str(counts['hold'])+' hold |\n| Full validation | PASS; one transparent exact-copy H1 exception |\n| Regression and handoff checks | PASS; see preparation-report.json |\n| Ready for implementation agent | Yes, using docs/IMPLEMENTATION_HANDOFF.md |\n| Webflow writes | Not performed |\n| Visual / functional acceptance | Pending |\n| Publication | Not performed; separate authorization required |\n\n[Actual validation run]('+report['run_url']+') verifies the generated replacement set. Rewrite SHA-256: `'+report['rewrite_sha256']+'`. The preparation container had no GitHub network access; full tests ran in GitHub Actions, not locally.\n\n## Approval scope\n\nThe exact hero is explicitly approved. The remaining alignment was delegated for preparation by the owner, not independently signed off sentence by sentence. The implementation agent must preserve the prepared edition, leave holds untouched, and report visual/content conflicts without inventing replacements. The current request authorizes preparation only; an implementation invocation authorizes sandbox edits, not publication.\n\n## Historical validation\n\nlocal-precheck.json records the earlier v1 precheck only and is not validation of this edition. Current evidence is preparation-report.json and validation.md.\n')
    print(dump({'status': 'PREPARED', 'edition': EDITION, 'counts': counts, 'changed_ids': changed,
                'rewrite_sha256': report['rewrite_sha256'], 'warnings': len(report['warnings'])}))

if __name__ == '__main__':
    main()
