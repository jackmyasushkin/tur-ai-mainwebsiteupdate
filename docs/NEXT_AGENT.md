# Next agent for transfer to the original Tur.ai project

Start with [PRODUCTION_TRANSFER_STRATEGY.md](PRODUCTION_TRANSFER_STRATEGY.md) and `migration/2026-10-13-production-preflight/target-plan.json`. The sandbox implementation and subsequent ordinal animation fix are already applied, published and owner-accepted. Do not replay their original sandbox apply plan.

The original Tur.ai target is Site `64e477696d41401ec48c50c6`, English Home `66368e29da23c5a1b0fe1396`. The live audit maps 102 existing replacement fields and four ordinal markers. HOME-123/124 need one new FAQ row; the owner approved including it in the strategy. Create target-owned IDs through native duplication of an existing FAQ row and verify accordion behavior.

The strategy is prepared; production writes and publication have not been performed or authorized by the planning task. After an explicit implementation instruction, reconcile fresh production state, finish native Placeholder/DOM-only reads, preserve production form actions, links, styles and all current code, then apply only the confirmed scoped changes. Publishing requires a separate instruction.

Keep the exact approved category **Enterprise Process Orchestration Platform** and `content/home/rewrite.json`. The [original sandbox handoff](IMPLEMENTATION_HANDOFF.md) supplies the historical source and content constraints; its source Site/Page IDs and preparation-stage status are not the production execution target. `main` may still contain the initial export until the PR chain is merged.
