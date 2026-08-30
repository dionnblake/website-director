# Localization and Internationalization Intelligence Protocol

<!-- FRAMEWORK_VERSION: 2.15.0 -->

**Protocol ID:** `LOCALIZATION_INTERNATIONALIZATION`<br>
**Capability:** #9<br>
**Version:** `2.14.0`<br>
**Planned phase:** `6.35`<br>
**Readiness gate:** `[LOCALIZATION_READY]`<br>
**State authority:** `localization.complete`<br>
**Canonical implementation:** [localization/validator.py](localization/validator.py)<br>
**Canonical plan:** [templates/localization-plan.md](templates/localization-plan.md)<br>
**Canonical manifest:** [templates/localization-manifest.json](templates/localization-manifest.json)<br>
**Canonical locale registry:** [templates/locale-registry.json](templates/locale-registry.json)

## 1. Purpose

This protocol governs Website Director's production-grade Localization and Internationalization Intelligence subsystem. It treats internationalization as the engineering and content architecture that makes a site locale-capable, localization as adaptation for language, script, culture, region, or market, and translation as one controlled activity within localization.

The subsystem produces inspectable plans, registries, manifests, review states, and deterministic validation evidence. It does not decide whether a translation is linguistically excellent, provision a translation provider, publish content, deploy a site, certify legal compliance, or replace an existing Website Director authority.

## 2. Authority and boundaries

The protocol is the canonical authority for localization and internationalization decisions. Its state is `localization.complete`. There is no parallel `i18n{}`, `l10n{}`, `translation{}`, `language_locked`, `translation_locked`, or `localization_locked` completion authority.

Adjacent authorities remain authoritative for their own concerns:

| Concern | Authority consumed by this protocol |
| --- | --- |
| Content types, fields, editorial lifecycle, provider-neutral CMS choice, portability | [CONTENT-OPERATIONS-CMS-PROTOCOL.md](CONTENT-OPERATIONS-CMS-PROTOCOL.md) |
| Search intent, SEO strategy, canonical policy, structured metadata | [SEO-INTELLIGENCE-PROTOCOL.md](SEO-INTELLIGENCE-PROTOCOL.md) and current SEO artifacts |
| Language attributes, labels, focus, errors, and accessible interaction | [ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md](ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md) |
| Data minimization, consent, regional safeguards, security headers, legal review boundary | [SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md](SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md) |
| Event names, parameters, attribution, and measurement privacy | [CONVERSION-ANALYTICS-PROTOCOL.md](CONVERSION-ANALYTICS-PROTOCOL.md) |
| Claims, evidence, asset rights, hashes, licenses, and provenance | [EVIDENCE-PROVENANCE-PROTOCOL.md](EVIDENCE-PROVENANCE-PROTOCOL.md) |
| Browser and runtime assertions | [BROWSER-REGRESSION-QA-PROTOCOL.md](BROWSER-REGRESSION-QA-PROTOCOL.md) |
| Release identity, deployment authorization, production verification, rollback | [LAUNCH-OPERATIONS-PROTOCOL.md](LAUNCH-OPERATIONS-PROTOCOL.md) |
| Long-term client ownership, backup and restore, training, and handoff | [CLIENT-CMS-HANDOFF-PROTOCOL.md](CLIENT-CMS-HANDOFF-PROTOCOL.md) |
| Five creative owner locks | [IMPLEMENTATION-CONTRACT.md](IMPLEMENTATION-CONTRACT.md) and the canonical lock registry |

Localization may add requirements, evidence, and implementation contracts. It may not silently mutate an approved information architecture, content structure, design system, copy, CTA wording, motion direction, measurement plan, legal disclosure, provenance claim, or deployment state.

## 3. Capability and lifecycle placement

Capability #9 is additive to the V2.13 framework. The planned lifecycle placement is:

1. `6.25` Content Operations and CMS Architecture
2. `6.35` Localization and Internationalization Intelligence
3. `6.5` Conversion and Analytics Intelligence
4. `6.75` Security, Privacy and Compliance Intelligence
5. `6.9` Accessibility Intelligence
6. `6.95` Evidence and Asset Provenance Intelligence

