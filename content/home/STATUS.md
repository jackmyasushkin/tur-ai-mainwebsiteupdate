# Home update status

Recorded 13 October 2026. [Review PR #1](https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/pull/1).

| Stage | Status |
|---|---|
| Owner direction | Approved: operational plane, quantified proof, task-matched models |
| Token-cost classification | Owner clarified: annual token spend, not license spend or full TCO |
| Exact replacement set | Complete: 228 decisions; 104 rewrite, 88 keep, 36 hold |
| Source fidelity | Original source JSON matched Git blob `0c887e4b43b99e3d90f65c65ac717d363c307245` |
| Local text precheck | PASS: field/segment lengths, whitespace, protected values and paired copy |
| Full repository checker | PASS in existing GitHub Actions: `EDITORIAL_LIMITS_PASS`, including `--complete` |
| Validation safeguards | All 9 tests passed |
| Errors / pending decisions | 0 / 0 |
| Non-blocking warnings | 36 wrapping/shorter-copy warnings, retained for visual review; see validation.md |
| Full wording approval | Pending owner review of this edition |
| Webflow write | Not performed |
| Visual / functional acceptance | Not performed; `layout_review` remains `pending` |
| Publication | Not performed; requires separate explicit authorization |

## Verified CI

[Content checks run 38324831525](https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/actions/runs/38324831525), job `115060973004`, completed successfully at 2026-10-12 23:57 UTC (13 October in Kyiv).

The run tested proposal commit `213e15c8ee697b5b365c14f213eb045712f58f2b` through PR merge ref `7a389534ef2da8e3b81c829c649080ed30f5e6f4`. The tested `rewrite.json` blob is `c792821fc5b6d5a2f788090748f605766544c782`. This status update does not change the replacement set or the checker.

The container could not check out the remote repository directly. The full source-manifest and editorial checks were therefore executed by the repository's unchanged GitHub Actions workflow, not represented as local execution. `local-precheck.json` preserves the earlier pre-CI snapshot; this status and [validation.md](validation.md) record the later CI result.

[Proposed copy](proposal.md) · [Exact values](rewrite.json) · [Evidence](evidence.md) · [Open questions](review-questions.md) · [Validation](validation.md)

The immutable baseline, original checker, Webflow layout, links, forms and customer assets are unchanged. Green CI is not factual-claim approval, visual acceptance or permission to publish.
