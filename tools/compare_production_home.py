#!/usr/bin/env python3
"""Read-only cross-site Home mapping. No API, browser, or mutation capability.

Inputs are saved JSON MCP read results, trees, and optional Designer DOM field
reads. Every UUID match is corroborated by context; absent data stays unknown.
"""
import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

UNKNOWN = object()
ORDINALS = ['HOME-071', 'HOME-074', 'HOME-077', 'HOME-080']


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def unpack(value):
    if isinstance(value, dict):
        if 'content' in value:
            result = []
            for part in value['content']:
                if part.get('type') == 'text':
                    try:
                        result.append(unpack(json.loads(part['text'])))
                    except (ValueError, TypeError):
                        pass
            return result
        return {k: unpack(v) for k, v in value.items()}
    if isinstance(value, list):
        return [unpack(v) for v in value]
    return value


def gather(value, predicate):
    if isinstance(value, dict):
        if predicate(value):
            yield value
            return
        for v in value.values():
            yield from gather(v, predicate)
    elif isinstance(value, list):
        for v in value:
            yield from gather(v, predicate)


def signature(n):
    return (n.get('type'), tuple(n.get('styleNames', [])))


def flatten(tree):
    nodes = {}
    paths = {}
    by_path = {}
    def walk(n, path=()):
        nid = n.get('id', {})
        if isinstance(nid, dict) and nid.get('element'):
            nodes[nid['element']] = n
            paths[nid['element']] = path
            by_path[path] = n
        for i, c in enumerate(n.get('children', [])):
            walk(c, path + ((i, signature(c)),))
    walk(tree)
    return {'tree': tree, 'nodes': nodes, 'paths': paths, 'by_path': by_path}


class Snapshot:
    def __init__(self, files):
        self.files = [str(p) for p in files]
        self.scopes = {}
        self.names = {}
        self.metadata = None
        self.dom_fields = {}
        self.site = None
        metadata_candidates = []
        catalog_names = {}
        for f in files:
            raw = unpack(read(f))
            for tree in gather(raw, lambda x: isinstance(x.get('id'), dict) and 'type' in x and 'element' in x['id']):
                sid = tree['id']['component']
                self.scopes[sid] = flatten(tree)
            for meta in gather(raw, lambda x: 'seo' in x and 'siteId' in x and isinstance(x.get('id'), str)):
                metadata_candidates.append(meta)
            for comp in gather(raw, lambda x: isinstance(x.get('id'), str) and 'name' in x and 'instanceCount' in x):
                catalog_names[comp['id']] = comp['name']
            for site in gather(raw, lambda x: 'workspaceId' in x and 'lastPublished' in x):
                if isinstance(site.get('id'), str):
                    self.site = site
            for fields in gather(raw, lambda x: isinstance(x.get('dom_fields'), dict)):
                self.dom_fields.update(fields['dom_fields'])
        self.names.update(catalog_names)
        for meta in metadata_candidates:
            if meta.get('id') in self.scopes and self.scopes[meta['id']]['tree'].get('type') == 'Body':
                self.metadata = meta
        for scope in self.scopes.values():
            for n in scope['nodes'].values():
                instance = n.get('instanceDetails', {})
                if instance.get('id') and instance.get('name'):
                    self.names[instance['id']] = instance['name']
        home_candidates = [sid for sid, val in self.scopes.items() if val['tree'].get('type') == 'Body']
        meta_home = self.metadata and self.metadata.get('id')
        self.home = meta_home if meta_home in self.scopes else home_candidates[0] if len(home_candidates) == 1 else None
        if self.home:
            self.names[self.home] = 'Home'


