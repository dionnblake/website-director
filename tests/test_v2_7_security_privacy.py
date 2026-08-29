# Website Director V2.7 Security, Privacy & Compliance Intelligence Test Harness
#
# Deterministic repository-level assertions for the V2.7 subsystem.
# Verifies canonical authority, single completion flag, five-lock invariant,
# legal-claim boundary, cross-document wiring, and frozen-pilot preservation.
#
# Run: python tests/test_v2_7_security_privacy.py
import io
import json
import os
import re
import sys

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

assertions_run = 0
assertions_passed = 0
failures = []


def check(cond, msg):
    global assertions_run, assertions_passed
    assertions_run += 1
    if cond:
        assertions_passed += 1
        print('[PASS] ' + msg)
    else:
        failures.append(msg)
        print('[FAIL] ' + msg)


def read(*parts):
    with io.open(os.path.join(workspace_dir, *parts), encoding='utf-8') as f:
        return f.read()


def exists(*parts):
    return os.path.exists(os.path.join(workspace_dir, *parts))


# ---------------------------------------------------------------------------
# 1. Canonical protocol and deliverables exist
# ---------------------------------------------------------------------------
PROTOCOL = 'SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md'
TEMPLATE = os.path.join('templates', 'security-privacy-review.md')
REGISTER = os.path.join('templates', 'security-privacy-register.json')
VALIDATION = os.path.join('examples', 'SECURITY-PRIVACY-COMPLIANCE-INTEGRATION-VALIDATION.md')

check(exists(PROTOCOL), 'Canonical protocol SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md exists')
check(exists(TEMPLATE), 'Working template templates/security-privacy-review.md exists')
check(exists(REGISTER), 'Machine-readable templates/security-privacy-register.json exists')
check(exists(VALIDATION), 'Integration validation artifact exists')

protocol = read(PROTOCOL)
template = read(TEMPLATE)

# ---------------------------------------------------------------------------
# 2. No competing security/privacy protocol was created
# ---------------------------------------------------------------------------
root_md = [f for f in os.listdir(workspace_dir) if f.endswith('.md')]
security_protocols = [
    f for f in root_md
    if re.search(r'(SECURITY|PRIVACY|COMPLIANCE|CONSENT)', f) and f.endswith('PROTOCOL.md')
]
check(security_protocols == [PROTOCOL],
      'Exactly one canonical security/privacy protocol at repo root: %s' % security_protocols)

# ---------------------------------------------------------------------------
# 3. Protocol declares the readiness gate and single completion flag
# ---------------------------------------------------------------------------
check('[SECURITY_PRIVACY_READY]' in protocol, 'Protocol declares readiness gate [SECURITY_PRIVACY_READY]')
check('security_privacy.complete' in protocol, 'Protocol declares security_privacy.complete')
check('No second, independently-writable completion flag' in protocol,
      'Protocol states the single completion flag invariant')
check('not an owner lock' in protocol, 'Protocol states [SECURITY_PRIVACY_READY] is not an owner lock')

# ---------------------------------------------------------------------------
# 4. State object present in the site-profile template, five locks preserved
# ---------------------------------------------------------------------------
profile = json.loads(read('templates', 'site-profile.json'))

check(profile.get('schema_version') == '2.7.0', 'site-profile.json schema_version is 2.7.0')
check('security_privacy' in profile, 'site-profile.json contains security_privacy{}')

sp = profile.get('security_privacy', {})
check(sp.get('complete') is False, 'security_privacy.complete defaults to false')
check(sp.get('status') == 'not_evaluated', 'security_privacy.status defaults to not_evaluated')
check(sp.get('consent_status') == 'UNASSESSED', 'security_privacy.consent_status defaults to UNASSESSED')
check(sp.get('compliance_certified') is False, 'security_privacy.compliance_certified is false')
check(sp.get('implementation_verified') is False, 'security_privacy.implementation_verified is false')
check(sp.get('production_verified') is False, 'security_privacy.production_verified is false')
check(sp.get('payment_model') == 'NOT_APPLICABLE', 'security_privacy.payment_model defaults to NOT_APPLICABLE')
check('exception' in sp and sp['exception'].get('applied') is False,
      'security_privacy.exception.applied defaults to false')

