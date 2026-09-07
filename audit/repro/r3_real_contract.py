"""R3: Real ASN owner contract vs real built-site rendered palette."""
import sys, os, json
REPRO=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,REPRO); sys.path.insert(0,os.path.join(REPRO,"browser-qa"))
from framework_validation.owner_intent import (validate_brand_tokens,
    resolve_motion_requirement, audit_owner_requirement_compliance)
from assertions import catalog

contract = json.load(open(os.environ["CONTRACT"]))

# Rendered roles as actually built (site.css :root + body background)
rendered = [
  {"role":"PAGE_BACKGROUND","hex":"#f4efe6","name":"paper cream"},
  {"role":"PRIMARY","hex":"#0b1830","name":"navy"},
  {"role":"ACCENT","hex":"#ffc700","name":"yellow"},
  {"role":"TEXT","hex":"#071124","name":"ink"},
]
impl = {"primary":"#0b1830","accent":"#ffc700","background":"#f4efe6"}

print("=== validate_brand_tokens (real contract vs real build) ===")
res = validate_brand_tokens(contract, impl, {"rendered_colors": rendered})
print(json.dumps(res, indent=2)[:1500])
print()
print("=== resolve_motion_requirement (real contract) ===")
mot = resolve_motion_requirement(contract, heuristic_level="MOTION_LEVEL_1")
print(json.dumps(mot, indent=2)[:900])
print()
print("=== Would the shipped ASN manifest ever reach these? ===")
ASN = json.load(open(os.environ["ASN_MANIFEST"]))
print("   plan['owner_intent'] present:", "owner_intent" in ASN)
print("   -> check_brand_tokens gate  :", "RUNS" if "owner_intent" in ASN else "SILENT SKIP (returns None)")
print("   plan['motion'] present      :", "motion" in ASN)
print("   -> check_motion gate        :", "RUNS" if "motion" in ASN else "SILENT SKIP (returns None)")
