# Production transfer preflight evidence

Read-only comparison of the original Tur.ai English Home and the accepted Copy of Tur.ai Home on 13 October 2026. See [the transfer strategy](../../docs/PRODUCTION_TRANSFER_STRATEGY.md).

`target-plan.json` is a planning candidate with exact target bindings and before guards. It does not execute writes. `home-mapping-audit.json` classifies all 228 source decisions, including absent and unverified targets. `mapping-summary.json` separates MCP draft evidence from published HTML corroboration.

Home and definition trees are sanitized MCP reads. Make webhook URLs are redacted; their replacement length is not a hash or an equality proof. No form submissions were read or sent. Freeform code is represented by inspection summaries and hashes, to preserve comparison evidence without copying service keys. Current production bytes must be re-read before any future mutation.

Style catalogs contain identity metadata only. Published CSS snapshots and `home-css-audit.json` support the in-place strategy; they do not establish draft computed styles, cascade or rendered acceptance. `shared-component-pages.json` plus the Home tree and component counts establish the six affected English pages.

`mcp-read-log.json` records serialized reads, pauses and two corrected style-query validation failures. The page-branch read returned the final `403 not_enterprise_plan_site`; no branch was created or retry attempted. There were no mutations, publish calls or 429 responses.

Reproduce the core mapping from the repository root:

```sh
python3 tools/compare_production_home.py --repo . \
  --production migration/2026-10-13-production-preflight/target-home.json \
  --production migration/2026-10-13-production-preflight/target-definitions.json \
  --production migration/2026-10-13-production-preflight/target-components.json \
  --production migration/2026-10-13-production-preflight/pages-and-branching.json \
  --sandbox migration/2026-10-13-production-preflight/source-home.json \
  --sandbox migration/2026-10-13-production-preflight/source-definitions.json \
  --sandbox migration/2026-10-13-production-preflight/source-components.json \
  --sandbox migration/2026-10-13-production-preflight/pages-and-branching.json \
  --out /tmp/turai-production-mapping.json
```

The hash manifest covers this dated evidence directory. It does not supersede the immutable baseline or earlier implementation/acceptance manifests.