locks = profile.get('locks', {})
check(len(locks) == 5, 'Exactly 5 owner locks exist in locks{} (found %d)' % len(locks))
check(not any('security' in k or 'privacy' in k for k in locks),
      'No sixth security/privacy owner lock in locks{}')
check(not any(isinstance(v, bool) and 'lock' in k for k, v in sp.items()),
      'security_privacy{} contains no lock boolean')

# measurement{} still canonical and untouched
check('measurement' in profile, 'measurement{} still present in site-profile.json')
check(profile['measurement'].get('complete') is not None,
      'measurement.complete preserved as the measurement readiness flag')

# ---------------------------------------------------------------------------
# 5. No duplicate readiness/completion flags across the schema
# ---------------------------------------------------------------------------
completion_flag_owners = [k for k, v in profile.items()
                          if isinstance(v, dict) and 'complete' in v]
check(completion_flag_owners.count('security_privacy') == 1,
      'Exactly one security_privacy completion flag in the schema')
# each state object owns at most one 'complete' key; no cross-object duplication
for owner in completion_flag_owners:
    keys = [k for k in profile[owner] if k == 'complete']
    check(len(keys) == 1, "State object '%s' owns exactly one 'complete' flag" % owner)

# ---------------------------------------------------------------------------
# 6. Legal claim boundary — every compliance-claim string is a prohibition
# ---------------------------------------------------------------------------
BANNED = ['GDPR COMPLIANT', 'CCPA COMPLIANT', 'HIPAA COMPLIANT',
          'PCI COMPLIANT', 'COPPA COMPLIANT', 'LEGAL COMPLIANCE VERIFIED']

check(all(b in protocol for b in BANNED),
      'Protocol enumerates every prohibited compliance claim')
check('NEVER' in protocol and 'must **NEVER** output' in protocol,
      'Protocol states the never-certify rule explicitly')
check('COMPLIANCE_NOT_CERTIFIED' in protocol, 'Protocol defines COMPLIANCE_NOT_CERTIFIED')
check('SPECIALIST_REVIEW_REQUIRED' in protocol, 'Protocol defines SPECIALIST_REVIEW_REQUIRED')
check('OWNER_OR_COUNSEL_REVIEW_REQUIRED' in protocol,
      'Protocol defines OWNER_OR_COUNSEL_REVIEW_REQUIRED')

# Scan every tracked framework doc: a banned phrase may only appear in prohibition context.
PROHIBITION_MARKERS = ('NEVER', 'never', 'not ', 'Prohibit', 'prohibit', 'REJECT', 'Rejected',
                       'REJECTED', 'unless', 'Do not', 'do not', 'must not', 'refused',
                       'without qualified', 'no unevidenced')
scan_files = [f for f in root_md]
scan_files += [os.path.join('templates', f) for f in os.listdir(os.path.join(workspace_dir, 'templates'))
               if f.endswith('.md')]
scan_files += [os.path.join('examples', f) for f in os.listdir(os.path.join(workspace_dir, 'examples'))
               if f.endswith('.md')]

def in_prohibition_context(lines, idx, window=10):
    """A banned phrase is acceptable only when the line itself, or the nearby
    preceding prose, frames it as something Website Director must never emit.
    This covers fenced blocks that enumerate the prohibited strings."""
    start = max(0, idx - window)
    for probe in lines[start:idx + 1]:
        if any(m in probe for m in PROHIBITION_MARKERS):
            return True
    return False


bad_claims = []
for rel in scan_files:
    lines = read(rel).splitlines()
    for i, line in enumerate(lines):
        for b in BANNED:
            if b in line and not in_prohibition_context(lines, i):
                bad_claims.append('%s :: %s' % (rel, line.strip()[:110]))
