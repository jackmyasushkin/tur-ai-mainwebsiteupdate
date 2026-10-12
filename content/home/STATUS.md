# Home update status

Recorded 13 October 2026.

| Stage | Status |
|---|---|
| Owner direction | Approved in the Home conversation: operational plane, quantified proof, task-matched models |
| Token-cost classification | Owner clarified: annual token spend, not license spend or full TCO |
| Exact replacement set | Complete: 228 decisions; 104 rewrite, 88 keep, 36 hold |
| Source fidelity | Local source JSON exactly matches Git blob `0c887e4b43b99e3d90f65c65ac717d363c307245` |
| Local text precheck | PASS: field/segment lengths, whitespace, protected values and paired copy |
| Full repository checker | Awaiting existing CI on this proposal |
| Full wording approval | Pending owner review of this edition |
| Webflow write | Not performed |
| Visual / functional acceptance | Not performed; `layout_review` remains `pending` |
| Publication | Not performed; requires separate explicit authorization |

The container could not check out the remote repository directly. Local validation
therefore does not claim to have run the baseline-manifest checker. The existing
GitHub workflow must run `python3 tools/check.py`, its validation tests, and
`python3 tools/check.py --complete`; `READY_FOR_REVIEW` requires completeness.

[Read the proposed copy](proposal.md) · [Exact values](rewrite.json) ·
[Evidence](evidence.md) · [Open questions](review-questions.md) ·
[Local precheck](local-precheck.json)

The immutable baseline, original checker, Webflow layout, links, forms and customer
assets are unchanged. Green CI is not approval of factual claims or permission to
publish.
