# SlopMonster Copy-Lint Surgical Review

## Final report fields

```text
SLOPMONSTER_COPY_LINT_REVIEW = VERIFIED
WEBSITE_DIRECTOR_BASE_SHA = 0b8f7902b93658e138b05c6d22a90ead17bbdf06
FINAL_BRANCH = codex/slopmonster-copy-lint-surgical
FINAL_SHA = RECORDED_AT_CLOSEOUT_IN_FINAL_RESPONSE
FRAMEWORK_VERSION_BEFORE = 2.15.0
FRAMEWORK_VERSION_AFTER = 2.15.0
SLOPMONSTER_UPSTREAM_SHA = f261dbf11c2a206ecd8780c070a46dae64edd8be
SLOPMONSTER_UPSTREAM_VERIFIED = YES
SLOPMONSTER_LICENSE = MIT, Copyright (c) 2026 Jack Roberts
ATTRIBUTION_REQUIRED = YES
ATTRIBUTION_IMPLEMENTED = YES
UPSTREAM_PATTERN_COUNT = 83
PATTERNS_ADOPTED = 13
PATTERNS_NARROWED = 3
PATTERNS_DELEGATED = 7
PATTERNS_REJECTED = 60
COPY_LINTER_DECISION = CURATED_IMPLEMENTATION_JUSTIFIED
SCORE_5_OF_5_ADOPTED = NO
CLEANSE_SCRIPT_ADOPTED = NO
RIVAL_MODEL_ROUTING_ADOPTED = NO
AUTOMATIC_REWRITE_ADOPTED = NO
PROOF_PATTERN_FINAL_OWNER = Capability 7 Provenance, EVIDENCE-PROVENANCE-PROTOCOL.md
PROVENANCE_AUTHORITY_PRESERVED = YES
GAUNTLET_AUTHORITY_PRESERVED = YES
CONTENT_LOCK_INTEGRATION = Existing content-plan checklist evidence only; locked findings use the existing Owner Change Request path
LOCKED_COPY_MUTATION_ALLOWED = NO
ENGLISH_ONLY_BOUNDARY = Known-locale English is scanned; known non-English is NOT_APPLICABLE; unknown locale is BLOCKED
NON_ENGLISH_FALSE_PASS_POSSIBLE = NO
POST_BUILD_RENDERED_COPY_SCAN = DEFERRED_NO_EXISTING_SURFACE
OWNER_LOCK_COUNT_BEFORE = 5
OWNER_LOCK_COUNT_AFTER = 5
NEW_STATE_MACHINES = 0
NEW_PHASES = 0
NEW_GATES = 0
NEW_ORCHESTRATORS = 0
PROJECTS_MUTATED = NO
PROTECTED_CORPUS_INTEGRITY = VERIFIED
CORPUS_TRUE_POSITIVES = 0
CORPUS_FALSE_POSITIVES = 0
CORPUS_NOTES = The scanner is a pre-lock source-copy aid. The five protected homepage artifacts contained no adopted matches. Rejected/delegated upstream signals included legitimate leverage, elevate, unlock, transformation, curated, whether, and list constructions.
TARGETED_TESTS = python -m unittest tests.test_copy_quality -v: 14/14 PASS
FULL_TEST_SUITE = python -m framework_validation --run-suites: 269 checks PASS, 0 failed, 0 blocked, 0 warnings
GLOBAL_VERIFIER = node C:\Users\ALPHA\.context\scripts\verify.js <project dir>: VERIFIED; pytest all passed
WINDOWS_CI = NOT_RUN
UBUNTU_CI = NOT_RUN
MAIN_MUTATED = NO
DEPLOYMENT_PERFORMED = NO
PR_CREATED = NO
```

`FINAL_SHA`, `FULL_TEST_SUITE`, and `GLOBAL_VERIFIER` are updated in the
closeout response after the final commit and verification run. This report is
an evidence record, not a new Website Director protocol, state, gate, or lock.

## Decision

`CURATED_IMPLEMENTATION_JUSTIFIED`, subject to owner review before any locked
copy is changed.

The useful boundary is a deterministic source-copy precheck with a small set
of high-signal constructions and two structural density observations. It emits
review findings with `FINDING_ID`, `SOURCE`, `METHOD`, `RULE`,
`LOCATION_OR_CONTEXT`, `SEVERITY`, `EVIDENCE`, `REMEDIATION`, and `LOCK_IMPACT`.
It does not issue a clean-copy verdict, score, rewrite, claim verdict, or
approval.