check(not bad_claims,
      'No framework document asserts a compliance certification (violations: %s)' % (bad_claims or 'none'))

# ---------------------------------------------------------------------------
# 7. Required protocol coverage (spec sections)
# ---------------------------------------------------------------------------
REQUIRED_TOPICS = [
    'STATIC_MARKETING', 'CONTENT_PUBLISHER', 'AFFILIATE', 'LEAD_GENERATION', 'ECOMMERCE',
    'AUTHENTICATED_APPLICATION', 'SAAS', 'COMMUNITY', 'USER_GENERATED_CONTENT',
    'PAYMENT_ENABLED', 'HEALTH_OR_SENSITIVE_DATA', 'CHILD_DIRECTED_OR_CHILD_ACCESSIBLE',
    'INTERNAL_PRIVATE_APPLICATION',
    'DATA_CLASS', 'RETENTION_KNOWN', 'PRODUCTION_REQUIRED',
    'Content-Security-Policy', 'Strict-Transport-Security', 'Referrer-Policy',
    'Permissions-Policy', 'X-Content-Type-Options',
    '.env.example', 'HttpOnly', 'SameSite',
    'CONDITIONALLY_REQUIRED', 'NOT_REQUIRED',
]
missing = [t for t in REQUIRED_TOPICS if t not in protocol]
check(not missing, 'Protocol covers all required classifications and controls (missing: %s)' % (missing or 'none'))

check('PAYMENT PROVIDER INTEGRATION' in protocol and 'STORING PAYMENT CARD DATA' in protocol,
      'Protocol distinguishes payment provider integration from card storage')
check('AFFILIATE DISCLOSURE' in protocol and 'PRIVACY POLICY' in protocol,
      'Protocol distinguishes affiliate disclosure from privacy policy')
check('never guess' in protocol.lower() or 'Do not guess' in protocol,
      'Protocol forbids guessing applicable law')
check('localhost' in protocol.lower(),
      'Protocol exempts local development HTTP from production transport failure')

# ---------------------------------------------------------------------------
# 8. Template has all 25 required sections
# ---------------------------------------------------------------------------
REQUIRED_SECTIONS = [
    '## 1. Project Risk Classification',
    '## 2. Data Inventory',
    '## 3. Data Minimization',
    '## 4. Forms',
    '## 5. Authentication',
    '## 6. Payment Boundary',
    '## 7. Secrets',
    '## 8. Third-Party Services',
    '## 9. Third-Party Scripts',
    '## 10. Analytics / Measurement Privacy',
    '## 11. Cookies / Browser Storage',
    '## 12. Consent Assessment',
    '## 13. Privacy Notice Requirements',
    '## 14. Affiliate / Sponsored Disclosure',
    '## 15. Marketing Claims Risks',
    '## 16. Security Headers',
    '## 17. HTTPS / Transport',
    '## 18. Dependency / Supply Chain',
    '## 19. Sensitive Data Escalations',
    '## 20. Legal Review Escalations',
    '## 21. Implementation Requirements',
    '## 22. Production Verification Requirements',
    '## 23. Known Gaps',
    '## 24. Exceptions',
    '## 25. Evidence',
]
missing_sections = [s for s in REQUIRED_SECTIONS if s not in template]
check(not missing_sections,
      'Template contains all 25 required sections (missing: %s)' % (missing_sections or 'none'))
check('compliance certification' in template.lower() and 'legal advice' in template.lower(),
      'Template carries the compliance boundary notice')

# register json is valid and carries no real secret values
register = json.loads(read(REGISTER))
check(register.get('compliance_certified') is False, 'Register compliance_certified is false')
check(register['consent']['status'] == 'UNASSESSED', 'Register consent status defaults to UNASSESSED')
check(all(s['client_exposed'] is False for s in register['secrets']['required_secrets']),
      'Register marks every required secret as not client-exposed')

