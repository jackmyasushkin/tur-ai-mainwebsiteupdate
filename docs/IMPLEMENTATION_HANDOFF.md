# START HERE: implement the prepared Tur.ai homepage

**Edition:** `enterprise-orchestration-handoff-v2`  
**Repository:** `jackmyasushkin/tur-ai-mainwebsiteupdate`  
**Branch:** `content/home-operational-plane-2026-10-13`  
**PR:** https://github.com/jackmyasushkin/tur-ai-mainwebsiteupdate/pull/1

The content-preparation task is complete. This document is the execution brief for the next agent. Do not restart discovery, rewrite the positioning or use the initial-export files on `main` as the new copy. Pin the current prepared commit before working and record it in your implementation report. An open PR does not mean the values exist on `main` or in Webflow.

**No Webflow read/write or browser QA has been performed for this edition.** Apply only when the owner explicitly assigns implementation. That assignment permits sandbox work within this brief; it does not permit publishing or changing other pages.

## 1. The content that must survive implementation

**H1 (exact):** Enterprise Process Orchestration Platform

**Subtitle (exact):** Run regulated processes across existing systems. Customers trust us to help them work faster today and change faster tomorrow.

**CTA:** Book a Demo, retaining its existing action.

Primary readers: Head of AI and Head of Transformation. The page moves from recognizable category and customer value, to scoped proof, the operational plane above systems of record, governed execution and task-matched model economics, then a measured pilot and expansion path.

Keep **62%, 82%, 83%, 3x** attached to their existing prepared captions and the metrics FAQ. 83% describes **annual token spend**, not licenses, token count or full TCO. 62% is process runtime, not implementation time-to-value. 3x delivery speed is distinct from annual process capacity. Do not swap anonymous banking results into named client cards or invent competitor claims.

## 2. Read this package in order

1. `content/home/decisions.md` and `business-brief.md`: settled words, precedence and persona context.
2. `content/home/rewrite.json`: authoritative 228 decisions and exact replacement values.
3. `content/home/apply-plan.json`: machine-readable execution plan, edition and source hashes.
4. `baseline/home/2026-10-12/inventory.json`: full target bindings. Join `items[].id` to `records[].id`; use the source record's field type, component IDs, nested component chain and inline structure. Do not guess a selector from the visible text.
5. `content/home/implementation-overrides.json`: the only legacy-budget exception, HOME-003.
6. `content/home/review-questions.md`, `evidence.md`, `validation.md` and `preparation-report.json`: holds, evidence boundaries, actual checks and warnings.
7. `docs/WORKFLOW.md` and the frozen baseline brief: layout/interaction acceptance requirements.

`proposal.md` is the readable copy review, generated from the exact set. Its Markdown tables do not replace source rich-text structure. `local-precheck.json` is an older v1 record; do not use it as the current pass report.

Before any write, run:

```sh
python3 tools/check.py --complete
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/verify_home_handoff.py
```

All must pass. The checker must disclose `H1-CATEGORY-2026-10-13`; a silent bypass or edited source budget is not a pass. Original source-manifest integrity must also pass. Do not run historical one-time preparation scripts from Git history.

## 3. Target lock

| Property | Required value |
|---|---|
| Webflow site | Copy of Tur.ai |
| Site ID | `6899ffe04a85e00f2b8cf5ab` |
| Page | Home, English |
| Page ID | `6899ffe04a85e00f2b8cf5ac` |
| Baseline | 12 October 2026 Designer snapshot |
| Designer | https://tur-ai-9ad25f67865b7ebb8e05b7460738fd68.design.webflow.com/?workflow=canvas |

Confirm identifiers through the available Webflow tools, not just the tab title. Do not apply to the public site, Home UA, case-detail pages, legal pages, CMS or a different sandbox. This brief does not authorize a publish call to any domain.

## 4. Live preflight and rollback record

Read the complete current page and involved component instances before mutation. Resolve bindings against the inventory. Inspect existing inline spans and paragraph breaks, link destinations, input names/IDs/values, component inheritance and relevant visibility states.

For each row, classify current live state:

- **Matches frozen original:** eligible for its specified action.
- **Already matches this edition exactly:** log as already applied; do not write again.
- **Matches the prior prepared edition:** do not assume it is untouched baseline. Record the actual before value and verify target identity/structure. Treat as an update to an existing draft only under the assigned implementation scope.
- **Any other text, structure or missing/ambiguous binding:** mark conflict and do not overwrite that field or its dependent rich-text group. Report the conflict; unrelated safe fields may proceed.

Save the actual pre-write values, raw rich text/attributes and screenshots in a new dated `implementation/` run directory. Do not alter the frozen baseline. This live readset is the rollback source; it may differ from the old baseline. Never include lead submissions, credentials or tokens in the record.

## 5. Mutation rules

Only `action=rewrite` is a planned write. `keep` and `hold` mean NO WRITE. A hold is not permission to hide, remove, activate or approve the old element. There are 104 planned rewrites and 124 no-write decisions (88 keep, 36 hold); the exact plan/checker is the source of truth if a later edition changes these counts.

Use the right operation for the source field: string node, component property, attribute or SEO metadata. Preserve IDs, links, DOM, classes, fonts, dimensions, spacing, animations, visibility and handlers. Use instance overrides where possible. If a component edit would propagate beyond Home and cannot be isolated, stop that group and report it rather than silently changing other pages.

For rich text, write every supplied segment into its corresponding source node; preserve node order, outer whitespace, blue highlights, inline elements and paragraph/line-break structure. Do not set a parent's flat textContent when this would destroy its children. Do not paste Markdown `<br>` from proposal.md. The original inline tree remains authoritative for the breaks in FAQ answers.

Keep desktop/mobile pairs synchronized: 089/098, 091/101, 093/104, 095/100, 096/103, 097/106. Check the separate 069/070 toggle nodes and repeated case summaries too. Similar text is not permission for a global replace.

Keep navigation, demo and contact actions distinct. Preserve form `name`, `id`, `data-name`, action, required flags, option values and honeypots. No test lead submission. Test states without sending personal data or triggering external workflows.

SEO: update HOME-227 and HOME-228 only. Open Graph inherits these values in the baseline; verify that this inheritance still holds. Do not create conflicting separate OG metadata.

## 6. Special case: the approved H1

The exact heading is **41/50 characters** and the subtitle **126/128**. H1's old per-segment budgets were tied to the rejected wording. The permitted replacement is:

| Source element ID | Old text | Exact new raw text | Old max / new visible length |
|---|---|---|---|
| `370cbcb9-ca44-e3fa-3af5-ffcc49e12e2f` | `We ` | `Enterprise ` | 2 / 10 |
| `2b066328-9a94-c967-16e0-a7eb5632acf0` | `Automate ` | `Process ` | 8 / 7 |
| `27e5d944-a647-2835-857a-f6cce18f23ad` | `Enterprise Customer Operations with ` | `Orchestration ` | 35 / 13 |
| `d289d6ed-e2cb-f2c5-ed95-3ce79ffdebe2` | `AI` | `Platform` | 2 / 8 |

All four belong to component/page `6899ffe04a85e00f2b8cf5ac`. The existing highlighted second node now highlights **Process**. The first three strings end with one regular space; the fourth has no outer space. No new node or styling is needed by the planned edit.

Do not change original max_chars values, insert invisible characters, split Enterprise across nodes, append AI, reduce the font or drop words. The exact exception has its own validator; it is not permission for other over-budget copy. If wrapping fails, capture the actual viewport and ask for a layout/content decision. Do not label the exception visually approved before rendering.

## 7. Known holds and interaction risks

