import os
import json
import re

def test_v2_5_1():
    passed = 0
    total = 0

    def check(condition, msg):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {msg}")
        else:
            print(f"[FAIL] {msg}")

    # 1. Authority Document
    check(os.path.exists("SIGNATURE-SCROLL-SPATIAL-CHOREOGRAPHY-LIBRARY.md"), "SIGNATURE-SCROLL-SPATIAL-CHOREOGRAPHY-LIBRARY.md exists")

    # 2. Registry parsing and pattern count
    reg_path = "templates/signature-interaction-registry.json"
    check(os.path.exists(reg_path), "templates/signature-interaction-registry.json exists")
    with open(reg_path, "r", encoding="utf-8") as f:
        reg = json.load(f)

    check(reg.get("schema_version") == "2.5.1", "Registry schema_version is 2.5.1")
    patterns = reg.get("patterns", [])
    check(len(patterns) >= 18, f"Pattern registry contains >= 18 patterns (actual: {len(patterns)})")
    
    # Check unique IDs and required fields
    p_ids = [p["pattern_id"] for p in patterns]
    check(len(p_ids) == len(set(p_ids)), "All pattern IDs are unique")

    req_fields = [
        "pattern_id", "pattern_name", "family", "description", "narrative_purpose",
        "best_for", "avoid_when", "primary_technique", "mobile_strategy",
        "reduced_motion_strategy", "accessibility_risk", "performance_risk",
        "novelty_level", "complexity_level", "content_requirements", "signature_potential"
    ]
    all_fields_ok = all(all(rf in p for rf in req_fields) for p in patterns)
    check(all_fields_ok, "All patterns have 100% required field compliance")

    # 3. Pilot site-profile validation
    pilot_profile_path = "projects/v2-5-1-signature-choreography-certification-pilot/site-profile.json"
    check(os.path.exists(pilot_profile_path), "Pilot site-profile.json exists")
    with open(pilot_profile_path, "r", encoding="utf-8") as f:
        pf = json.load(f)

    check(pf.get("schema_version") == "2.5.1", "Pilot schema_version is 2.5.1")
    locks = pf.get("locks", {})
    check(len(locks) == 5, "Exactly 5 owner locks in locks{}")
    check("signature_choreography_locked" not in locks, "No sixth signature owner lock created")

    sc = pf.get("signature_choreography", {})
    check(sc.get("primary_pattern") == "PINNED_HORIZONTAL_SCROLLYTELLING", "Primary pattern is PINNED_HORIZONTAL_SCROLLYTELLING")
    check(sc.get("supporting_pattern") == "SCROLL_DRIVEN_ASSEMBLY", "Supporting pattern is SCROLL_DRIVEN_ASSEMBLY")
    check(sc.get("interaction_level") == "2_FEATURE", "Interaction level is 2_FEATURE")
    check(sc.get("mobile_strategy") == "REFLOWED", "Mobile strategy is REFLOWED")

    # 4. Pilot Web Source & DOM structure
    html_path = "projects/v2-5-1-signature-choreography-certification-pilot/index.html"
    check(os.path.exists(html_path), "index.html exists")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    check('id="atelier-scrollytelling"' in html_content, "Pinned scrollytelling container present in DOM")
    check('id="chapter-01"' in html_content and 'id="chapter-05"' in html_content, "All 5 chapter panels present in DOM")
    check('id="assembly-container"' in html_content, "Scroll-driven assembly container present in DOM")
    check('id="capabilities"' in html_content, "Vertical capabilities section follows scrollytelling")

    # 5. CSS Responsive & Reduced Motion checks
    css_path = "projects/v2-5-1-signature-choreography-certification-pilot/css/style.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    check("@media (max-width: 768px)" in css_content and "width: 100%" in css_content, "Mobile reflow CSS media query present")
    check("@media (prefers-reduced-motion: reduce)" in css_content, "prefers-reduced-motion media query present")

    # 6. JS Script and Performance
    js_path = "projects/v2-5-1-signature-choreography-certification-pilot/js/main.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()
    check("ScrollTrigger" in js_content and "gsap.to" in js_content, "GSAP and ScrollTrigger properly invoked in JS")
    check("prefers-reduced-motion" in js_content, "Reduced-motion bypassed inside JS")

    # 7. Evidence ledger
    hashes_path = "projects/v2-5-1-signature-choreography-certification-pilot/evidence/source-hashes.json"
    check(os.path.exists(hashes_path), "Evidence source-hashes.json ledger exists")

    # 8. Historical Pilot Invariant Check
    historical_pilots = [
        "alpha-starts-now",
        "v1-9-visual-prototype-certification-pilot",
        "v2-0-asset-director-pilot",
        "v2-1-immersive-web-certification-pilot",
        "v2-2-rive-certification-pilot",
        "v2-3-page-experience-certification-pilot",
        "v2-4-cro-analytics-certification-pilot",
        "v2-5-client-handoff-certification-pilot"
    ]
    for hp in historical_pilots:
        hpp = os.path.join("projects", hp, "site-profile.json")
        if os.path.exists(hpp):
            with open(hpp, "r", encoding="utf-8") as f:
                h_pf = json.load(f)
            check("signature_choreography" not in h_pf or hp == "v2-5-1-signature-choreography-certification-pilot", f"Historical pilot {hp} unmutated by V2.5.1")

    print("-" * 60)
    print(f"V2.5.1 TEST SUITE RESULT: {passed}/{total} ASSERTIONS PASSED")
    return passed == total

if __name__ == "__main__":
    test_v2_5_1()
