# Tur.ai Home: original-project transfer

**Current edition: enterprise-orchestration-handoff-v2**

**104 replacements are applied in the sandbox; 124 keep/hold decisions are preserved.** Start at [the content implementation report](implementation/2026-10-13-enterprise-orchestration/REPORT.md). Its animation decision and publication status describe that historical run. The subsequent owner-approved [ordinal animation fix](implementation/2026-10-13-ordinal-animation/REPORT.md) preserves Number Count and displays `01–04` with leading zeros. **The owner has published the fix and confirmed it works.** See the [publication and owner acceptance record](implementation/2026-10-13-ordinal-animation-acceptance/ACCEPTANCE.md).

Current Webflow metadata confirms the sandbox publication at `2026-10-13T05:42:48.576Z`. The agent did not publish or merge PRs. Historical before/after reads remain intact.

**The transfer to the original Tur.ai project is applied and producer-verified, without publication.** See the [production transfer report](implementation/2026-10-13-production-home-transfer/REPORT.md): 104 editorial changes, 124 keep/hold decisions, one native FAQ addition, the Home-only ordinal fix, 12 responsive image pairs and checks on six English pages. The existing footer award overflow at 480px remains documented. The [transfer strategy](docs/PRODUCTION_TRANSFER_STRATEGY.md) is the historical approved plan; do not replay it.

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

Webflow changes are applied and read back. Producer review and owner acceptance of the published ordinal animation fix are recorded. Form-state limits remain documented in the content run. PR #1 remains open; a merge does not publish the website.

## Source snapshot

The immutable [baseline](baseline/home/2026-10-12/README.md) contains the original 228 fields, bindings, layout measurements and source checksums. It is not the new page copy. Do not modify it.
