# Website Director Templates

## Purpose

Own current and review-only template artifacts consumed by the isolated
Website Director prototype and its framework validator.

## Ownership

site-profile.json is the current V2.15-compatible site-profile fixture with
the V2.15 framework version recorded explicitly. content-model.md and
content-model.json own the Capability #8 semantic content-model contract;
cms-decision.md owns the vendor-neutral CMS necessity and provider decision
record. inspiration-board.md and
research-synthesis.md own the reference-evidence fields consumed by the
bounded V2.11.1 Design Inspiration MCP adapter. evidence-ledger.md and
evidence-ledger.json own the Capability 7 claim, source, rights, attribution,
asset, and research-reference recording templates. framework-validation-review.md
is the human review record template. localization-plan.md,
localization-manifest.json, and locale-registry.json own the provider-neutral
Capability #9 localization and internationalization planning artifacts.
`inspiration-board.md` and `inspiration-source-registry.json` own the
owner-selectable, reference-only inspiration intake and source registry used
by cinematic and visual research work.
`owner-intent.json` defines the neutral machine-readable owner constraint
shape. `alpha-starts-now-owner-intent.json` is the current Alpha Starts Now
owner-contract artifact: navy blue is primary, yellow is accent, historical
orange-family directions are non-authoritative, and explicit cinematic intent
requires Level 3 evidence. It does not create a site state or sixth lock.

## Local Contracts

- The current profile must match `schemas/site-profile.schema.json` and the
  canonical framework version.
- It must contain exactly the five approved owner locks.
- Framework-validation status, reports, and release certification do not belong
  inside the site profile.
- MCP-discovered references remain `REFERENCE_ONLY`; template fields must not
  turn them into production assets, implementation tokens, or a new state
  object.
- Evidence-ledger records are the cross-cutting provenance source of truth;
  asset-provenance.md and asset-manifest.json consume it without replacing
  Asset Director ownership or creating a sixth lock.
- Production claims and assets require traceable evidence, permitted-use
  records, attribution where required, and SHA-256 identity where applicable.
  Missing or unresolved evidence remains blocked. Hashes do not establish
  ownership or legal clearance.
- Content Operations templates define entities, fields, editorial lifecycle,
  editable surfaces, portability, migration, and provider decisions without
  duplicating V2.5 handoff operations or creating a sixth lock.
- Localization templates define evidence-based requirement assessment, BCP
  47-style locale identity, route and fallback policy, translation review and
  freshness, formatting, RTL, typography and font provenance, localized SEO,
  content-model integration, accessibility, analytics, assets, browser QA,
  launch, and handoff inputs. They do not provision providers, publish, deploy,
  certify legal translation, or create a sixth lock.
- Application architecture templates define conditional, behavior-based
  classification, minimal module activation, provider-neutral auth/commerce
  contracts, verification evidence, exceptions, and the single
  `application.complete` readiness flag. They never activate every module,
  contain credentials, perform live payments, deploy, or create a sixth lock.
- Inspiration registry and board records are reference-only by default. An
  owner-selected source must carry relevance, adaptation, and non-copy fields;
  source reuse additionally requires verified license, provenance, stack, and
  design-system evidence.
- Browser QA templates may declare `runtime_observations` requirements for
  real-browser form and mobile-navigation evidence. Required observations are
  fail-closed and local form exercise is limited to safely intercepted
  same-origin requests; templates do not authorize production side effects.
- Historical templates may be referenced by compatibility records but must not
  be silently regenerated or promoted to current.
- Owner-intent records must retain requirement class, source, currentness,
  scope, and authority. Reference signals require a source-to-principle-to-
  client-interpretation-to-implementation trace; references cannot redefine a
  current brand contract. Exact brand values are not to be invented when the
  owner has approved only semantic roles.

## Work Guidance

Keep templates dependency-free, explicit, and neutral. Add a new template only
when its manifest and registry ownership are clear.

## Verification

Run `python -m framework_validation --run-suites` and inspect schema, reference,
content-operations, localization, application, provenance, and five-lock findings. The
synthetic Capability 7 A-V suite plus W-AK fail-closed regression edges,
Capability 8 A-V suite, Capability 9 A-AF suite, and Capability 10 A-AV suite
must remain isolated from
projects/ and external systems.

## Child DOX Index

- None.