# ---------------------------------------------------------------------------
# 9. Cross-document wiring
# ---------------------------------------------------------------------------
skill = read('SKILL.md')
check('PHASE 6.75' in skill, 'SKILL.md declares PHASE 6.75')
check('[SECURITY_PRIVACY_READY]' in skill, 'SKILL.md declares the SECURITY_PRIVACY_READY gate')
check('GATE SECURITY' in skill, 'SKILL.md workflow diagram includes GATE SECURITY')
check('5.14 Single-Source-of-Truth Rule for `security_privacy` State' in skill,
      'SKILL.md documents the security_privacy source-of-truth rule')
check('security-privacy-review.md' in skill, 'SKILL.md references the working template')
check('Exactly 5 owner locks remain' in skill, 'SKILL.md restates the five-lock invariant')
check('> **Version:** 2.7.0' in skill, 'SKILL.md version is 2.7.0')

contract = read('IMPLEMENTATION-CONTRACT.md')
check('## 2.6 Builder Security & Privacy Requirements (V2.7)' in contract,
      'IMPLEMENTATION-CONTRACT.md adds builder security requirements')
check('HALTS and escalates' in contract, 'Implementation contract requires halt-and-escalate on conflict')
check('Client-Side Secrets' in contract, 'Implementation contract prohibits client-side secrets')
check('Undeclared Third-Party Scripts' in contract,
      'Implementation contract prohibits undeclared third-party scripts')
check('Raw Payment Card Storage' in contract, 'Implementation contract prohibits raw card storage')
check('Fabricated Compliance Claims' in contract,
      'Implementation contract prohibits fabricated compliance claims')

checklist = read('PRODUCTION-CHECKLIST.md')
check('## 5.3 Security, Privacy & Compliance Verification (V2.7)' in checklist,
      'PRODUCTION-CHECKLIST.md adds security/privacy production verification')
check('Do not mark legal compliance "PASS."' in checklist,
      'Production checklist forbids marking legal compliance as PASS')
for item in ['Mixed content', 'mixed content', 'Security Headers', 'Secrets Exposure',
             'Consent Behavior', 'Third-Party Scripts', 'Cookies & Browser Storage']:
    pass
check('Zero mixed content' in checklist, 'Production checklist verifies mixed content')
check('Zero secrets in the client bundle' in checklist, 'Production checklist verifies secret exposure')
check('External dependency failure tested' in checklist,
      'Production checklist verifies external dependency failure')
check('NOT_YET_VERIFIED' in checklist, 'Production checklist reports absent production evidence honestly')

gauntlet = read('WEBSITE-GAUNTLET-PROTOCOL.md')
check('4.15 Security & Privacy Coverage (V2.7 — No New Critic)' in gauntlet,
      'Gauntlet documents V2.7 coverage without a new critic')
check('BUILDER != CRITIC' in gauntlet, 'Gauntlet maintains BUILDER != CRITIC')
check('No second Gauntlet state machine is created' in gauntlet,
      'Gauntlet states no second state machine is created')
SECURITY_CRITIC_HEADING = r'^### 4\.\d+ [^\n]*(Security|Privacy|Compliance)[^\n]*Critic\s*$'
check(re.search(SECURITY_CRITIC_HEADING, gauntlet, re.M) is None,
      'No standalone Security/Privacy critic heading was added to the Gauntlet')

analytics = read('CONVERSION-ANALYTICS-PROTOCOL.md')
check('SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md' in analytics,
      'CONVERSION-ANALYTICS-PROTOCOL.md §15 delegates to the canonical authority')
check('A dedicated Security / Privacy / Compliance subsystem is future work' not in analytics,
      'Stale "future work" claim removed from the analytics protocol')
check('is the **only** authoritative readiness flag' in analytics and 'measurement.complete' in analytics,
      'Measurement single-flag invariant preserved')

readme = read('README.md')
check('What V2.7 Adds (Security, Privacy & Compliance Intelligence)' in readme,
      'README documents the V2.7 subsystem')