The phase precondition is `CONTENT_OPERATIONS_READY`. This protocol must be assessed after the content model and editorial ownership are understood and before measurement is finalized. The existing historical phase numbers are not renumbered.

`[LOCALIZATION_READY]` is a readiness gate, not an owner lock. The framework retains exactly five owner locks:

```text
design_direction_locked
information_architecture_locked
content_structure_locked
design_system_locked
motion_direction_locked
```

No localization, language, translation, regional, or internationalization lock may be added.

## 4. Requirement assessment

The requirement model records evidence, not stereotypes. A project may remain `localization.required = false` when its confirmed audience, market, content, and strategy are English-only. This avoids speculative locale routes, translation catalogs, font payloads, analytics dimensions, and CMS complexity.

The assessment may consider owner-confirmed target markets, audience languages, geographic expansion, contractual or regulatory requirements, existing translated content, SEO opportunity, regional product availability, local offices, multiple currencies, customer-support capability, content-maintenance capability, or an explicit multilingual strategy.

The assessment must ignore IP address, browser language, owner ethnicity, company name, and geographic stereotypes as proof of requirement. The deterministic helper [calculate_localization_requirement](localization/validator.py) returns `NOT_REQUIRED` or `PLANNING` with recorded signals and ignored inputs.

Conditional status values are:

| Status | Meaning |
| --- | --- |
| `NOT_REQUIRED` | Recorded evidence does not require multi-locale support. |
| `PLANNING` | Requirement exists and the architecture is being specified. |
| `READY` | Required artifacts and review inputs are complete enough for implementation. |
| `BLOCKED` | A required decision, evidence item, or control is missing. |
| `IMPLEMENTED` | The required local implementation exists, but production verification is separate. |
| `VERIFIED` | Required implementation evidence passed in the applicable environment. |
| `EXCEPTION_APPLIED` | Owner-recorded exception exists with a reason and known limits. |

`UNKNOWN`, `UNASSESSED`, and `BLOCKED` are not converted into a pass by wording changes. A missing provider is not a failure when the project does not require one. A missing required source locale, route, fallback rule, font license, or review record is a block.

## 5. Canonical state

The preferred state shape is additive and remains compatible with historical profiles:

```json
{
  "localization": {
    "required": false,
    "complete": false,
    "source_locale": null,
    "default_locale": null,
    "supported_locales": [],
    "route_strategy": null,
    "fallback_policy_defined": false,
    "seo_localization_ready": false,
    "content_localization_ready": false,
    "rtl_required": false,
    "translation_review_required": false,
    "implementation_verified": false,
    "production_verified": false,
    "blocked_reason": null,
    "exception": { "applied": false, "reason": null }
  }
}
```

`localization.complete` is the single readiness flag for this subsystem. It means the required plan and contract are complete. It does not mean a translation provider has been configured, an application build has passed browser QA, a production URL has been verified, or legal translation has been approved. `implementation_verified` and `production_verified` are separate evidence states and are never inferred from `complete`.

Historical site profiles may omit `localization{}`. V2.14 does not retrofit frozen pilots or silently migrate existing projects.

## 6. Locale identity and registry

Locale identifiers use BCP 47-style syntax. Examples include `en`, `en-US`, `es-MX`, `zh-Hant-TW`, and `ar`. Language, script, and region are distinct values. Underscore aliases such as `english_USA` are invalid.

The canonical registry is [templates/locale-registry.json](templates/locale-registry.json). Each locale record supports these fields:

```text
locale
language
region
script
enabled
default
source
route_prefix
direction
status
translation_owner
fallback_locale
seo_enabled
content_coverage
review_status
```

When localization is required, the registry must contain exactly one source locale and exactly one default locale. Both must resolve to enabled locale records. Every enabled locale declares direction, content coverage, route identity, fallback behavior, and review ownership. `FULL`, `PARTIAL`, and `NOT_AVAILABLE` coverage are explicit, not implied by a locale appearing in a list.

## 7. Route strategies and URL policy

Select exactly one public routing strategy when localized routes are exposed:

