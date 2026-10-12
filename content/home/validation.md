# Validation record — Home content proposal

Recorded 13 October 2026 for [PR #1](https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/pull/1). No Webflow changes or publication.

## Executed repository checks

Source: decoded log of GitHub Actions job `115060973004`, [run 38324831525](https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/actions/runs/38324831525).

| Check | Result |
|---|---|
| `python3 tools/check.py` | `EDITORIAL_LIMITS_PASS` |
| `python3 -m unittest discover -s tools -p 'test_*.py'` | 9 tests passed |
| `python3 tools/check.py --complete` | `EDITORIAL_LIMITS_PASS`; `complete_required: true` |
| Decisions | 88 keep, 104 rewrite, 36 hold, 0 pending |
| Errors | None |
| Warnings | 36, across 32 fields |
| Visual acceptance | `NOT_CHECKED` |
| Claim truth | `NOT_CHECKED` by the automated checker; source boundaries are documented separately in evidence.md |
| Webflow changed | `false` |

Tested proposal commit: `213e15c8ee697b5b365c14f213eb045712f58f2b`.
PR test merge ref: `7a389534ef2da8e3b81c829c649080ed30f5e6f4`.
Tested replacement blob: `c792821fc5b6d5a2f788090748f605766544c782`.
The workflow, validation safeguards and immutable baseline were not modified to obtain this result.

## Warning review

### Shorter than the soft target — 18 warnings

HOME-007, HOME-011, HOME-015, HOME-027, HOME-029, HOME-035, HOME-045, HOME-047, HOME-059, HOME-066, HOME-068, HOME-073, HOME-076, HOME-117, HOME-119, HOME-121, HOME-135, HOME-227.

Editorial disposition: retain the shorter wording. It removes generic claims, specifies a case or states the point with fewer words. Do not pad text merely to meet a soft target. Visual balance and adjacent card heights still require the Webflow pass; SEO title HOME-227 is not a visible layout block.

### Longer unbroken word/token — 18 warnings

HOME-004, HOME-015, HOME-033, HOME-043, HOME-044, HOME-056, HOME-085, HOME-113, HOME-114, HOME-118, HOME-119, HOME-120, HOME-121, HOME-122, HOME-123, HOME-133, HOME-135, HOME-152.

Editorial disposition: retain meaningful terms such as traceability, staffing requirement and lead-to-quote. The warning compares the longest token with the original, not with an actual pixel width. Check wrapping in the existing fonts at all target widths. Do not mask a problem with smaller fonts, nonbreaking spaces, soft hyphens, hidden overflow or additional manual line breaks.

These are acknowledged review items, not verified visual passes. The 3x multiplier and 01.-04. ordinal replacements also need visual review even though the checker accepts their lengths.

## Before implementation

Re-read the live Webflow page and reconcile any source drift. Apply only after the owner approves the complete wording and explicitly authorizes implementation. Preserve all IDs, links, component scopes, form behavior and source paragraph structures. Check the baseline widths and interactive states defined in the repository workflow. Resolve the case-link and attribution issues in review-questions.md before publication.

`hold` means no write. It does not hide, delete, certify or approve the original content.
