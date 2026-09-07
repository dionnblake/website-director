"""R1: Do design-first HOMEPAGE surface names produce FULL_PAGE captures?"""
import sys, os, json
REPRO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPRO)
sys.path.insert(0, os.path.join(REPRO, "browser-qa"))
import runner
from framework_validation.design_first_flow import HOMEPAGE_REVIEW_SURFACES
from framework_validation.cinematic_inspiration import REQUIRED_RENDER_SURFACES

BASE = {"routes": [{"path": "/index.html", "name": "Home"}],
        "viewports": {"smoke": [1440]}, "browsers": {"smoke": ["chromium"]}}

def surfaces_of(jobs):
    return [(j.get("surface_id"), j.get("capture"), j.get("viewport"))
            for j in jobs if j.get("surface_id")]

print("HOMEPAGE_REVIEW_SURFACES =", HOMEPAGE_REVIEW_SURFACES)
print("REQUIRED_RENDER_SURFACES =", REQUIRED_RENDER_SURFACES)
print()

cases = [
  ("A. canonical cinematic names (strings)", list(REQUIRED_RENDER_SURFACES)),
  ("B. design-first homepage names (strings)", list(HOMEPAGE_REVIEW_SURFACES)),
  ("C. homepage names as explicit objects capture=FULL_PAGE",
     [{"surface_id": s, "capture": "FULL_PAGE"} for s in HOMEPAGE_REVIEW_SURFACES]),
]
results = {}
for label, surfaces in cases:
    plan = dict(BASE)
    plan["visual_evidence"] = {"required": True, "required_surfaces": surfaces}
    jobs = runner._matrix(plan, "smoke")
    got = surfaces_of(jobs)
    results[label] = got
    print(label)
    for sid, cap, vp in got:
        flag = "" if cap == "FULL_PAGE" else "   <-- VIEWPORT ONLY"
        print("   %-28s capture=%-9s viewport=%s%s" % (sid, cap, vp, flag))
    print()

b = results["B. design-first homepage names (strings)"]
viewport_only = [s for s, c, v in b if c != "FULL_PAGE"]
print("VERDICT R1:", "REPRODUCED - %d/%d design-first homepage surfaces captured VIEWPORT-only"
      % (len(viewport_only), len(b)) if viewport_only else "NOT REPRODUCED")