| Strategy | Contract |
| --- | --- |
| `PATH_PREFIX` | Locale is represented by a path prefix such as `/es` or `/es-mx`. |
| `SUBDOMAIN` | Locale is represented by a controlled host such as `es.example.test`. |
| `SEPARATE_DOMAIN` | Locale is represented by an explicitly owned domain. |
| `NO_PUBLIC_LOCALE_ROUTING` | Locale is not exposed as a public route; this is valid for English-only or non-public localization. |

For `PATH_PREFIX`, the default locale URL policy must be explicitly `ROOT` or `PREFIX`. `ROOT` reserves the root route for the default locale. `PREFIX` gives every locale a prefix. Prefixes must be collision-free, must not consume reserved application paths, and must have deterministic redirects for legacy URLs.

The route strategy does not authorize DNS, hosting, deployment, redirects on a live site, or domain purchases. Those remain owner-controlled external actions.

## 8. Locale switcher and user continuity

A public multi-locale site provides an accessible locale switcher with visible language names or equivalent text labels. Flags may supplement a label but cannot be the sole identifier. The current locale is programmatically exposed, keyboard navigation works, focus remains predictable, and the switcher does not reset the user to an unrelated page when a matching translation exists.

If a page is unavailable in the requested locale, the UI states the fallback or unavailable condition. It does not silently present mixed source and translated content as complete localization.

## 9. Fallback policy

Select one registry-level fallback policy:

* `NO_FALLBACK`
* `SOURCE_LOCALE_FALLBACK`
* `PARENT_LANGUAGE_FALLBACK`
* `CONTENT_TYPE_SPECIFIC`

The fallback graph must be acyclic. A locale may not fall back to itself. A target must exist in the registry. Content-type-specific fallback must separately describe body content, UI strings, forms, SEO metadata, legal content, alt text, and structured data. Fallback is a controlled behavior, not an excuse to publish stale or unreviewed translations.

## 10. Translation and review lifecycle

Translation is one part of localization. A record may use these statuses:

```text
SOURCE
NOT_TRANSLATED
MACHINE_DRAFT
HUMAN_REVIEW_REQUIRED
REVIEWED
APPROVED
STALE
PUBLISHED
```

`MACHINE_TRANSLATED` may be accepted as a compatibility alias for `MACHINE_DRAFT`, but machine output remains draft material. A record marked `PUBLISHED` or publicly visible must retain source locale, target locale, source text version, translation method, review status, and review ownership. Human or otherwise explicitly authorized review is required before production publication.

Legal, privacy, terms, consent, disclaimer, regulatory, and contractual content receives a separate legal-review flag where applicable. Machine translation cannot be marked legally approved merely because it has a general translation review. The subsystem never emits a legal-compliance certification.

## 11. Translation freshness and provenance

Every translated record retains a stable source content or field identity, source version or hash, target locale, method, timestamps, reviewer, and evidence reference. A source version mismatch or a source change newer than the translation marks the record `STALE`. A stale record cannot be treated as current or published.

Translated claims preserve the source evidence reference and claim strength. Translation may clarify language but may not strengthen a hedged claim into a guarantee, certainty, or unsupported promise. A material wording change is a content and provenance decision, not a translation shortcut.

The protocol consumes the V2.12 provenance ledger. It does not recreate hashes, erase prior evidence, or treat a translated claim as newly evidenced.

## 12. UI message architecture

UI strings use stable semantic message IDs, for example `nav.primary_label`, `form.submit_label`, and `errors.required_field`. IDs do not derive from English wording, route names, locale codes, or translation status. Labels, aria text, hints, empty states, validation errors, status messages, and confirmation messages share the same message architecture.

Count-bearing messages use standards-aware plural categories and safe named interpolation. They do not concatenate translated fragments around a number. Interpolation variables are explicit, type-checked, escaped for their output context, and available in every required locale.

## 13. Dates, times, numbers, currency, and units

Dates and times use locale-aware formatting over unambiguous stored timestamps and an explicit timezone policy. Fixed universal masks such as `MM/DD/YYYY` are defects. Numbers use locale-aware grouping and decimal rules. Currency is an explicit ISO-style code or a documented domain code; it is never inferred from language alone.

