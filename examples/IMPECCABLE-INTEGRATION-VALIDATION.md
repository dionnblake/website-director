# WEBSITE DIRECTOR: IMPECCABLE V4.3.1 SURGICAL REFRESH VALIDATION

> Integration version: 1.1.0
> Framework version: 2.15.0
> Status: CURATED_IMPLEMENTATION_RETAINED
> Scope: local, provider-neutral, read-only design-quality scanning

This file is a reference validation example. The executable assertions live
in tests/test_impeccable.py and are registered inside the existing
framework_validation suite. This example does not create a new phase, gate,
state, orchestrator, owner lock, provider, hook, browser daemon, or deployment.

## 1. Upstream identity

| Attribute | Evidence |
| :--- | :--- |
| Repository | https://github.com/pbakaus/impeccable |
| Previous tag and commit | skill-v4.1.2 / 63b04e2530f5c7b41ea83c133daab24f34912456 |
| Target tag and commit | skill-v4.3.1 / cd12f8660e2dde57b9615c8a6b8ea674101f9cfc |
| Previous registry | 59 rule IDs |
| Target registry | 61 built-in rule IDs |
| Registry delta | organic-clip-path, buried-raster |
| License | Apache License 2.0 |
| universal.zip | 15,625,571 bytes |
| universal.zip SHA-256 | 1deea4cdfb1608df6d9e08ef359629e7cc866a22ab7c2195a835627b887f190b |
| Target verification | YES for tag, commit, release metadata, license, and digest |

The release sidecar matched the artifact metadata and digest. The upstream
binary was not executed and no upstream provider package was installed.

## 2. Integration decision

Option A, the official upstream engine adapter, is rejected for this refresh.
The official source and release identity were audited, but a compatible
Website Director adapter, approved binary lifecycle, cross-platform execution
proof, and non-duplicating context boundary were not all established.

Option B is retained in framework_validation/impeccable.py. It preserves the
18 existing contractual entries, supports both side-tab IDs, and adopts nine
new static or explainable heuristic rules. Runtime, accessibility, design
system, and qualitative rules remain with their existing owners.

ENGINE_DECISION = CURATED_IMPLEMENTATION_RETAINED
ENGINE_ADOPTION = REJECTED
LEGACY_EXECUTABLE_SCANNER_PRESENT = NO
LEGACY_VALIDATION_DOCUMENT_ACCURATE = YES after this correction
LEGACY_VALIDATION_DOCUMENT_ACCURATE_BEFORE_REFRESH = PARTIAL
UPSTREAM_RULE_COUNT_DISCOVERED = 61
EXISTING_RULES_ACCOUNTED_FOR = 18 contractual entries; 18 upstream IDs plus the Website Director touch-target extension
NEW_RULES_ADOPTED = 9
NEW_STATIC_RULES_ADOPTED = 5
NEW_HEURISTIC_RULES_ADOPTED = 4
RULES_REJECTED_OR_DELEGATED = 34

## 3. Executable validation scenarios

| ID | Scenario | Expected evidence |
| :--- | :--- | :--- |
| 01 | Existing contract positives | All 18 entries detect their synthetic positive fixture |
| 02 | Existing contract negatives | Clean controls do not produce those rule IDs |
| 03 | v4.3.1 additions | Nine adopted IDs each have positive and negative controls |
| 04 | Normalized findings | Exactly nine fields and the declared method taxonomy |
| 05 | Contextual override | Only an explicitly locked design direction authorizes a heuristic |
| 06 | Lock protection | Locked repair impact is reported without changing the lock registry |
| 07 | Browser and Accessibility ownership | Runtime-only IDs are not emitted by the source scanner |
| 08 | Engine failure modes | Missing or corrupt official artifacts return BLOCKED; no fallback pass |
| 09 | Windows and POSIX paths | Backslashes normalize to stable slash-separated locations |
| 10 | Frozen and historical integrity | The protected projects corpus and 2.15 profile remain unchanged |
| 11 | Explicit output-directory root | A selected `build` or `dist` root is scanned; nested ignored directories remain excluded |
| 12 | No scannable input | Empty, unsupported-only, and empty source-map inputs fail closed and cannot PASS |

Run the targeted proof with:

    python -m unittest tests.test_impeccable

Run the canonical full proof with:

    python -m framework_validation --run-suites

The suite runs only local synthetic inputs. It does not make a network
request, call a provider, execute an upstream binary, open a browser, or write
under projects/.

## 4. Finding example

    FINDING_ID: DET-001
    SOURCE: IMPECCABLE_DETECTOR
    METHOD: DETERMINISTIC
    RULE: low-contrast
    LOCATION: src/page.css:12
    SEVERITY: MAJOR
    EVIDENCE: computed contrast 2.80:1 is below the 4.50:1 body threshold
    REMEDIATION: increase contrast or use the approved design-system token
    LOCK_IMPACT: NONE

An authorized heuristic remains in the result with remediation text beginning
AUTHORIZED_BY_LOCK. It is not deleted and the scanner does not mutate the
locked design direction.

## 5. Ownership boundary

The scanner owns only the rows marked A, B, or C in the complete matrix in
IMPECCABLE-ENGINE-PROTOCOL.md. Browser QA owns live console errors, viewport
geometry, clipping, occlusion, post-reveal state, and rendered/runtime asset
integrity. Accessibility owns logical heading hierarchy, computed rendered
assertions, and manual criteria. `skipped-heading` is therefore not emitted
by Impeccable. Impeccable's `broken-image` finding is only an obvious
source-level missing/empty/placeholder precheck and cannot substitute for the
Browser QA asset-integrity verdict. Design Constitution and Design System own
token identity. Website Gauntlet owns qualitative visual and copy judgment.

The previous example claimed a Node module named
impeccable-scanner-test.js. That file was not present in the historical
checkout. The claim is removed rather than retroactively fabricated.
