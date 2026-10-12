# Home rewrite — content review

**Proposed edition · 13 October 2026 · no Webflow changes or publication**

**228 decisions: 104 rewrite · 88 keep · 36 hold.** Exact replacements, original values and all rich-text segments live in [rewrite.json](rewrite.json). Evidence lives in [evidence.md](evidence.md).

## The page in one view

> **We Speed Up Regulated Processes with Governed AI**
>
> An operational plane above your systems of record. Run processes across systems, AI and people, with control and traceability.

| Work faster | Change faster / scale efficiently |
|---|---|
| **62% shorter process cycles** — bank onboarding, 16 to 6 days | **83% lower LLM costs** — annual token spend, EUR 1.8M to EUR 300K |
| **82% lower staffing needs** — the same process, 34 to 6 FTE | **3x faster process delivery** — a European-bank transformation result |

**Execution mechanism:** task-matched models, shared context, governed system actions, bounded retries, required human decisions and recorded outcomes.

**Entry route:** one measured pilot, a production rollout assessed against a baseline, then reusable expansion. No new landing-page structure is required.

The cost correction is applied throughout: token spend, not licenses, not token count and not full TCO. Case captions and an existing FAQ supply the boundaries without adding a disclaimer component.

## Exact proposed replacements by section

Character counts below use normalized Unicode code points, including spaces. They are editorial limits, not a claim about rendered line wraps. Unchanged functional labels and protected fields are summarized rather than repeated.

### 1. Hero and navigation

Keep **Book a Demo** and **Contact Us** and their existing actions. The hero puts the business outcome first, followed by the architectural role.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-003 | We Speed Up Regulated Processes with Governed AI | 48 / 50 |
| HOME-004 | An operational plane above your systems of record. Run processes across systems, AI and people, with control and traceability. | 126 / 128 |
| HOME-006 | See one process, its controls and the business case for change. | 63 / 70 |

### 2. Work faster / change faster: selected results

Four case-specific proof points. The first two refer to the same onboarding case; token economics is a separate engagement. Runtime, required capacity, annual token spend and delivery speed remain distinct.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-007 | Work and change faster. Results from banking engagements. | 57 / 69 |
| HOME-008 | Shorter process cycles | 22 / 22 |
| HOME-009 | 62 | 2 / 2 |
| HOME-011 | One European bank: customer onboarding fell from 16 days to 6. | 62 / 84 |
| HOME-012 | Lower staffing needs | 20 / 23 |
| HOME-013 | 82 | 2 / 2 |
| HOME-015 | The same bank's onboarding staffing requirement fell from 34 FTE to 6. | 70 / 103 |
| HOME-016 | Lower LLM costs | 15 / 15 |
| HOME-017 | 83 | 2 / 2 |
| HOME-019 | Banking case: annual token spend fell from €1.8M to €300K. | 58 / 73 |
| HOME-020 | Faster process delivery | 23 / 24 |
| HOME-021 | 3 | 1 / 1 |
| HOME-022 | × | 1 / 1 |
| HOME-023 | A European bank: 3x faster process delivery; 2-3 to 12+ processes automated per year. | 85 / 92 |

### 3. Founder statement

A proposed new statement for the founder's approval. Name, role, photograph and attribution bindings stay unchanged.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-024 | We built Tur.ai so businesses can work and change faster without replacing their core. | 86 / 93 |

### 4. How execution works

Five existing steps now explain intake, task-matched models, governed execution, human decisions and evidence. Step counts and icons are unchanged.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-027 | Coordinate Every Step, From Incoming Work to a Controlled Outcome. | 66 / 79 |
| HOME-029 | Work intake | 11 / 15 |
| HOME-030 | Bring requests, documents and system data into one process with shared context. | 79 / 85 |
| HOME-032 | Model choice | 12 / 13 |
| HOME-033 | Use models matched to each task, rather than one general-purpose model for every step. Keep AI costs tied to the work. | 118 / 131 |
| HOME-035 | Controlled execution | 20 / 26 |
| HOME-036 | Coordinate AI, system actions and approvals under your process rules. Carry context and verification results forward, with bounded retries and clear ownership. | 159 / 166 |
| HOME-038 | Human decisions | 15 / 16 |
| HOME-039 | Route exceptions to the right person to decide. | 47 / 48 |
| HOME-041 | Traceable outcomes | 18 / 20 |
| HOME-042 | Record actions and decisions for review and audit. | 50 / 52 |

### 5. Existing customer cases