Units remain canonical, are converted under an explicit policy, or are selected by the user. Safety, technical, scientific, and regulated values require documented precision, rounding, and conversion rules. The manifest records date, time, number, currency, unit, pluralization, and interpolation strategies.

## 14. RTL, bidirectional text, and layout

RTL languages declare `direction: rtl` and expose `dir="rtl"` at the document or component boundary. Test reading order, focus order, navigation, forms, tables, mixed-direction text, numerals, punctuation, overflow, and error placement.

Use CSS logical properties such as `margin-inline`, `padding-inline`, `inset-inline`, `border-start-start-radius`, and logical text alignment where practical. Record exceptions that are intentionally physical. Do not mirror brand marks, logos, or identity-bearing artwork mechanically. Icons with directional meaning require a documented mirror policy.

## 15. Typography and expansion

Every enabled locale receives verified script and glyph coverage. This includes CJK, Arabic-derived scripts, Cyrillic, Hebrew, and mixed-script content when applicable. The font record includes script coverage, locale scope, web use, license status, redistribution status, and V2.12 provenance reference. An unresolved font license is a release block, not an implementation detail.

Design and browser QA exercise at least 30 percent and 50 percent text expansion. Pseudo-localization is deterministic test content, not a translation. It must exercise navigation, buttons, forms, headings, metadata, error messages, and constrained layouts.

## 16. Assets and media

Assets are classified as locale-neutral or locale-specific. Locale-specific captions, alt text, media metadata, filenames, overlays, and subtitles follow the translation and provenance lifecycle. Production media must have rights and evidence records. Dribbble, Mobbin, Landbook, Awwwards, Pinterest, and screenshots remain research references and cannot become localized production media without a separately verified asset record.

## 17. Content Operations and CMS integration

Localization consumes the V2.13 content model. Content Operations owns the content types, field definitions, editorial roles, publishing authority, slug contract, backup, restore, and portability. Localization owns which fields vary by locale, how variants map to source identity, translation statuses, review workflow, freshness, and fallback.

The supported CMS localization strategies are `FIELD_LEVEL_LOCALIZATION`, `DOCUMENT_PER_LOCALE`, and `HYBRID`. The chosen strategy must identify localizable and non-localizable fields. Stable IDs, evidence references, hashes, technical metadata, and timestamps are normally non-localizable. Body copy, titles, descriptions, labels, alt text, and SEO text are normally localizable, subject to the content model.

Slug policy is explicit. A localized slug may preserve a stable route key, use a translated slug with a durable redirect, or remain source-language by deliberate decision. Slug changes retain redirect evidence and do not create duplicate content records. Localized records remain portable through the existing CMS export and restore contract.

## 18. SEO and search discovery

Localized indexable pages have intentional self-referencing and reciprocal `hreflang` links. The graph includes the exact locale identifiers used by the page routes. `x-default` is included only when its destination and purpose are explicit. Localized pages use localized self-canonicals unless a documented canonical exception is approved.

Localized sitemaps, structured data, title and description fields, Open Graph locale fields, image metadata, and alternate assets remain consistent with the locale registry. SEO localization does not invent search demand, claims, or conversion data. It consumes the existing SEO strategy and content model.

## 19. Accessibility and forms

Localized pages expose the correct HTML language and direction. Visible text, accessible names, descriptions, labels, hints, validation errors, live-region messages, consent copy, and confirmation states are localized according to the fallback policy. Forms preserve field identity, validation meaning, and focus behavior across locales.

Date and number input guidance is locale-aware but does not reduce machine-readable data integrity. The locale switcher, localized form errors, and translated labels are included in accessibility review and browser evidence.

## 20. Security and privacy

Localization does not justify collecting IP-derived geography, inferred ethnicity, unnecessary profile data, or extra form fields. Locale selection may be explicit, session-scoped, or stored only under an approved privacy model. Consent text and regional disclosures are localizable content with provenance and legal-review requirements.

No API key, provider token, database credential, production connection string, translation account, or personal data is written to the repository, test fixtures, logs, screenshots, or generated artifacts. Provider adapters, if later authorized, are replaceable boundaries and remain disabled unless configured through an approved secure mechanism.

## 21. Analytics and measurement