class Mapper:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.scope_map = {}
        self.scope_errors = []
        for sid in source.scopes:
            if sid == source.home and target.home:
                self.scope_map[sid] = target.home
                continue
            name = source.names.get(sid)
            matches = [k for k, v in target.names.items() if v == name] if name else []
            if len(matches) == 1 and matches[0] in target.scopes:
                self.scope_map[sid] = matches[0]
            elif sid in target.scopes and name and target.names.get(sid) == name:
                self.scope_map[sid] = sid
            else:
                self.scope_errors.append({'source_scope': sid, 'name': name, 'reason': 'missing_or_ambiguous_component_scope'})

    def map_id(self, ref):
        sid, eid = ref['component'], ref['element']
        if sid not in self.source.scopes or sid not in self.scope_map:
            return {'status': 'unverified', 'reason': 'scope_not_resolved', 'source_id': ref}
        src = self.source.scopes[sid]
        tgt = self.target.scopes[self.scope_map[sid]]
        if eid not in src['nodes']:
            return {'status': 'unverified', 'reason': 'source_node_not_exposed_by_mcp', 'source_id': ref}
        a = src['nodes'][eid]
        path = src['paths'][eid]
        b = tgt['nodes'].get(eid)
        evidence = 'same_element_uuid_and_structural_context'
        if b is None:
            b = tgt['by_path'].get(path)
            evidence = 'full_child_index_type_style_path'
        if b is None:
            return {'status': 'conflict', 'reason': 'target_node_missing', 'source_id': ref}
        bid = b['id']['element']
        if signature(a) != signature(b) or tgt['paths'][bid] != path:
            return {'status': 'conflict', 'reason': 'uuid_context_or_type_style_path_mismatch', 'source_id': ref, 'candidate_id': b['id']}
        # Root context is independently identified as Home or named component.
        return {'status': 'mapped', 'source_id': ref, 'target_id': b['id'], 'evidence': evidence, 'component_name': self.source.names.get(sid, 'unknown'), 'type': b['type'], 'style_names': b.get('styleNames', []), 'path': [list(p) for p in path]}

    def node(self, mapped):
        ref = mapped.get('target_id')
        return self.target.scopes[ref['component']]['nodes'][ref['element']] if ref else None

    def prop(self, record):
        prop = record.get('component_prop') or {}
        chain = record.get('component_instance_chain') or []
        if not chain:
            return UNKNOWN, []
        current = self.source.home
        mapped_chain = []
        target_instance = None
        for eid in chain:
            mapped = self.map_id({'component': current, 'element': eid})
            mapped_chain.append(mapped)
            if mapped['status'] != 'mapped':
                return UNKNOWN, mapped_chain
            original_instance = self.source.scopes[current]['nodes'].get(eid, {}).get('instanceDetails', {})
            target_instance = self.node(mapped).get('instanceDetails', {})
            current = original_instance.get('id')
        candidates = [p for p in target_instance.get('props', []) if p.get('propId') == prop.get('propId') and p.get('name') == prop.get('name')]
        if len(candidates) != 1:
            candidates = [p for p in target_instance.get('props', []) if p.get('name') == prop.get('name')]
        return (candidates[0].get('value', UNKNOWN), mapped_chain) if len(candidates) == 1 else (UNKNOWN, mapped_chain)


def attribute_value(node, attribute):
    attrs = node.get('attributes', {})
    if isinstance(attrs, list):
        attrs = dict(attrs)
    if attribute in attrs:
        return attrs[attribute]
    settings = node.get('settings', {})
    if attribute == 'alt' and 'altText' in settings:
        return settings['altText']
    input_ = settings.get('input', {})
    aliases = {'placeholder': ['placeholder', 'placeholderText'], 'value': ['value', 'text'], 'data-wait': ['waitingText', 'waitText']}
    for k in aliases.get(attribute, []):
        for container in (settings, input_):
            if k in container:
                return container[k]
    return UNKNOWN


def field_value(record, mapper):
    field_id = record['id']
    field_type = record['source_field']
    if field_type.startswith('seo.'):
        meta = mapper.target.metadata
        return meta.get('seo', {}).get(field_type.split('.', 1)[1], UNKNOWN) if meta else UNKNOWN, []
    if field_type == 'component_instance_prop':
        return mapper.prop(record)
    refs = [segment['source_id'] for segment in record.get('segments', [])] if field_type == 'textContent' and record.get('segments') else [record['source_id']]
    mappings = [mapper.map_id(ref) for ref in refs]
    if field_id in mapper.target.dom_fields:
        return mapper.target.dom_fields[field_id].get('value', UNKNOWN), mappings
    if any(m['status'] != 'mapped' for m in mappings):
        return UNKNOWN, mappings
    nodes = [mapper.node(m) for m in mappings]
    if field_type == 'textContent':
        values = [n.get('textContent', UNKNOWN) for n in nodes]
        return (''.join(values) if all(v is not UNKNOWN for v in values) else UNKNOWN), mappings
    if field_type.startswith('attribute:'):
        return attribute_value(nodes[0], field_type.split(':', 1)[1]), mappings
    if field_type.startswith('option:'):
        index = int(field_type.split(':')[1])
        options = nodes[0].get('settings', {}).get('input', {}).get('options', UNKNOWN)
        if options is UNKNOWN:
            return UNKNOWN, mappings
        try:
            opt = options[index]
            return opt.get('text', opt.get('label', UNKNOWN)) if isinstance(opt, dict) else opt, mappings
        except (IndexError, TypeError):
            return UNKNOWN, mappings
    return UNKNOWN, mappings