Keep the existing clients, logos and destinations. Hidden variants remain hidden. The hidden procurement variant is held because its client attribution conflicts; see review-questions.md.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-043 | Real operations powered by Tur.ai. | 34 / 36 |
| HOME-044 | Lead-to-quote automation | 24 / 24 |
| HOME-045 | 3x faster quotes | 16 / 24 |
| HOME-047 | Cashback campaign operations | 28 / 41 |
| HOME-048 | Heineken ran 12 nationwide campaigns with a small in-house team. | 64 / 74 |
| HOME-051 | Noordwest supported service enquiries through an ERP rollout with a small team. | 79 / 96 |
| HOME-056 | Lead-to-quote automation | 24 / 24 |
| HOME-057 | Radio Holland cut time-to-quote by 3x through coordinated requests, workflows and system updates. | 97 / 113 |
| HOME-059 | Cashback campaign operations | 28 / 41 |
| HOME-060 | Heineken ran 12 nationwide campaigns with a small in-house team. | 64 / 75 |
| HOME-063 | Noordwest supported service enquiries through an ERP rollout with a small team. | 79 / 96 |
| HOME-066 | Heineken cut vendor onboarding from months to weeks. | 52 / 68 |

**Hold / no write:** HOME-053, HOME-054, HOME-055.

### 6. Architecture and the cost mechanism

The old unsupported survey percentages become **01. / 02. / 03. / 04.** problem/solution pairs. These are ordinals, not statistics. The same toggle, nodes, spans and solution-card count remain.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-068 | Same systems. More control, faster work and lower AI costs. | 59 / 75 |
| HOME-069 | Click to see how<br>Tur.ai changes this | 36 / 41 |
| HOME-070 | Click to see how<br>Tur.ai changes this | 36 / 41 |
| HOME-071 | 01 | 2 / 2 |
| HOME-072 | . | 1 / 1 |
| HOME-073 | One model for every task | 24 / 47 |
| HOME-074 | 02 | 2 / 2 |
| HOME-075 | . | 1 / 1 |
| HOME-076 | People bridging systems and teams | 33 / 51 |
| HOME-077 | 03 | 2 / 2 |
| HOME-078 | . | 1 / 1 |
| HOME-079 | Process changes held up by core releases | 40 / 41 |
| HOME-080 | 04 | 2 / 2 |
| HOME-081 | . | 1 / 1 |
| HOME-082 | Retries that waste tokens and time | 34 / 39 |
| HOME-083 | AI models matched to each task | 30 / 37 |
| HOME-084 | One governed flow across systems and teams | 42 / 44 |
| HOME-085 | Change processes above existing systems | 39 / 40 |
| HOME-086 | Bounded retries, checks and human decisions | 43 / 48 |

### 7. Testimonial

The existing section heading is kept. The customer quotation and attribution are held unchanged; no new claim is put in the customer's mouth.

**Hold / no write:** HOME-177, HOME-178, HOME-179, HOME-207.

### 8. Pilot, launch and scale

Desktop tabs and mobile cards carry identical text within the tighter paired budgets. Dates, guaranteed ROI and universal delivery promises are not added.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-088 | One measured pilot before you scale across the business | 55 / 63 |
| HOME-089 | PILOT | 5 / 7 |
| HOME-091 | LAUNCH | 6 / 7 |
| HOME-093 | SCALE | 5 / 6 |
| HOME-095 | Choose a process with measurable value. Map its systems, decisions and controls, agree the baseline, and test a scoped workflow. Assess cycle time, staffing needs and AI costs before deciding whether to proceed. | 211 / 231 |
| HOME-096 | Move the agreed process into production with IT and process owners. Validate integrations, access, exceptions and required approvals. Compare results with the baseline and build the rollout case from measured outcomes, not assumed savings. | 239 / 264 |
| HOME-097 | Reuse the platform, integrations and controls for the next process. Train your teams to run and improve workflows, then track delivery speed, cost per accepted result and operating effort as volume and coverage grow. | 216 / 251 |
| HOME-098 | PILOT | 5 / 7 |
| HOME-100 | Choose a process with measurable value. Map its systems, decisions and controls, agree the baseline, and test a scoped workflow. Assess cycle time, staffing needs and AI costs before deciding whether to proceed. | 211 / 236 |
| HOME-101 | LAUNCH | 6 / 7 |
| HOME-103 | Move the agreed process into production with IT and process owners. Validate integrations, access, exceptions and required approvals. Compare results with the baseline and build the rollout case from measured outcomes, not assumed savings. | 239 / 264 |
| HOME-104 | SCALE | 5 / 6 |
| HOME-106 | Reuse the platform, integrations and controls for the next process. Train your teams to run and improve workflows, then track delivery speed, cost per accepted result and operating effort as volume and coverage grow. | 216 / 251 |

### 9. Deployment review

Replace unbounded integration assurances with a scoped review of the customer's environment. The Microsoft badge is not treated as a security certification.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-107 | Review deployment, integrations and data handling with our team, so the pilot fits your IT and security requirements. | 117 / 119 |

### 10. Buyer questions