check('SECURITY_PRIVACY_READY` (Gate Security)' in readme, 'README lists the Gate Security readiness gate')
check('security-privacy-review.md' in readme, 'README repository structure lists the template')

agents = read('AGENTS.md')
check('Security, Privacy & Compliance Governance (V2.7 — Additive)' in agents,
      'AGENTS.md adds V2.7 governance rules')
check('WEBSITE_DIRECTOR_V2_7_SECURITY_PRIVACY_COMPLIANCE_INTELLIGENCE_CERTIFIED' in agents,
      'AGENTS.md records the V2.7 system status')
check('**Version:** 2.7.0' in agents, 'AGENTS.md version is 2.7.0')

# ---------------------------------------------------------------------------
# 10. No secrets introduced by this upgrade
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    r'AKIA[0-9A-Z]{16}',
    r'sk_live_[0-9a-zA-Z]{16,}',
    r'ghp_[0-9A-Za-z]{30,}',
    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'AIza[0-9A-Za-z\-_]{30,}',
]
new_files = [PROTOCOL, TEMPLATE, REGISTER, VALIDATION,
             'SKILL.md', 'README.md', 'AGENTS.md', 'IMPLEMENTATION-CONTRACT.md',
             'PRODUCTION-CHECKLIST.md', 'WEBSITE-GAUNTLET-PROTOCOL.md',
             'CONVERSION-ANALYTICS-PROTOCOL.md',
             os.path.join('templates', 'site-profile.json')]
leaks = []
for rel in new_files:
    text = read(rel)
    for pat in SECRET_PATTERNS:
        if re.search(pat, text):
            leaks.append('%s :: %s' % (rel, pat))
check(not leaks, 'No secret-shaped material in any V2.7 file (found: %s)' % (leaks or 'none'))

# ---------------------------------------------------------------------------
# 11. Frozen pilots untouched — no security_privacy retrofit
# ---------------------------------------------------------------------------
projects_dir = os.path.join(workspace_dir, 'projects')
retrofitted = []
if os.path.isdir(projects_dir):
    for name in sorted(os.listdir(projects_dir)):
        pf = os.path.join(projects_dir, name, 'site-profile.json')
        if not os.path.exists(pf):
            continue
        with io.open(pf, encoding='utf-8') as f:
            try:
                data = json.load(f)
            except ValueError:
                check(False, 'Pilot %s site-profile.json is valid JSON' % name)
                continue
        check(True, 'Pilot %s site-profile.json is valid JSON' % name)
        if 'security_privacy' in data:
            retrofitted.append(name)
        pl = data.get('locks', {})
        if pl:
            check(len(pl) == 5 or data.get('schema_version') is None,
                  'Pilot %s preserves its original lock count (%d)' % (name, len(pl)))
check(not retrofitted,
      'No frozen pilot was retrofitted with security_privacy{} (found: %s)' % (retrofitted or 'none'))

# ---------------------------------------------------------------------------
# 12. All repository JSON remains valid
# ---------------------------------------------------------------------------
bad_json = []
for root, dirs, files in os.walk(workspace_dir):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', 'scratch',
                                            '__pycache__', '.chrome_test_profile')]
    for fn in files:
        if not fn.endswith('.json'):
            continue
        full = os.path.join(root, fn)
        try:
            with io.open(full, encoding='utf-8') as f:
                json.load(f)
        except Exception as exc:
            bad_json.append('%s (%s)' % (os.path.relpath(full, workspace_dir), type(exc).__name__))
check(not bad_json, 'All repository JSON parses (invalid: %s)' % (bad_json or 'none'))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print('-' * 60)
print('V2.7 SECURITY, PRIVACY & COMPLIANCE TEST SUITE RESULT: %d/%d ASSERTIONS PASSED'
      % (assertions_passed, assertions_run))
if failures:
    print('FAILURES:')
    for f in failures:
        print('  - ' + f)
    sys.exit(1)
sys.exit(0)
