# Localization and Internationalization Plan

<!-- FRAMEWORK_VERSION: 2.14.0 -->

This template is the provider-neutral Capability 9 planning artifact for Website Director V2.14. It records engineering, content architecture, adaptation, review, and verification decisions. It does not provision a translation provider, publish content, deploy a site, or certify legal compliance.

## Project Control

- Framework version: `2.14.0`
- Planned phase: `6.35`, after Content Operations and CMS Architecture (`6.25`) and before Conversion and Analytics (`6.5`)
- Readiness gate: `[LOCALIZATION_READY]`
- State authority: `localization.complete`
- Owner locks: `design_direction_locked`, `information_architecture_locked`, `content_structure_locked`, `design_system_locked`, `motion_direction_locked`
- Owner lock count: exactly five. Localization does not create a sixth lock.
- Protocol: [LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md](../LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md)
- Manifest: [localization-manifest.json](./localization-manifest.json)
- Locale registry: [locale-registry.json](./locale-registry.json)

## Requirement Assessment

Record the evidence that makes localization `NOT_REQUIRED`, `PLANNING`, `READY`, `BLOCKED`, `IMPLEMENTED`, `VERIFIED`, or `EXCEPTION_APPLIED`. Do not infer a requirement from IP address, browser language, ethnicity, company name, or geographic stereotype. An English-only site may remain `required: false` without localization bloat.

- Required: `false`
- Assessment status: `NOT_REQUIRED`
- Recorded signals: `NONE`
- Blocked reason: `null`
- Exception: `applied: false`, `reason: null`

## Source Locale

Record exactly one authoritative source locale when localization is required. The source locale is the origin for content identity, translation freshness, claim provenance, and review comparisons.

## Default Locale

Record exactly one default locale. The default locale is distinct from the source locale when the product requires that distinction. The URL policy must explicitly state `ROOT` or `PREFIX` for path-prefix routing.

## Supported Locales

Use BCP 47-style identifiers such as `en`, `en-US`, `es-MX`, `zh-Hant-TW`, and `ar`. Keep language, script, and region distinct. Each registry record declares direction, route, coverage, owner, status, SEO participation, and fallback behavior.

## Route Strategy

Select one of `PATH_PREFIX`, `SUBDOMAIN`, `SEPARATE_DOMAIN`, or `NO_PUBLIC_LOCALE_ROUTING`. Record route collision checks, reserved paths, default URL policy, redirects, canonical behavior, sitemap behavior, and route ownership.

## Locale Switcher

Provide an accessible locale switcher when multiple public locales exist. Use text labels and expose the current locale to keyboard and assistive technology users. Flags may supplement a label but cannot be the sole language identifier. Preserve the current content intent when a translated route exists and state fallback behavior when it does not.

## Content Coverage

Record `FULL`, `PARTIAL`, or `NOT_AVAILABLE` coverage for every enabled locale and content surface. Partial coverage must identify the exact fallback route and must not silently mix source and translated content.

## Fallback Policy

Choose `NO_FALLBACK`, `SOURCE_LOCALE_FALLBACK`, `PARENT_LANGUAGE_FALLBACK`, or `CONTENT_TYPE_SPECIFIC`. Store an acyclic fallback graph. Explain whether titles, body content, UI strings, legal content, metadata, and forms have different fallback rules.

## Content/CMS Strategy

Consume the V2.13 content model and portability contract. Choose `FIELD_LEVEL_LOCALIZATION`, `DOCUMENT_PER_LOCALE`, or `HYBRID`. Content Operations owns what fields and content types exist. Localization owns which fields vary by locale and how their lifecycle is reviewed. Do not create a second CMS or content authority.

## Localizable Fields

For every content type, classify fields as localizable or non-localizable. Localizable fields may include body copy, titles, descriptions, labels, alt text, metadata, and structured editorial text. Non-localizable fields may include stable IDs, hashes, evidence references, timestamps, technical dimensions, and machine identifiers unless an explicit contract says otherwise.

## Translation Workflow

Use the status sequence `SOURCE`, `NOT_TRANSLATED`, `MACHINE_DRAFT`, `HUMAN_REVIEW_REQUIRED`, `REVIEWED`, `APPROVED`, `STALE`, and `PUBLISHED`. Machine translation is draft material only. Record source identity, target locale, method, owner, reviewer, evidence reference, and source version for every translated record.

