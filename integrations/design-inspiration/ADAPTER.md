# DESIGN INSPIRATION MCP ADAPTER

> **Integration version:** 1.0.0
> **Website Director:** V2.11.1
> **Status:** Bounded research-only adapter
> **Rule:** RESEARCH PATTERNS, DO NOT CLONE COMPOSITIONS.

## 1. Purpose and authority boundary

This adapter makes the audited `design-inspiration-mcp-server` available as a
replaceable Visual Research discovery transport. It produces candidate
evidence for `VISUAL-RESEARCH-PROTOCOL.md`; it does not choose a design
direction, write implementation tokens, create a site profile state object,
or authorize production assets.

The existing Visual Research protocol remains the interpretation authority.
The existing Awwwards Showcase Intelligence protocol remains the policy and
world-class benchmark authority for Awwwards references. Direct competitor
research, Landbook, cross-industry research, and JCodesMore reconnaissance
remain additive channels.

## 2. Model and upstream pin

The integration uses Model A: an externally configured, pinned stdio MCP
server returns structured search content; the local adapter validates,
normalizes, deduplicates, and bounds that content. The repository does not
install or launch the upstream package, alter global MCP configuration, or
maintain a second provider-specific integration for each platform.

| Field | Recorded value |
| :--- | :--- |
| Repository | `https://github.com/YonasValentin/design-inspiration-mcp-server` |
| Audited commit | `2935c0775fb1cfe3d95503615901e1fa743430e8` |
| Pin type | Immutable commit; automatic updates disabled |
| `package.json` version | `1.0.0` |
| `CHANGELOG.md` version | `1.1.0` (upstream/package discrepancy retained honestly) |
| License | MIT |
| Audit date | 2026-08-29 |
| Transport | stdio |
| Live smoke | `BLOCKED_CREDENTIAL_MISSING` unless a key is already present in the process environment |

The machine-readable record is `upstream.json`. A changed SHA, branch, tag,
or automatic update fails the adapter pin check.

## 3. Source audit record

The audit inspected the upstream README, LICENSE, package manifests and lock
file, the complete `src/index.ts`, and the source dependency graph before any
installation or execution.

### Network

- Search tools POST to `https://google.serper.dev/images` or
  `https://google.serper.dev/search`.
- The upstream source accepts `SERPER_API_KEY` and sends it as an HTTP header;
  the key is not returned by the tool.
- Search results include remote titles, snippets, links, and image URLs. The
  adapter records URLs as reference metadata and does not fetch or download
  them.
- The upstream token path can cause `dembrandt` to inspect an arbitrary URL.
  That open-world behavior is unsafe for ordinary research and is not exposed
  by this adapter.

### Environment and secrets

`SERPER_API_KEY` is the only upstream environment input observed. It is
available, blocked, or disabled through an explicit state model. The adapter
never prints, serializes, tests for a value by echoing it, or stores the key.

### Filesystem and subprocesses

The audited `src/index.ts` has no direct filesystem API. It invokes
`dembrandt` through Node `execFile` with argv separation, a 60-second timeout,
and a 5 MiB output buffer. It resolves an executable from `PATH` and returns
raw error text. `dembrandt` is external and independently versioned, so its
filesystem/browser behavior is not accepted as an audited repository runtime.
The Website Director adapter does not invoke it, spawn a process, or write a
file.

### MCP tools and output handling

The upstream server registers `design_search_images`,
`design_search_references`, `design_search_styles`, and
`design_extract_tokens`. The adapter exposes only the first three. Upstream
text truncates at 25,000 characters and image/reference counts are accepted
from bounded tool arguments; the adapter applies its own smaller stage budget,
canonical URL deduplication, supported-platform filter, normalized fields,
and provenance.

The raw upstream result is not a design instruction. No HTML, CSS, token set,
asset file, or implementation specification crosses this boundary.

Observed upstream errors include missing-key configuration failure, HTTP 401
invalid-key failure, HTTP 429 rate limiting, other non-OK response text, and
`dembrandt` timeout/process/stderr/JSON parsing failures. The adapter exposes
none of those raw error paths to a production workflow; request preparation
returns a bounded status and missing credentials remain
`BLOCKED_CREDENTIAL_MISSING`.

### Dependencies and remote handling

The package declares `@modelcontextprotocol/sdk` and `zod` as direct runtime
dependencies, with 92 transitive lockfile entries. The inspected lockfile had
no package install scripts. The adapter has no runtime dependency beyond the
Python standard library. The repository records the upstream dependency audit
but does not vendor or install it.