Existing event names remain stable across locales. When measurement requires locale, add a normalized locale parameter to the existing event. Do not create separate event names such as `signup_es` or `signup_fr`. Analytics remains subject to measurement consent, minimization, retention, attribution, and production verification controls.

The localization plan does not create analytics properties, modify tag managers, install live pixels, transmit production analytics, or infer a baseline.

## 22. Browser and regression QA

Localization extends the existing browser QA runner. It does not create a second runner or a second evidence schema. Runtime checks include route integrity, document language, direction, locale switcher accessibility, fallback visibility, missing translations, formatting output, plural categories, interpolation safety, pseudo-localized overflow, RTL layout, font coverage, and localized SEO metadata.

The `simulation` engine can exercise deterministic negative controls but sets neither implementation nor production verification. A real browser run against a local build may set implementation evidence only. Production verification belongs to Launch Operations and requires a known release identity.

## 23. Launch and handoff

Launch Operations owns release readiness, deployment authorization, production verification, rollback, and post-launch monitoring. `[LOCALIZATION_READY]`, a local build, and a local browser run never authorize deployment.

The existing V2.5 handoff owns durable client operations. Localization transfers the locale registry, field policy, translation ownership, review responsibilities, stale process, asset responsibilities, SEO rules, route policy, backup and restore expectations, and known gaps into that handoff. It does not create a second CMS handoff authority.

## 24. Provider-neutral operation

No translation-memory system, machine-translation service, localization SaaS, provider account, or network API is required for framework certification. The subsystem validates local fixtures and contracts. A future provider integration must be an audited, replaceable adapter with explicit credentials, scope, rate, retention, review, and rollback controls. Provider installation and external account actions require owner authorization and are outside this protocol's local certification.

## 25. Artifacts and validation

The required artifacts are:

* [templates/localization-plan.md](templates/localization-plan.md)
* [templates/localization-manifest.json](templates/localization-manifest.json)
* [templates/locale-registry.json](templates/locale-registry.json)
* [schemas/localization-manifest.schema.json](schemas/localization-manifest.schema.json)
* [localization/validator.py](localization/validator.py)
* [tests/test_v2_14_localization.py](tests/test_v2_14_localization.py)
* [examples/LOCALIZATION-INTERNATIONALIZATION-INTEGRATION-VALIDATION.md](examples/LOCALIZATION-INTERNATIONALIZATION-INTEGRATION-VALIDATION.md)

The deterministic validator covers locale syntax and uniqueness, source/default identity, route collisions, fallback cycles, state authority, translation status and freshness, UI message safety, formatting, RTL, typography and license provenance, localized assets, Content Operations integration, accessibility, analytics, handoff, SEO reciprocity and canonical identity, and pseudo-localization overflow.

The release suite is registered in [schemas/test-suites.json](schemas/test-suites.json) as `v2_14_localization`. The suite uses temporary fixtures and the frozen-integrity guard. It must not mutate anything under `projects/`.

## 26. Required negative controls

The V2.14 suite must fail closed for at least:

* invalid locale identifiers, duplicate source/default declarations, fallback cycles, and route collisions;
* wrong `html lang`, missing hreflang reciprocity, and localized pages canonicalizing to the source route;
* machine drafts, unreviewed translations, stale translations, and untranslated legal content presented as approved;
* unsafe UI concatenation, missing plural categories, hard-coded date masks, and language-derived currency;
* RTL pages with LTR direction, mechanical brand-logo mirroring, pseudo-localized overflow, and missing script fonts;
* unresolved font licenses, strengthened claims, lost evidence references, research references used as production media;
* per-language analytics event names, duplicated CMS or handoff authority, missing localization state authority, and frozen fixture mutation.

## 27. Compatibility and stop boundary

V1 through V2.13 profiles remain valid when they omit the optional localization state. Single-language projects remain valid without locale routes or translation records. Frozen pilots are not retrofitted. The V2.14 state is additive and uses the same five owner locks.

Capability #10, Ecommerce, Authentication, and Application Modules, remains out of scope. This protocol must not be used to smuggle ecommerce catalog behavior, login flows, payments, or authenticated application data into a brochure-site localization assessment.