- Hidden procurement/logo conflict: HOME-053, 054, 055 and 194 are no-write. Do not activate this hidden variant or assume which logo is correct.
- Testimonial and attribution: HOME-177, 178, 179 and 207 are no-write. The quote has DOM-only source bindings; do not rewrite it or infer a current role from a historical quote.
- Hidden test/UA forms: HOME-160 through 176 and HOME-216 through 226 remain untouched.
- Noordwest service-desk link currently points to `#`. Preserve the URL; log it as an existing unresolved defect. Do not invent a destination or disable a button without approval.
- The linked procurement case has an older out-of-scope numerical wording issue recorded in review-questions.md. Do not silently edit that page as part of Home.
- The four old survey percentages are now the ordinals **01. / 02. / 03. / 04.**, not statistics. Update each number and suffix together. Check both sides of the interaction; do not leave a percent sign on an ordinal.
- Fourth main metric is **3x**, not 3%. The prepared suffix is the multiplication character in HOME-022. Verify number and suffix as a group.
- Existing icons, logos, client names and media remain unchanged. An AI-focused video or old screenshot may need separate owner review; do not claim that a text update refreshed media.

These do not block unrelated safe sandbox text edits. They must remain visible in the report and be reviewed before any later publication decision.

## 8. Apply in small, reversible groups

Recommended sequence: hero; headline metrics and their captions/FAQ boundary; orchestration steps and architecture toggle; existing case summaries; pilot/launch/scale pairs; FAQs; forms/shared components; SEO. After each group, re-read the actual values and compare with rewrite.json. Avoid bulk blind replacement.

Log every field as applied, already-correct, no-write, conflict or failed. If any required member of a metric/rich-text/duplicate group fails, do not leave the group misleading; roll back that group's applied values using the live readset, or stop with explicit owner-visible status.

Rollback restores actual captured before values, not guessed baseline text. Never roll back unrelated concurrent changes.

## 9. Visual and functional acceptance

Compare before/after at **1383, 820, 667, 393, 320 px**. Also inspect **1440** and breakpoint edges **991/992, 767/768, 479/480**. Extra-width before captures must be taken during preflight; the baseline does not contain all of them.

Check H1 category readability, subtitle, CTA one-line behavior, metric captions, every case slide, both toggle states, all three desktop tabs and mobile cards, every expanded FAQ, demo and call modals, contact form, and non-submitting success/error/wait states. Test navigation/anchors without submitting leads.

Acceptance requires no new clipping, overlap, unintended overflow, illegible wrapping, missing spans, mixed old/new metric units, accidental hidden content activation, or propagated changes on other pages. Shorter copy and longer words still require review even if counts pass. Do not shrink fonts or hide overflow to conceal a problem. Record any pre-existing defects separately from new regressions.

Screenshots and read-back evidence are required. Identify whether the implementer or another reviewer performed the visual check; do not invent independent QA.

## 10. Implementation definition of done

The next agent is finished when:

1. All planned rewrite fields are applied and read back exactly, or explicitly blocked with reasons; a blocked set is not called fully complete.
2. Every keep/hold remains unchanged and shared-component impact is checked.
3. Required views and interactive states are tested and documented, including H1 and numeric suffix changes.
4. The run folder contains pinned source commit/hashes, live before values, per-ID after values/status, before/after screenshots, conflicts/holds, rollback record and a concise report.
5. STATUS.md distinguishes applied, visually accepted, blocked and published. **Published remains false.**

Use an implementation branch/PR for the run record; do not force push or automatically merge PR #1. No publish step is part of this task.

Suggested report schema:

```json
{
  "edition": "enterprise-orchestration-handoff-v2",
  "source_commit": "record actual pinned SHA",
  "site_id": "6899ffe04a85e00f2b8cf5ab",
  "page_id": "6899ffe04a85e00f2b8cf5ac",
  "fields": [{"id": "HOME-003", "status": "applied|already-correct|no-write|conflict|failed", "before": "actual value", "after": "read-back value"}],
  "visual_checks": [],
  "unresolved_issues": [],
  "published": false
}
```

## Kickoff prompt for the next agent

> Implement edition `enterprise-orchestration-handoff-v2` from PR #1 in the Copy of Tur.ai English Home sandbox only. Start with docs/IMPLEMENTATION_HANDOFF.md on branch content/home-operational-plane-2026-10-13 and pin its prepared commit. Use rewrite.json plus the baseline bindings, respect the exact H1 exception and all holds, perform live preflight, scoped writes, read-back and visual checks, then record the result in GitHub. Do not invent copy, change layout/styles/links/forms or publish the site. Report conflicts instead of overwriting them.
