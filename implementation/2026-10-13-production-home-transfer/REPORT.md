# Original Tur.ai Home transfer — 13 October 2026

**APPLIED_AND_PRODUCER_VERIFIED_UNPUBLISHED.** All 104 approved editorial fields and the previously accepted ordinal formatter are applied to original Tur.ai. Publication and owner acceptance of this target remain separate steps. No PR was merged and no site was published.

Target: site `64e477696d41401ec48c50c6`, English Home `66368e29da23c5a1b0fe1396`. Source: edition `enterprise-orchestration-handoff-v2`, commit `086ce563960473a70221dccb8c7092507fa93e3b`, accepted sandbox ordinal fix. The owner authorized execution after [plan PR #6](https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/pull/6) and explicitly approved adding the absent process-fit FAQ.

## Applied result

| Item | Confirmed result |
|---|---|
| Copy | 120 mapped existing String nodes plus 2 native FAQ String nodes exact on readback; 101 editorial text fields |
| Placeholder | 1 native Placeholder edited in Designer and verified after reload |
| SEO | 2 exact fields; inherited Open Graph and its image unchanged |
| Shared scope | 7 definition changes applied once in Footer, Modal Demo and Modal Contact |
| Keep/hold | 124 decisions preserved: 90 present MCP fields, 28 absent target fields left absent, 6 protected DOM fields exact |
| FAQ | One existing production row duplicated natively; target-owned IDs, classes and structure verified against its template |
| Ordinals | Four `data-tur-number-format=ordinal-2` markers added; `fs-numbercount-element=number` retained |
| Formatter | `TuraiHomeOrdinalFormat` v1.0.0 registered on the target and attached only to English Home's footer |
| Existing code | Original Home/site freeform code unchanged on fresh comparison; no site-wide app script added |
| Structure | Ten captured page/definition scopes match the expected trees after only the approved text, marker and FAQ changes |

The exact H1 remains `Enterprise Process Orchestration Platform`, with existing blue highlighting only on `Process`. Four segment boundaries and trailing spaces are preserved. Production links, styles, asset references, form settings and integrations were retained. The source sandbox's endpoints and project configuration were not copied.

The native restore point was created before writes: **13 October 2026, 11:43:59 local**, description `Before approved Home transfer 2026-10-13 | target 64e477696d41401ec48c50c6 | no publication`. See [backup confirmation](before-native-backup.txt). Raw custom code containing operational configuration was kept outside Git; [code hashes](before-code-summary.json) and [exact comparison results](after-code-preservation.json) are committed.

## Producer verification

Run `python3 tools/verify_production_transfer.py` to reproduce the [content and invariant audit](content-and-invariant-audit.json). This verifies the 122 exact String nodes, new FAQ shape, protected DOM values, SEO, Open Graph, placeholder, code preservation evidence, script placement, shared-page checks, responsive image pairs, call pacing and unchanged publication metadata. It verifies saved evidence, not future live state.

Home was compared at **1383, 820, 667, 393, 320, 1440, 991, 992, 767, 768, 479 and 480px**. All twelve before/after full-page PNG pairs are retained. Use [the evidence viewer](EVIDENCE.html) or [layout measurements](layout-dom-audit.json). No new horizontal overflow was found. At 480px the existing award row extends to 512px; the same clipped Spinawards logo is present in both captures. See [the isolated finding](KNOWN_ISSUES.md).

Home Preview with custom code enabled was exercised on desktop/mobile: both toggle states, four mobile case slides, two desktop case groups covering four cases, PILOT/LAUNCH/SCALE tabs, all eight FAQ rows opened and closed, CTA demo/contact modals and normal form layout. `3×` and all four settled `01.–04.` values were checked. Before completion, English Home was returned to Designer at 1383px. [Desktop interaction state checks](desktop-interaction-checks.json) and `qa-home-*` images record these states.

On Home, Radio Holland Case, Heineken Cashback, Heineken Procurement, Imprint EN and Privacy Policy EN, the exact seven shared values were verified. All five secondary pages have desktop demo/contact modal screenshots and desktop/mobile footer screenshots; [DOM audit](shared-component-dom-audit.json) confirms propagation at both widths. On those secondary pages, mobile navigation hides the modal trigger links, as before. Their mobile modal opening is not claimed; the shared modal layout was exercised on Home mobile and the same definitions/styles are retained on all pages.

No form was submitted. Success/error copy is confirmed in the saved definitions and page DOM; actual post-submit rendering and delivery are not tested. Initial Preview scroll-reveal states and smooth scrolling can produce transient blank/offscreen captures. `qa-preview-before-scroll-1383.png` is labeled as such and is not the final layout comparison. No independent acceptance review or published-site QA is claimed.

## Pacing and recovery

[The complete MCP log](mcp-log.json) records 131 calls and 273 weighted operations, including reads and validation failures. Calls were sequential, at most 10 actions per batch, at least 2 seconds apart. Recorded rolling peaks are 23 operations before throttling and 15 afterward; the audit has no pacing violations.

At `2026-10-13T08:49:29.984Z`, a guard read returned a nested `GET /v2/pages` 429 without exposed Retry-After. All calls were paused for 62 seconds, the budget was reduced to 15/min, and the affected group's actual state was reconciled before continuing. No applied write was replayed and no further 429 occurred. Nested rate-limit detection was added to the policy and regression-tested. The formatter registration and application were separately guarded against existing scripts.

Two requests failed schema validation (an SEO wrapper and one QA navigation call); each was counted and corrected after establishing the result. They made no target changes. There were no unresolved partial batches, unknown write outcomes or unrelated conflicts.

The rate-policy tests cover a full rolling budget, minimum gap, oversized batch, Retry-After, fallback backoff, stop threshold, partial/unknown write reconciliation and nested MCP 429 detection. Existing editorial, handoff and animation tests are retained.

## Publication boundary

Before and after reads show site `lastPublished` **2025-11-06T16:08:46.501Z** and both custom domains **2025-11-12T13:37:52.643Z** unchanged. See [before](before-site.json) and [after](after-site.json). This transfer updated the Designer project only. Sandbox publication/acceptance records refer to a different site.

The evidence manifest records file sizes and SHA-256 values. Do not restore the backup, replay writes, merge the PR chain or publish as part of reviewing this report.
