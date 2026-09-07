"""R2: Does an owner cinematic requirement survive an omitted motion block?"""
import sys, os, json, types
REPRO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPRO); sys.path.insert(0, os.path.join(REPRO, "browser-qa"))
from assertions import catalog

class Obs:
    def __init__(self, raw=None):
        self.route="/index.html"; self.viewport=1440; self.browser="chromium"
        self.engine="playwright"; self.raw = raw or {}
        self.motion_observations = self.raw.get("motion_observations", [])

ASN = json.load(open(os.environ["ASN_MANIFEST"]))
print("=== ASN production manifest blocks present ===")
for k in ("owner_intent","motion","visual_evidence","runtime_observations","observations","brand_implementation"):
    print("   %-22s %s" % (k, "PRESENT" if k in ASN else "ABSENT"))
print()

obs = Obs({"engine_identity":"REAL_BROWSER","rendered_colors":[{"role":"primary","hex":"#1a1a1a"}]})

print("=== 1. ACTUAL ASN manifest (as shipped) ===")
print("   check_motion       ->", catalog.check_motion(obs, ASN))
print("   check_brand_tokens ->", catalog.check_brand_tokens(obs, ASN))
print()

# Owner declares MOTION_LEVEL_3 cinematic, but plan omits the motion block.
owner = {"MOTION": {"OWNER_REQUIRED_LEVEL": "MOTION_LEVEL_3",
                    "OWNER_STATED": True, "EXPERIENCE": "CINEMATIC"},
         "BRAND": {"PRIMARY":"ASN_NAVY","ACCENT":"ASN_YELLOW"}}
plan2 = dict(ASN); plan2["owner_intent"] = owner
print("=== 2. Owner intent present (MOTION_LEVEL_3) but motion block omitted ===")
r = catalog.check_motion(obs, plan2)
print("   check_motion       ->", r)
b = catalog.check_brand_tokens(obs, plan2)
print("   check_brand_tokens ->", "None" if b is None else b.verdict if hasattr(b,'verdict') else b)
print()

print("=== 3. Control: motion block explicitly required ===")
plan3 = dict(plan2); plan3["motion"] = {"required": True}
r3 = catalog.check_motion(obs, plan3)
print("   check_motion -> %d finding(s)" % (len(r3) if r3 else 0))
for f in (r3 or []): print("      ", f.check_id, f.verdict, "|", f.detail)
print()
print("VERDICT R2: case1 motion=%s brand=%s | case2 motion=%s (owner L3 IGNORED)" % (
    catalog.check_motion(obs,ASN), catalog.check_brand_tokens(obs,ASN), r))
