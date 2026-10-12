"""Validate editorial budgets only. A pass is not visual or factual acceptance."""
import json, re, sys, pathlib, collections

ROOT=pathlib.Path(__file__).resolve().parent
normal=lambda x:re.sub(r'\s+',' ',x).strip()

def main():
    if len(sys.argv)!=2:
        print('Usage: python3 validate_rewrite.py completed_rewrite.json')
        return 2
    source=json.loads((ROOT/'inventory.json').read_text())['records']
    data=json.loads(pathlib.Path(sys.argv[1]).read_text())
    supplied=data.get('items',[])
    errors=[];warnings=[]
    ids=[i.get('id') for i in supplied]
    dup=[k for k,n in collections.Counter(ids).items() if n>1]
    if dup:errors.append('Duplicate IDs: '+str(dup))
    byid={i.get('id'):i for i in supplied}
    expected={r['id'] for r in source}
    if expected-set(byid):errors.append('Missing IDs: '+', '.join(sorted(expected-set(byid))))
    if set(byid)-expected:errors.append('Unknown IDs: '+', '.join(sorted(set(byid)-expected)))
    for r in source:
        item=byid.get(r['id'])
        if not item:continue
        rid=r['id'];action=item.get('action')
        if item.get('original_text')!=r['original_text']:errors.append(rid+': original_text changed')
        if item.get('max_chars')!=r['max_chars']:errors.append(rid+': max_chars changed')
        if action not in ('keep','rewrite','hold'):
            errors.append(rid+': choose keep, rewrite or hold');continue
        if action in ('keep','hold'):
            if item.get('new_text') not in (None,'',r['original_text']):
                errors.append(rid+': keep/hold must not contain replacement copy')
            if action=='hold' and not item.get('reason'):warnings.append(rid+': add hold reason')
            continue
        if r['policy'].startswith('hold'):
            errors.append(rid+': protected source; use hold with an editorial recommendation');continue
        new=item.get('new_text')
        if not isinstance(new,str) or not new.strip():errors.append(rid+': new_text is empty');continue
        if re.search(r'<[^>]+>',new):errors.append(rid+': new_text must be plain text')
        normalized=normal(new)
        if len(normalized)>r['max_chars']:
            errors.append(f"{rid}: {len(normalized)} characters exceeds {r['max_chars']}")
        if len(normalized)<r['target_chars'][0]:warnings.append(rid+': shorter than the soft target; review visual balance')
        longest=max(map(len,normalized.split()))
        if longest>r['longest_token_chars']:warnings.append(rid+': longer unbroken word/token; check wrapping')
        old_segments=r['segments']
        if len(old_segments)>1:
            segs=item.get('new_segments') or []
            if len(segs)!=len(old_segments):errors.append(rid+': preserve every rich-text segment');continue
            substitutions={}
            for old,seg in zip(old_segments,segs):
                if seg.get('source_id')!=old['source_id']:errors.append(rid+': segment IDs/order changed')
                if seg.get('max_chars')!=old['max_chars']:errors.append(rid+': segment budget changed')
                t=seg.get('new_text')
                if not isinstance(t,str):errors.append(rid+': missing segment text');continue
                if len(normal(t))>old['max_chars']:errors.append(rid+': segment exceeds character budget')
                if re.match(r'^\s*',t)[0]!=old['leading_whitespace'] or re.search(r'\s*$',t)[0]!=old['trailing_whitespace']:
                    errors.append(rid+': preserve segment boundary whitespace exactly')
                if '<' in t or '>' in t:errors.append(rid+': segment must be plain text')
                substitutions[old['source_id']['element']]=t
            def reconstruct(n):
                if n['type']=='String':return substitutions.get(n['id']['element'],n.get('text_raw') or '')
                if n['type']=='':return '\n'
                return ''.join(reconstruct(c) for c in n.get('children',[]))
            if normal(reconstruct(r['inline_structure']))!=normalized:
                errors.append(rid+': new_text does not match reconstructed segments')
        if r['evidence_required'] and not item.get('claim_evidence'):
            errors.append(rid+': provide claim_evidence or hold the claim')
        if item.get('layout_review')!='pending':
            warnings.append(rid+': layout_review should remain pending until actual Webflow visual checks')
    report={'status':'FAIL' if errors else 'EDITORIAL_LIMITS_PASS',
            'errors':errors,'warnings':warnings,
            'visual_acceptance':'NOT_CHECKED','claim_truth':'NOT_CHECKED','webflow_changed':False}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if errors else 0

if __name__=='__main__':sys.exit(main())