The upstream catalogue was not imported wholesale. The five representative
protected homepage artifacts were already free of the selected findings, while
the same audit found legitimate local uses of broad vocabulary, a qualifier,
and Oxford lists. That is evidence to keep those rules out of a deterministic
Website Director scanner, not evidence that every future draft is perfect.

## Scope and provenance

Website Director base was verified at `origin/main` and the local remote:

```text
0b8f7902b93658e138b05c6d22a90ead17bbdf06
```

The upstream repository was cloned into the disposable audit directory
`C:\Users\ALPHA\AppData\Local\Temp\website-director-slopmonster-audit-20260910`,
detached at the requested commit, and verified against both `HEAD` and the
upstream `main` ref. The audited upstream source is [SlopMonster on
GitHub](https://github.com/ItsssssJack/SlopMonster), specifically [commit
f261dbf11c2a206ecd8780c070a46dae64edd8be](https://github.com/ItsssssJack/SlopMonster/commit/f261dbf11c2a206ecd8780c070a46dae64edd8be).
Its `LICENSE` is MIT, Copyright (c) 2026 Jack Roberts. The Website Director
implementation carries that attribution in the module docstring and here.

Inspected upstream materials:

- `tools/deslop.py`
- `tools/test_deslop.py`
- `tools/cleanse.sh` and `tools/test_cleanse.sh` were inspected but never run
- `README.md`
- `SKILL.md`
- `references/principles.md`
- `LICENSE`

The upstream implementation contains 39 root vocabulary patterns, 21 exact
vocabulary patterns, 17 phrase patterns, and 6 structural or proof patterns.
The upstream `5/5` score, build gate, rival-model cleanse, and English-only
false-5/5 behavior were explicitly excluded.

## Upstream pattern disposition matrix

Every upstream pattern receives one disposition. `ADOPT_HEURISTIC` means the
pattern is used as a review finding. `ADOPT_WITH_NARROWING` means the
concept is used only with the narrower Website Director boundary. The
delegated rows are not executable scanner rules.

| # | Upstream pattern | Disposition | Website Director decision and owner |
|---:|---|---|---|
| 1 | `delve` | `REJECT_FALSE_POSITIVE_RISK` | Broad verb; context is required. |
| 2 | `leverage` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate technical and business term in the protected corpus. |
| 3 | `seamless` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent quality claim. |
| 4 | `elevate` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate technical verb in the protected corpus. |
| 5 | `robust` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent engineering adjective. |
| 6 | `unlock` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate domain verb and broad metaphor. |
| 7 | `unleash` | `REJECT_FALSE_POSITIVE_RISK` | Broad marketing verb. |
| 8 | `empower` | `REJECT_FALSE_POSITIVE_RISK` | Broad value verb. |
| 9 | `streamline` | `REJECT_FALSE_POSITIVE_RISK` | Valid process term in many briefs. |
| 10 | `cutting-edge` | `DELEGATE_PROVENANCE` | If used as a factual comparative claim, Provenance owns support; no lexical finding. |
| 11 | `state-of-the-art` | `DELEGATE_PROVENANCE` | If used as a factual comparative claim, Provenance owns support; no lexical finding. |
| 12 | `game-changer` | `REJECT_FALSE_POSITIVE_RISK` | Broad evaluative metaphor. |
| 13 | `game-changing` | `REJECT_FALSE_POSITIVE_RISK` | Broad evaluative adjective. |
| 14 | `revolutionize` | `REJECT_FALSE_POSITIVE_RISK` | Broad claim language. |
| 15 | `revolutionise` | `REJECT_FALSE_POSITIVE_RISK` | Broad claim language and spelling variant. |
| 16 | `transformative` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent positioning language. |
| 17 | `transformation` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate domain noun in the protected corpus. |
| 18 | `innovate` | `REJECT_FALSE_POSITIVE_RISK` | Broad verb. |
| 19 | `holistic` | `REJECT_FALSE_POSITIVE_RISK` | Domain-dependent term. |
| 20 | `synergy` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent business term. |
| 21 | `synergies` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent business term and plural. |
| 22 | `paradigm` | `REJECT_FALSE_POSITIVE_RISK` | Domain-dependent noun. |
| 23 | `bespoke` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate service descriptor in some briefs. |
| 24 | `meticulous` | `REJECT_FALSE_POSITIVE_RISK` | Subjective quality adjective. |
| 25 | `tapestry` | `REJECT_FALSE_POSITIVE_RISK` | Metaphor with legitimate editorial use. |
| 26 | `testament` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent rhetorical noun. |
| 27 | `beacon` | `REJECT_FALSE_POSITIVE_RISK` | Metaphor with legitimate brand use. |
| 28 | `unparalleled` | `DELEGATE_PROVENANCE` | Absolute comparative claim belongs to evidence review, not lexical lint. |
| 29 | `supercharge` | `REJECT_FALSE_POSITIVE_RISK` | Broad marketing verb. |
| 30 | `turbocharge` | `REJECT_FALSE_POSITIVE_RISK` | Broad marketing verb. |
| 31 | `effortless` | `REJECT_FALSE_POSITIVE_RISK` | User-outcome claim requires context. |
| 32 | `next-level` | `REJECT_FALSE_POSITIVE_RISK` | Broad positioning phrase. |
| 33 | `pivotal` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent emphasis. |
| 34 | `foster` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate verb in editorial and service copy. |
| 35 | `showcase` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate product and portfolio verb. |
| 36 | `compelling` | `REJECT_FALSE_POSITIVE_RISK` | Subjective quality adjective. |
| 37 | `intuitive` | `REJECT_FALSE_POSITIVE_RISK` | Usability claim requires runtime and user context. |
| 38 | `world-class` | `DELEGATE_PROVENANCE` | Absolute comparative claim belongs to evidence review, not lexical lint. |
| 39 | `best-in-class` | `DELEGATE_PROVENANCE` | Comparative claim belongs to evidence review, not lexical lint. |
| 40 | `crafted` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate craft descriptor. |
| 41 | `curated` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate section and disclosure language in the protected corpus. |
| 42 | `harnessing` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate technical verb form. |
| 43 | `harness the power` | `REJECT_FALSE_POSITIVE_RISK` | Broad phrase but literal technical contexts exist. |
| 44 | `journey` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate user and editorial metaphor. |
| 45 | `realm` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent noun. |
| 46 | `landscape` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate domain noun. |
| 47 | `navigate the` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate interaction and domain verb. |
| 48 | `in the world of` | `REJECT_FALSE_POSITIVE_RISK` | Broad opener with legitimate editorial use. |
| 49 | `in today's` | `REJECT_FALSE_POSITIVE_RISK` | Time framing is context-dependent. |
| 50 | `ever-evolving` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent change descriptor. |
| 51 | `fast-paced` | `REJECT_FALSE_POSITIVE_RISK` | Context-dependent descriptor. |
| 52 | `look no further` | `REJECT_FALSE_POSITIVE_RISK` | Common CTA language with literal navigational uses. |
| 53 | `dive in` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate action label and metaphor. |
| 54 | `let's dive` | `REJECT_FALSE_POSITIVE_RISK` | Broad invitation phrase. |
| 55 | `deep dive` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate research and content term. |
| 56 | `embark` | `REJECT_FALSE_POSITIVE_RISK` | Broad metaphor. |
| 57 | `unlock the power` | `REJECT_FALSE_POSITIVE_RISK` | Broad marketing phrase. |
| 58 | `buckle up` | `REJECT_FALSE_POSITIVE_RISK` | Literal safety language makes lexical detection unsafe. |
| 59 | `the secret sauce` | `REJECT_FALSE_POSITIVE_RISK` | Metaphor with context-dependent editorial use. |
| 60 | `level up` | `REJECT_FALSE_POSITIVE_RISK` | Common product and game action language. |
| 61 | `not just X, but Y` | `ADOPT_HEURISTIC` | High-signal contrast construction; manual review only. |
| 62 | `not just X, it's Y` | `ADOPT_HEURISTIC` | High-signal contrast construction; manual review only. |
| 63 | `whether you're X or Y` | `DELEGATE_GAUNTLET` | Legitimate audience qualifier in the protected corpus; contextual critique remains qualitative. |
| 64 | `more than just` | `ADOPT_HEURISTIC` | Stock contrast opener with a bounded review finding. |
| 65 | `this/that's where ... comes in` | `ADOPT_HEURISTIC` | Stock transition with a bounded review finding. |
| 66 | `say goodbye to` | `ADOPT_HEURISTIC` | High-signal departure promise; manual review only. |
| 67 | `imagine a/an/the` | `ADOPT_HEURISTIC` | Invitation opener; context remains with the writer. |
| 68 | `in conclusion` or `to sum up` | `ADOPT_HEURISTIC` | Essay-summary transition; manual review only. |
| 69 | `when it comes to` | `ADOPT_HEURISTIC` | Throat-clearing transition; manual review only. |
| 70 | `at the end of the day` | `ADOPT_HEURISTIC` | Stock summary phrase; manual review only. |
| 71 | `the key is` or `the truth is` | `REJECT_FALSE_POSITIVE_RISK` | Ordinary explanatory phrases make the combined rule too broad. |
| 72 | `helps you to` or `can help you` | `REJECT_FALSE_POSITIVE_RISK` | Legitimate service and accessibility language. |
| 73 | `may/could potentially` or `might possibly` | `ADOPT_HEURISTIC` | Redundant hedge construction with precise review remediation. |
| 74 | `very unique` or `quite literally` | `ADOPT_HEURISTIC` | Intensifier check with manual accuracy review. |
| 75 | `here's the thing`, `let's break it down`, or `the best part` | `ADOPT_WITH_NARROWING` | Scan only the two opener forms; exclude ordinary `the best part` usage. |
| 76 | `ready to get started` or `let's get started` | `ADOPT_HEURISTIC` | Generic CTA opener; the existing CTA authority remains in place. |
| 77 | `the result/answer/catch/kicker/upshot?` | `ADOPT_HEURISTIC` | Self-answering rhetorical lead; manual review only. |
| 78 | Two em dashes in a 220-character sentence window | `ADOPT_WITH_NARROWING` | Source-copy sentence window only; no page score or build gate. |
| 79 | Four or more hyphenated compounds in a 220-character sentence window | `ADOPT_WITH_NARROWING` | Source-copy sentence window only; no page score or build gate. |
| 80 | Semicolon density | `REJECT_FALSE_POSITIVE_RISK` | House style and technical prose make page-length density ambiguous. |
| 81 | Oxford tricolon | `REJECT_FALSE_POSITIVE_RISK` | Nine legitimate local list observations were found. |
| 82 | Non-Oxford tricolon | `REJECT_FALSE_POSITIVE_RISK` | Service and information lists are legitimate copy structures. |
| 83 | Numeric proof with people nouns | `DELEGATE_PROVENANCE` | Capability 7 owns evidence, support, rights, and truth status. |

The disposition counts are mutually exclusive and sum to 83:

```text
13 ADOPT_HEURISTIC + 3 ADOPT_WITH_NARROWING + 7 delegated + 60 rejected = 83
```

## Adopted behavior

The implementation is [framework_validation/copy_quality.py](framework_validation/copy_quality.py).
It is standard-library-only and accepts supplied `plain` or simple `markdown`
text plus an explicit source locale. It returns `SCANNED`, `NOT_APPLICABLE`, or
`BLOCKED` as applicability state for the call; none is a Website Director
readiness state.

Adopted rules emit `MINOR` heuristic findings. Empty input is a deterministic
`BLOCKED` input condition. Unknown locale is `BLOCKED`; known non-English input
is `NOT_APPLICABLE`. The scanner does not infer language from text and does not
claim that non-English copy is clean.

The content workflow integration is one checklist item in the existing
`templates/content-plan.md` Content Lock section. A finding on unlocked copy
has `LOCK_IMPACT = REVIEW_BEFORE_CONTENT_LOCK`; a finding on locked copy has
`LOCK_IMPACT = LOCKED_CHANGE_REQUIRED`. Existing `content_structure_locked`
ownership and the Owner Change Request path remain authoritative. No schema
state, gate, phase, lock, orchestrator, or approval route was added.

## Delegated and rejected concerns

- Numeric or social proof is not a copy-lint finding. `EVIDENCE-PROVENANCE-PROTOCOL.md`
  owns source support, rights, attribution, currentness, and production claim
  truth status.
- Broad comparative or absolute terms are not lexical findings. If a real
  claim uses them, Provenance owns the evidence review.
- `whether you're X or Y` and similar contextual rhetoric remains a qualitative
  Gauntlet concern because the protected corpus contains a legitimate audience
  qualifier.
- Tricolons, semicolon density, broad vocabulary, and ordinary `the best part`
  language are rejected from deterministic detection because local examples
  demonstrate unacceptable ambiguity.
- No automatic rewrite, rival-model route, `cleanse.sh` path, provider, or
  subprocess exists in the implementation.

## Corpus evaluation

Protected corpus files were never edited. The conservative corpus was five
representative home artifacts, one per protected Alpha Starts Now surface:

```text
projects/alpha-starts-now/build/index.html
projects/alpha-starts-now-clean-room/build/index.html
projects/alpha-starts-now-flagship-proof/production/index.html
projects/alpha-starts-now-v1-1/build/index.html
projects/alpha-starts-now-v1-6-flagship/build/index.html
```

Visible text was extracted read-only for this audit. This is source-artifact
evaluation, not a new Browser QA rendered-text observation. The adopted
scanner found zero matches across those five artifacts. The upstream audit
found 21 legitimate observations from rules that were rejected or delegated:

| Signal family | Count | Corpus context |
|---|---:|---|
| `leverage` root vocabulary | 4 | Professional and technical language. |
| `elevate` root vocabulary | 2 | Technical physiology copy. |
| `unlock` root vocabulary | 1 | Technical biology copy. |
| `transformation` root vocabulary | 1 | Anti-hype discussion of transformation promises. |
| `curated` exact vocabulary | 3 | Section title, arsenal language, and affiliate disclosure. |
| `whether ... or ...` phrase | 1 | Legitimate audience qualifier. |
| Oxford tricolon | 9 | Service, information architecture, and technical lists. |

The 21 observations are not treated as adopted-rule false positives because
those upstream rules are not in the scanner. They are recorded as the reason
for rejecting or delegating them. No claim was made that the corpus contains a
known bad adopted-pattern true positive.

## Existing-authority checks

- `DESIGN-CONSTITUTION.md` §7.6 remains the copy-quality authority and §7.7
  remains the factual-integrity authority.
- `templates/content-plan.md` remains the copy plan and Content Lock checklist.
- `EVIDENCE-PROVENANCE-PROTOCOL.md` remains the proof and factual-claim owner.
- `content_structure_locked` remains one of exactly five owner locks.
- The Gauntlet remains the qualitative rendered-copy and generic-language
  critic.
- Browser QA was not expanded. Its existing observations do not establish a
  full rendered visible-copy surface, so the post-build scan is
  `DEFERRED_NO_EXISTING_SURFACE`.
- Framework version remains 2.15.0.
- No file under `projects/` was changed.

## Verification evidence

Targeted development verification passed:

```text
python -m unittest tests.test_copy_quality -v
Ran 13 tests
OK
```

The targeted tests cover every adopted rule with positive and negative cases,
literal-sense controls, UTF-8 typography, Markdown extraction, empty input,
English and non-English applicability, unknown-language blocking, proof-owner
separation, lock impact, deterministic output, process/provider absence,
protected-corpus read-only scanning, and the no-new-suite/no-new-gate/five-lock
invariants.

Upstream tests passed in the detached pinned checkout:

```text
python tools/test_deslop.py
all tests passed
```

The prohibited cleanse scripts were not executed. The registered Website
Director full-suite and global-verifier evidence is recorded above.

## Files changed

- `framework_validation/copy_quality.py`
- `tests/test_copy_quality.py`
- `schemas/test-suites.json` (existing framework-validation suite only)
- `framework_validation/AGENTS.md`
- `tests/AGENTS.md`
- `templates/content-plan.md`
- `DESIGN-CONSTITUTION.md`
- `SKILL.md`
- `SLOPMONSTER-COPY-LINT-REVIEW.md`

No existing Browser QA file, state registry, gate registry, project surface,
deployment surface, or main branch was changed.

## Recommendation

`OWNER_REVIEW_REQUIRED`.

The curated implementation is narrow enough to be useful as a pre-lock review
aid and explicit enough to avoid a false clean-copy claim. Owner review is
still required before any finding changes locked production copy. Do not adopt
the rejected upstream vocabulary, proof detector, score gate, cleanse flow,
rival-model routing, or automatic rewrite path.