## Review Workflow

A human or otherwise explicitly authorized reviewer must approve translated content before production publication. Legal, privacy, consent, terms, disclaimer, and regulatory content requires legal review where applicable. Translation review is not legal approval.

## Translation Freshness

A source version change or source timestamp newer than the translation marks the translation `STALE`. Stale content cannot be treated as current or published until it is re-reviewed against the new source.

## UI Strings

Use stable semantic message IDs such as `nav.primary_label` and `form.submit_label`. Do not derive IDs from English text, route names, or translation status. Keep labels, errors, aria text, empty states, and validation messages in the same message catalog.

## Formatting

Use locale-aware runtime formatting for dates, times, numbers, currencies, units, and plural categories. Record explicit currency and unit policy. Formatting must be deterministic, testable, and independent of the visitor's inferred location.

## Dates/Times

Store timestamps in an unambiguous machine representation and format them for the active locale and timezone policy. Do not ship fixed masks such as `MM/DD/YYYY` as a universal display contract.

## Numbers/Currency

Use locale-aware number separators and explicit currency codes. Language does not determine currency. Record conversion, rounding, tax, and display precision rules where money is shown.

## Units

Record whether values remain canonical, are converted by locale, or require user selection. Do not silently convert safety, technical, or regulated values without an explicit precision and rounding policy.

## RTL

Declare `dir="rtl"` for RTL locales and test reading order, focus order, overflow, forms, tables, icons, and mixed-direction text. Record an intentional icon mirroring policy. Brand marks and logos must not be mechanically mirrored.

## Typography

Verify script and glyph coverage for every enabled locale, including CJK and Arabic-derived scripts when applicable. Record webfont licensing and redistribution evidence through the V2.12 provenance authority. Plan for at least 30 percent and 50 percent expansion cases.

## Assets

Classify assets as locale-neutral or locale-specific. Localized images, captions, alt text, media metadata, and filenames need the same provenance, rights, and review treatment as source assets. Research references such as Dribbble, Mobbin, Landbook, or screenshots are not production media.

## SEO/Hreflang

For indexable localized pages, generate intentional self and reciprocal `hreflang` references plus `x-default` where appropriate. Keep localized self-canonicals, localized metadata, route-aware sitemaps, structured data, Open Graph locale data, and alternate asset references consistent.

## Accessibility

Localize document language, direction, visible labels, accessible names, descriptions, validation errors, status messages, and the locale switcher. Do not make an untranslated or flag-only control the only way to change language.

## Forms

Localize labels, hints, errors, consent text, confirmation states, and date/number input guidance. Preserve field identity and validation semantics across locales. Do not collect extra personal data merely to support localization.

## Analytics

Reuse the existing event names and add locale as a parameter where measurement requires it. Do not create a separate event taxonomy for every language. Respect [CONVERSION-ANALYTICS-PROTOCOL.md](../CONVERSION-ANALYTICS-PROTOCOL.md) and [SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md](../SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md).

## Provenance

Preserve source claims, evidence references, asset hashes, license records, and review history across localized variants. Translation cannot strengthen a source claim. A translated legal statement is not automatically legally approved. Use [EVIDENCE-PROVENANCE-PROTOCOL.md](../EVIDENCE-PROVENANCE-PROTOCOL.md) as the provenance authority.

## QA

Extend the existing [BROWSER-REGRESSION-QA-PROTOCOL.md](../BROWSER-REGRESSION-QA-PROTOCOL.md) runner with locale, pseudo-localization, RTL, route, formatting, and fallback assertions. Do not create a second browser runner. Simulation is not production verification.

## Launch

Launch Operations owns production verification and release identity. A localization plan or local browser run does not authorize deployment or establish production verification. No provider account, production credential, live analytics property, Search Console property, or live site is changed by this artifact.

## Handoff

Transfer locale registry, field policy, translation statuses, review responsibilities, freshness process, asset ownership, SEO rules, and backup/restore expectations through the existing V2.5 Client CMS Handoff authority. Do not create a parallel handoff system.

## Known Gaps/Exceptions

Record unresolved script coverage, legal review, provider selection, partial locale coverage, CMS portability, production evidence, and owner decisions here. `UNKNOWN`, `UNASSESSED`, and `BLOCKED` remain explicit states. An exception requires a reason and never silently promotes an unverified integration.