def safe_compare(a, b):
    return a is not UNKNOWN and norm(a) == norm(b)


def semantic_changes(source, target, mapper):
    changes = []
    counts = Counter()
    for sid, scope in source.scopes.items():
        if sid not in mapper.scope_map:
            continue
        target_scope = target.scopes[mapper.scope_map[sid]]
        counts['source_nodes'] += len(scope['nodes'])
        counts['target_nodes'] += len(target_scope['nodes'])
        mapped_target_ids = set()
        for eid, n in scope['nodes'].items():
            m = mapper.map_id(n['id'])
            if m['status'] != 'mapped':
                counts['unmapped_nodes'] += 1
                changes.append({'scope': source.names.get(sid, sid), 'source_id': n['id'], 'mapping_status': m['status'], 'reason': m['reason']})
                continue
            other = mapper.node(m)
            mapped_target_ids.add(other['id']['element'])
            for key in sorted(set(n) | set(other)):
                if key in ('id', 'children', 'styleNames', 'type'):
                    continue
                left = copy.deepcopy(n.get(key))
                right = copy.deepcopy(other.get(key))
                if key == 'settings' and isinstance(left, dict) and isinstance(right, dict):
                    # Clone-owned asset IDs are not meaningful text/style changes.
                    left.pop('assetId', None)
                    right.pop('assetId', None)
                if key == 'instanceDetails' and isinstance(left, dict) and isinstance(right, dict):
                    left['id'] = mapper.scope_map.get(left.get('id'), left.get('id'))
                if left != right:
                    counts[key + '_differences'] += 1
                    changes.append({'scope': source.names.get(sid, sid), 'source_id': n['id'], 'target_id': other['id'], 'property': key, 'source': left, 'target': right})
        for tid in sorted(set(target_scope['nodes']) - mapped_target_ids):
            counts['target_only_nodes'] += 1
            changes.append({'scope': source.names.get(sid, sid), 'target_id': target_scope['nodes'][tid]['id'], 'mapping_status': 'target_only_node', 'type':target_scope['nodes'][tid].get('type'), 'style_names':target_scope['nodes'][tid].get('styleNames', [])})
    return {'counts': dict(counts), 'differences': changes, 'limit': 'Only exposed MCP tree properties compared. CSS declarations, embeds, interactions, form integrations and DOM-only values require separate reads.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--production', action='append', default=[], required=True)
    ap.add_argument('--sandbox', action='append', default=[])
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    repo = Path(args.repo)
    source_file = repo / 'implementation/2026-10-13-enterprise-orchestration/before-readset.json'
    accepted_file = repo / 'implementation/2026-10-13-enterprise-orchestration/after-trees.json'
    inventory = read(repo / 'baseline/home/2026-10-12/inventory.json')
    plan = read(repo / 'content/home/apply-plan.json')
    source = Snapshot([source_file])
    production = Snapshot(args.production)
    live = Snapshot(args.sandbox) if args.sandbox else None
    pm = Mapper(source, production)
    sm = Mapper(source, live) if live else None
    records = {r['id']: r for r in inventory['records']}
    results = []
    for item in plan['items']:
        record = records[item['id']]
        before, mappings = field_value(record, pm)
        expected = item['expected_original_text']
        desired = item['target_text'] if item['action'] == 'rewrite' else expected
        original_equal = safe_compare(before, expected)
        desired_equal = safe_compare(before, desired)
        current_segments = None
        if record['source_field'] == 'textContent' and record.get('segments') and all(m['status'] == 'mapped' for m in mappings):
            current_segments = [pm.node(m).get('textContent', None) for m in mappings]
            expected_segments = [s['text_raw'] for s in record['segments']]
            desired_segments = ([s['new_text'] for s in item['segments']] if item['segments'] else [desired]) if item['action'] == 'rewrite' else expected_segments
            original_equal = current_segments == expected_segments
            desired_equal = current_segments == desired_segments
        if any(m['status'] == 'conflict' for m in mappings):
            state = 'binding_conflict'
        elif before is UNKNOWN:
            state = 'value_unverified'
        elif desired_equal:
            state = 'already_correct' if item['action'] == 'rewrite' else 'no_write_matches_baseline'
        elif original_equal:
            state = 'eligible_from_baseline' if item['action'] == 'rewrite' else 'no_write_matches_baseline'
        else:
            state = 'production_value_conflict'
        home_instance_presence = True
        chain_context = []
        current_scope = source.home
        for instance_id in record.get('component_instance_chain', []):
            cm = pm.map_id({'component': current_scope, 'element': instance_id})
            chain_context.append(cm)
            if cm['status'] != 'mapped':
                home_instance_presence = False
                break
            current_scope = source.scopes[current_scope]['nodes'][instance_id].get('instanceDetails', {}).get('id')
        if state == 'binding_conflict' and item['action'] != 'rewrite' and all(m.get('reason') == 'target_node_missing' for m in mappings):
            state = 'no_write_node_absent_on_target_home'
        if not home_instance_presence and item['action'] != 'rewrite':
            state = 'no_write_component_not_instanced_on_target_home'
        row = {'id': item['id'], 'action': item['action'], 'source_field': record['source_field'], 'section': record['section'], 'status': state, 'expected_original': expected, 'desired': desired, 'current_production': None if before is UNKNOWN else before, 'production_mappings': mappings, 'current_production_raw_segments': current_segments, 'home_instance_presence': home_instance_presence, 'home_instance_chain_mapping': chain_context}
        if sm:
            current_live, live_mapping = field_value(record, sm)
            row['sandbox_verified'] = None if current_live is UNKNOWN else safe_compare(current_live, desired)
            if record['source_field'] == 'textContent' and record.get('segments') and all(m['status'] == 'mapped' for m in live_mapping):
                live_segments = [sm.node(m).get('textContent', None) for m in live_mapping]
                desired_segments = ([s['new_text'] for s in item['segments']] if item['segments'] else [desired]) if item['action'] == 'rewrite' else [s['text_raw'] for s in record['segments']]
                row['sandbox_verified'] = live_segments == desired_segments
                row['current_sandbox_raw_segments'] = live_segments
            row['current_sandbox'] = None if current_live is UNKNOWN else current_live
        results.append(row)
    ops = read(repo / 'implementation/2026-10-13-enterprise-orchestration/planned-text-operations.json')
    exact_ops = []
    for op in ops:
        mapped = pm.map_id(op['id'])
        node = pm.node(mapped)
        current = node.get('textContent', UNKNOWN) if node else UNKNOWN
        exact_ops.append({**op, 'sandbox_id': op['id'], 'id': mapped.get('target_id'), 'production_before': None if current is UNKNOWN else current, 'mapping': mapped, 'status': 'eligible' if current == op['before'] else 'already_correct' if current == op['after'] else 'unknown' if current is UNKNOWN else 'conflict'})
    ordinals = []
    for field_id in ORDINALS:
        record = records[field_id]
        m = pm.map_id(record['source_id'])
        n = pm.node(m) or {}
        attrs = n.get('attributes', {})
        ordinals.append({'field_id': field_id, 'mapping': m, 'current_attributes': attrs, 'required_preserved_attribute': {'fs-numbercount-element': 'number'}, 'proposed_added_attribute': {'data-tur-number-format': 'ordinal-2'}, 'current_marker': attrs.get('data-tur-number-format'), 'animation_attribute_verified': attrs.get('fs-numbercount-element') == 'number'})
    output = {'read_only': True, 'edition': plan['edition'], 'source_commit': '086ce563960473a70221dccb8c7092507fa93e3b', 'ordinal_fix_commit': '5e3fad4', 'owner_acceptance_commit': '8f35796', 'production_home_page_id': production.home, 'scope_mapping': pm.scope_map, 'scope_errors': pm.scope_errors, 'input_sha256': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in production.files + (live.files if live else [])}, 'counts': dict(Counter(r['status'] for r in results)), 'rewrite_counts': dict(Counter(r['status'] for r in results if r['action'] == 'rewrite')), 'no_write_counts': dict(Counter(r['status'] for r in results if r['action'] != 'rewrite')), 'text_operation_counts': dict(Counter(r['status'] for r in exact_ops)), 'fields': results, 'planned_text_operations': exact_ops, 'ordinal_marker_mappings': ordinals, 'exposed_structure_settings_comparison': semantic_changes(source, production, pm), 'limitations': ['UUID equality alone is never accepted; scope and structural context corroborate every mapping.', 'Normalized aggregate equality is insufficient for write execution: exact segment raw strings are recorded separately.', 'No Webflow mutation authorization is implied by an eligible mapping.', 'DOM-only and absent form attributes remain unverified until read directly.', 'Shared components require production-wide usage inventory before mutation.']}
    Path(args.out).write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({k: output[k] for k in ['counts', 'rewrite_counts', 'no_write_counts', 'text_operation_counts', 'scope_errors']}, indent=2))

if __name__ == '__main__':
    main()