Use the existing eight FAQ pairs to cover evaluation, system fit, data, token economics, measurement, differentiation, human controls and process fit. Keep the source paragraph structures.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-109 | How do we start and measure the first value? | 44 / 48 |
| HOME-110 | Start with one process and an agreed baseline for cycle time, staffing effort, AI usage and required controls. Define what a successful pilot must demonstrate.<br><br>We scope the workflow, integrations, data and approvals with your business and IT teams. Timing depends on that scope and access to your systems; we agree milestones before work starts.<br><br>Use measured results to decide whether to expand, adapt or stop. | 410 / 446 |
| HOME-111 | Can we change processes without replacing our existing systems? | 63 / 64 |
| HOME-112 | Tur.ai runs process logic, approvals and controls above your systems of record, so you can change operations without replacing your core. | 137 / 138 |
| HOME-113 | How do we fit Tur.ai into our security and data requirements? | 61 / 64 |
| HOME-114 | Agree the deployment design with your IT and security teams: system access, data flows and model use.<br><br>Define where data is processed, who can access it and what is retained.<br><br>Review the architecture and evidence against your requirements before production. Confirm data residency, retention and operational responsibilities. | 323 / 351 |
| HOME-115 | How does Tur.ai keep AI costs under control as we scale? | 56 / 63 |
| HOME-116 | Tur.ai uses models matched to each task rather than one model for everything. Governed execution limits unnecessary retries. In one banking engagement, annual token spend fell from €1.8M to €300K. This is AI usage spend, not total ownership cost. | 246 / 247 |
| HOME-117 | What do the results on this page actually measure? | 50 / 82 |
| HOME-118 | Selected banking results, not a forecast for every deployment: onboarding fell from 16 to 6 days, with staffing needs from 34 to 6 FTE. A separate engagement cut annual token spend from €1.8M to €300K. The 3x figure measures process-delivery speed, not onboarding time. FTE describes required capacity, not confirmed headcount cuts. | 332 / 378 |
| HOME-119 | How does Tur.ai differ from automating tasks or adding a chatbot? | 65 / 113 |
| HOME-120 | Tur.ai does more than generate answers or automate individual steps. It coordinates system actions, documents, rules, approvals and exceptions in one process. Your systems of record remain in place, while the operational plane governs how work moves from request to outcome. | 274 / 311 |
| HOME-121 | What happens when AI needs human judgment or an exception occurs? | 65 / 100 |
| HOME-122 | Your rules determine what can execute. Required approvals and exceptions go to the responsible person; the process continues when the required conditions are met. Recorded context, actions and decisions support review. Autonomy does not remove accountability. | 259 / 303 |
| HOME-123 | Which processes are a good fit for Tur.ai? | 42 / 42 |
| HOME-124 | Cross-system processes with documents, approvals and exceptions: customer onboarding, procurement and service operations. | 121 / 123 |

### 11. Contact, forms and footer

Functional field labels and CTA targets stay unchanged. A submitted form is a request, not a confirmed demo booking. Shared-component impact remains an implementation check.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-126 | Discuss one process, its controls and the business case for change. | 67 / 73 |
| HOME-133 | Your process and goals | 22 / 23 |
| HOME-135 | Thank you! We'll be in touch. | 29 / 38 |
| HOME-136 | Your message was not sent. Please try again. | 44 / 53 |
| HOME-141 | © 2026 Tur.ai. All rights reserved. | 35 / 35 |
| HOME-143 | See a relevant process, its controls and the results behind our claims. | 71 / 75 |
| HOME-149 | Thank you! We'll contact you about your demo. | 45 / 45 |
| HOME-150 | Your message was not sent. Please try again. | 44 / 53 |
| HOME-152 | Share your details to discuss one process. | 42 / 50 |
| HOME-158 | Thank you! We'll contact you about your call. | 45 / 45 |
| HOME-159 | Your message was not sent. Please try again. | 44 / 53 |
| HOME-209 | Which process needs to improve, and what would success look like? | 65 / 78 |

### 12. SEO

The page title and description use the same horizontal positioning. Open Graph inherits these values; no separate OG node is created.

| ID | Proposed copy | Characters / max |
|---|---|---:|
| HOME-227 | Tur.ai \| Governed Process Execution | 35 / 42 |
| HOME-228 | Run and change regulated processes above your existing systems. Tur.ai coordinates AI, people and controls. See results and book a demo. | 136 / 139 |

## Preserved content and behavior

All 228 IDs, their order, `original_text`, `max_chars`, and the source fields for all 51 rich-text segments are preserved. There are 19 rich-text fields; replacement segments retain their exact leading and trailing whitespace.

Hidden test and Ukrainian forms remain on hold. Existing non-empty alt descriptions are kept except attribution-sensitive assets explicitly held. Blank decorative alt values are not filled in. No link destinations, form field names, option values, styles, components, counts or event handlers are changed.

`hold` means do not write that field. It does not hide or remove the original content, and it does not certify the original claim.

## What still needs review

Approve the complete wording, including the founder statement. Resolve the existing case asset/link issues described in [review-questions.md](review-questions.md). Then apply only with explicit authorization and perform the Webflow visual/functional pass.

Implementation TTV and full scalable TCO remain separate evidence work. The current edition does not substitute process time or token expenditure under those labels.

## Checks

See [STATUS.md](STATUS.md) for exact local versus repository-CI results. A green character-limit check is not factual, visual or publication approval.