## 4. Supported discovery platforms

The unified adapter formally recognizes exactly five source platforms:

| Platform | Discovery signal | Interpretation owner |
| :--- | :--- | :--- |
| Dribbble | Interface pattern signal; filter aggressively for production utility | Visual Research |
| Behance | Case-study and material-system signal | Visual Research |
| Awwwards | Showcase benchmark and craft signal | `AWWWARDS-SHOWCASE-INTELLIGENCE.md` |
| Mobbin | Product-flow and interaction sequencing signal | Visual Research |
| Pinterest | Broad mood/material signal; low provenance strength until verified | Visual Research |

Recognition is unified. This integration does not create five separate MCP
clients or make platform popularity a quality judgment.

## 5. Query policy and bounded budget

Queries must be specific to the project brief, positioning, research brief,
business/audience, emotional posture, design ambition, conversion goal, or
reference mode. Generic input such as `good design`, `nice website`, `cool
landing page`, or `best UI` is rejected or rewritten from those fields.
Sensitive values, email addresses, API keys, tokens, passwords, and arbitrary
credential fields are rejected or redacted before a request can be prepared.
Queries remain within the upstream 200-character bound.

The deterministic budget is:

| Stage | Default | Maximum |
| :--- | ---: | ---: |
| Initial discovery | 8 | 12 |
| Shortlist | 3 | 6 |
| Deep study | 1 | 3 |

Canonical source URLs remove tracking parameters and trailing differences.
Repeated sources are deduplicated before synthesis. Each candidate records
platform, source URL, exact query, retrieval timestamp, provider, upstream
commit, and `REFERENCE_ONLY` boundary.

## 6. Normalized evidence model

Each normalized candidate follows `normalized-result.schema.json` and includes:

`source_platform`, `source_url`, `title`, `image_url`, `query`,
`pattern_type`, `visual_notes`, `production_plausibility`, `reference_grade`,
`copyright_boundary`, `retrieved_at`, `provider`, and `upstream_commit`.

Raw image URLs are reference pointers only. Asset Director owns production
image selection, licensing, provenance, optimization, and responsive crops.

## 7. Reference grading heuristic

The adapter provides a transparent, deterministic heuristic, not an objective
mathematical truth. Reviewers score each dimension from 0 to 5:

`VISUAL_CRAFT`, `SUBJECT_RELEVANCE`, `DISTINCTIVENESS`,
`INFORMATION_HIERARCHY`, `TYPOGRAPHIC_QUALITY`, `LAYOUT_QUALITY`,
`BRAND_FIT`, `CONVERSION_APPLICABILITY`, `RESPONSIVE_PLAUSIBILITY`,
`ACCESSIBILITY_PLAUSIBILITY`, and `IMPLEMENTABILITY`.

- **A:** strong craft, subject fit, and production plausibility.
- **B:** useful reference with bounded transferability.
- **C:** limited fit or utility; retain only with an explicit reason.
- **D:** high visual signal with low production utility, including “Dribbble
  fantasy” references that do not survive responsive, accessibility, or
  implementation scrutiny.

Missing scores remain `UNASSESSED`; they are never inferred as a pass.

## 8. Token extraction boundary

`design_extract_tokens` is disabled in ordinary adapter use. The audited source
normalizes a URL by prepending `https://` when needed and passes it to
`dembrandt` without a public-host, HTTPS, or private-network allowlist. That
creates open-world/SSRF and arbitrary subprocess-output risk.

Only a future, deliberate `REFERENCE_DECONSTRUCTION_MODE` may make a public or
explicitly authorized HTTPS URL eligible, and only after a separate
subprocess audit confirms a pinned `dembrandt` installation. The current
adapter returns a policy status and no tokens; it never executes `dembrandt`.
If any requirement is missing, the status is `TOKEN_EXTRACTION_BLOCKED`.
Ordinary search normalization is unaffected.

## 9. Originality and production boundaries

The adapter refuses requests to clone, copy, reproduce, duplicate, or make a
pixel-perfect version of a reference. The allowed transformation is:

`reference evidence -> transferable pattern -> client-specific reason -> original synthesis`

MCP evidence may not directly set design direction, implementation tokens,
copy, components, exact layouts, branded graphics, or production asset paths.
The canonical phrase is: **RESEARCH PATTERNS, DO NOT CLONE COMPOSITIONS.**

## 10. Example configuration

`mcp-client-config.example.json` contains placeholders only. An owner may
configure a local client against the audited pinned checkout with
`SERPER_API_KEY` already present in the process environment. No global MCP
configuration is changed by this repository.
