# Tur.ai Home: implementation handoff

**Current edition: enterprise-orchestration-handoff-v2**

Start at **[the implementation handoff](docs/IMPLEMENTATION_HANDOFF.md)**.

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

Webflow changes, visual acceptance and publication have NOT been performed. PR #1 remains the review/change record; a merge does not publish the website.

## Source snapshot

The immutable [baseline](baseline/home/2026-10-12/README.md) contains the original 228 fields, bindings, layout measurements and source checksums. It is not the new page copy. Do not modify it.
