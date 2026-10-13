# Tur.ai Home: sandbox implementation

**Current edition: enterprise-orchestration-handoff-v2**

**104 replacements are applied in the sandbox; 124 keep/hold decisions are preserved.** Start at [the content implementation report](implementation/2026-10-13-enterprise-orchestration/REPORT.md). Its animation decision and publication status describe that historical run. The subsequent owner-approved [ordinal animation fix](implementation/2026-10-13-ordinal-animation/REPORT.md) preserves Number Count and displays `01–04` with leading zeros. It is applied to the Home draft and verified in Designer custom-code Preview.

The ordinal fix was not published by this run. Preflight and final site reads both report an earlier sandbox publication at `2026-10-13T01:53:31.599Z`. No automatic merge is performed.

The [original implementation handoff](docs/IMPLEMENTATION_HANDOFF.md) describes the prepared source edition; its preparation-stage statements are historical.

- [Exact replacements](content/home/rewrite.json) and [machine apply plan](content/home/apply-plan.json)
- [Copy in page order](content/home/proposal.md)
- [Approved direction](content/home/business-brief.md), [decisions](content/home/decisions.md), [evidence](content/home/evidence.md)
- [Status](content/home/STATUS.md), [validation](content/home/validation.md), [known holds](content/home/review-questions.md)

Approved hero:

> **Enterprise Process Orchestration Platform**
>
> Run regulated processes across existing systems. Customers trust us to help them work faster today and change faster tomorrow.

Prepare and validate, without writing to Webflow:

```sh
python3 tools/check.py --complete
python3 -m unittest discover -s tools -p "test_*.py"
python3 tools/verify_home_handoff.py
```

HOME-003 has one explicit exact-copy segment exception. The original baseline and budgets are unchanged. See `implementation-overrides.json`; do not silence arbitrary validation errors.

Webflow changes are applied and read back. Producer review is recorded; independent acceptance has not occurred. Form-state limits remain documented in the content run. PR #1 remains open; a merge does not publish the website.

## Source snapshot

The immutable [baseline](baseline/home/2026-10-12/README.md) contains the original 228 fields, bindings, layout measurements and source checksums. It is not the new page copy. Do not modify it.
