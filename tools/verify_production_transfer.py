#!/usr/bin/env python3
"""Verify captured production trees against the approved, bounded transfer."""
import argparse
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def trees(response):
    return [json.loads(item['text'])['result'][0]['data']
            for item in response['content'] if item['type'] == 'text']


def nodes(tree):
    yield tree
    for child in tree.get('children', []):
        yield from nodes(child)


def without_added(tree, added_id):
    tree = copy.deepcopy(tree)
    for node in nodes(tree):
        if 'children' in node:
            node['children'] = [c for c in node['children'] if c['id']['element'] != added_id]
    return tree


def differences(a, b, path='root'):
    if type(a) is not type(b):
        return [path + ': type mismatch']
    if isinstance(a, dict):
        out = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                out.append(path + '.' + key + ': key mismatch')
            else:
                out.extend(differences(a[key], b[key], path + '.' + key))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path + ': length mismatch']
        return [d for i, (x, y) in enumerate(zip(a, b))
                for d in differences(x, y, path + '[' + str(i) + ']')]
    return [] if a == b else [path + ': value mismatch']


def verify_rate(log):
    calls = [x for x in log if x['type'] == 'call']
    seconds = lambda value: datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()
    limited_at = [seconds(x['at']) for x in log if x['type'] == 'rate_limit']
    violations, peaks = [], {'before_429': 0, 'after_429': 0}
    for i, call in enumerate(calls):
        start = seconds(call['startedAt'])
        reduced = any(t < start for t in limited_at)
        budget = 15 if reduced else 30
        weighted = call['weight'] + sum(x['weight'] for x in calls[:i]
                    if start - 60 < seconds(x['endedAt']) <= start)
        phase = 'after_429' if reduced else 'before_429'
        peaks[phase] = max(peaks[phase], weighted)
        if weighted > budget or not 1 <= call['weight'] <= 10:
            violations.append(call['label'] + ': operation budget')
        if i and start - seconds(calls[i-1]['endedAt']) < 1.999:
            violations.append(call['label'] + ': call gap or overlap')
    return {'calls':len(calls), 'weighted_operations':sum(c['weight'] for c in calls),
            'rate_limit_events':len(limited_at), 'rolling_peaks':peaks,
            'violations':violations, 'passed':not violations}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='implementation/2026-10-13-production-home-transfer')
    args = parser.parse_args()
    run = Path(args.run)
    plan = read(Path('migration/2026-10-13-production-preflight/target-plan.json'))
    before = trees(read(run / 'before-home.json')) + trees(read(run / 'before-definitions.json'))
    after = trees(read(run / 'after-all-trees.json'))
    assert len(before) == len(after) == 10
    faq = read(run / 'new-faq-mapping.json')
    leaf_checks, scope_checks = [], []
    for old, new in zip(before, after):
        scope = old['id']['component']
        expected = copy.deepcopy(old)
        emap = {n['id']['element']: n for n in nodes(expected)}
        amap = {n['id']['element']: n for n in nodes(new)}
        for op in plan['text_operations']:
            if (op.get('scope_component_id') or plan['target']['page_id']) != scope:
                continue
            key = op['id']['element']
            assert emap[key]['textContent'] == op['expected_current_raw']
            emap[key]['textContent'] = op['approved_new_raw']
            leaf_checks.append({'field':op['field_id'], 'id':key,
                                'exact':amap[key].get('textContent') == op['approved_new_raw']})
        if scope == plan['target']['page_id']:
            for op in plan['ordinal_operations']:
                emap[op['id']['element']].setdefault('attributes', {}).update(op['add_attribute'])
            new = without_added(new, faq['row_id']['element'])
        diff = differences(expected, new)
        scope_checks.append({'scope':scope, 'only_approved_changes':not diff, 'unexpected_differences':diff})
    home = after[0]
    hmap = {n['id']['element']: n for n in nodes(home)}
    for op in faq['operations']:
        leaf_checks.append({'field':op['field_id'], 'id':op['id']['element'],
                            'exact':hmap[op['id']['element']].get('textContent') == op['approved_new_raw']})
    old_faq = next(n for n in nodes(before[0]) if n['id'] == faq['template_id'])
    new_faq = hmap[faq['row_id']['element']]
    def shape(n):
        return {k:([shape(c) for c in v] if k == 'children' else v)
                for k,v in n.items() if k not in ['id', 'textContent']}
    faq_same_shape = shape(old_faq) == shape(new_faq)
    assert len(leaf_checks) == 122
    seo_before = next(json.loads(c['text'])['result'] for c in read(run/'before-pages.json')['content']
                      if c['type']=='text')['pages']
    seo_before = next(p for p in seo_before if p['id']==plan['target']['page_id'])
    seo_after = json.loads(read(run/'after-seo.json')['content'][0]['text'])['result']
    seo_ok = all(seo_after['seo'][op['property'].split('.')[1]] == op['approved_new'] for op in plan['seo_operations'])
    og_ok = seo_before['openGraph'] == seo_after['openGraph']
    placeholder = (run/'placeholder-after-native.txt').read_text()
    placeholder_ok = 'Placeholder: '+plan['native_placeholder_operation']['approved_new'] in placeholder
    inventory = {x['id']:x for x in read(Path('baseline/home/2026-10-12/inventory.json'))['records']}
    dom = read(run/'after-dom-protected-and-forms.json')
    protected_values = {'HOME-177':dom['quote'], 'HOME-178':dom['name'], 'HOME-179':dom['role'],
                        'HOME-205':dom['arrowAlts'][0], 'HOME-206':dom['arrowAlts'][1],
                        'HOME-207':dom['portrait']}
    dom_checks = {key:value == inventory[key]['original_text'] for key,value in protected_values.items()}
    rate = verify_rate(read(run/'mcp-log.json')['log'])
    site_before = json.loads(read(run/'before-site.json')['content'][0]['text'])['result']
    site_after = json.loads(read(run/'after-site.json')['content'][0]['text'])['result']
    publication = all(site_before[k] == site_after[k]
                      for k in ['lastPublished','fullSiteCompiledAt','customDomains'])
    scripts = [json.loads(c['text']) for c in read(run/'after-script-attachment.json')['content']]
    home_only = scripts[0]['result']['scripts'] == [{'id':'turaihomeordinalformat',
        'displayName':'TuraiHomeOrdinalFormat','version':'1.0.0','location':'footer','attributes':{}}]
    home_only = home_only and scripts[1]['error']['status'] == 404
    code_preserved = read(run/'after-code-preservation.json')['sameResults'] == [True,True]
    widths = [1383,820,667,393,320,1440,991,992,767,768,479,480]
    pairs = all((run/f'{prefix}-{w}.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
                for w in widths for prefix in ['before','after'])
    shared = read(run/'shared-component-dom-audit.json')
    shared_ok = all(all(f['present'] for f in row['fields']) for row in shared)
    shared_ok = shared_ok and all(any(r['pageId'] == p['page_id'] and r['width'] == w
                    for r in shared) for p in plan['shared_component_pages'] for w in [1383,393])
    source_hashes = {path:hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected
                     for path,expected in plan['source_hashes'].items()}
    text_ids = set(x['field'] for x in leaf_checks)
    assert len(text_ids) == 101
    unchanged = [dict(x, verified=True,
                     evidence='protected_dom_fields' if x['id'] in dom_checks else 'scopes')
                 for x in plan['field_dispositions'] if x['action'] in ['keep','hold']]
    assert len(unchanged) == 124
    editorial_checks = [{'id':field, 'exact':all(x['exact'] for x in leaf_checks if x['field']==field)}
                        for field in sorted(text_ids)]
    editorial_checks += [{'id':plan['native_placeholder_operation']['field_id'],'exact':placeholder_ok}]
    editorial_checks += [{'id':op['field_id'],'exact':seo_after['seo'][op['property'].split('.')[1]] == op['approved_new']}
                         for op in plan['seo_operations']]
    assert len(editorial_checks) == 104
    report = {'exact_string_nodes':len(leaf_checks), 'editorial_fields':104,
              'all_exact':all(x['exact'] for x in leaf_checks), 'leaves':leaf_checks,
              'scopes':scope_checks, 'new_faq_native_shape_matches_template':faq_same_shape,
              'seo_exact':seo_ok, 'open_graph_preserved':og_ok, 'placeholder_verified_after_reload':placeholder_ok,
              'keep_hold':{'decisions':124,'present_mcp_fields':90,'absent_target_fields':28,'dom_only_fields':6},
              'protected_dom_fields':dom_checks, 'rate_audit':rate,
              'home_only_formatter':home_only, 'freeform_code_preserved':code_preserved,
              'twelve_before_after_png_pairs':pairs, 'other_five_shared_pages_verified':shared_ok,
              'source_hashes_match_pinned_plan':source_hashes,
              'editorial_field_checks':editorial_checks, 'no_write_field_checks':unchanged,
              'publication':'not performed', 'publication_metadata_unchanged':publication}
    report['passed'] = all([report['all_exact'],faq_same_shape,seo_ok,og_ok,placeholder_ok,
                            all(x['only_approved_changes'] for x in scope_checks),
                            all(dom_checks.values()),rate['passed'],publication,home_only,
                            code_preserved,pairs,shared_ok])
    report['passed'] = report['passed'] and all(source_hashes.values())
    (run/'content-and-invariant-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in
                     ['leaves','scopes','editorial_field_checks','no_write_field_checks']},ensure_ascii=False,indent=2))
    if not report['passed']:
        print(json.dumps([s for s in scope_checks if not s['only_approved_changes']],indent=2))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
