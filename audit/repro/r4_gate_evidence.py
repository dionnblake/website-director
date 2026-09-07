"""R4: Can true flags hide invalid design evidence? Can fabricated receipts pass?"""
import sys, os, json
REPRO=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,REPRO)
from framework_validation import design_first_flow as dff
from framework_validation.cinematic_inspiration import validate_rendered_visual_evidence

APPROVAL = {"STATE_LOCATION":"VISUAL_PROTOTYPES_HOMEPAGE_VISUAL_APPROVED",
  "HOMEPAGE_VISUAL_APPROVED":True,"OWNER_APPROVED":True,"OWNER_ACTION":"APPROVE",
  "APPROVED_BY":"OWNER","REVIEWED":True,
  "RENDERED_SURFACES":["DESKTOP_FULL_HOMEPAGE","MOBILE_FULL_HOMEPAGE"]}  # bare strings, no receipts

print("=== C1: 7 flags TRUE + valid-shaped approval, design evidence never inspected ===")
gate = {k:True for k in ("BUSINESS_UNDERSTANDING_COMPLETE","OWNER_INTENT_CAPTURED",
  "REQUIRED_ASSETS_IDENTIFIED","REFERENCES_INTERPRETED","HOMEPAGE_RENDERED_AND_REVIEWED",
  "OWNER_APPROVAL_RECORDED","DESIGN_SYSTEM_DERIVED_AND_READY")}
gate["HOMEPAGE_APPROVAL"]=APPROVAL
r = dff.validate_production_gate(gate)
print("   validate_production_gate ->", r["status"], "| can_start_production:", r.get("can_start_production"))
print("   NOTE: RENDERED_SURFACES were bare strings - zero screenshot receipts supplied.")
print()
print("   Same run's REAL design evidence, if anyone had asked:")
rh = dff.validate_homepage_design("SHOWCASE", {"SECTIONS":{}, "LOWER_HALF_QUALITY":"GENERIC_FILLER","PROSE_ONLY":True})
print("     validate_homepage_design(garbage)            ->", rh["status"], [i["code"] for i in rh["issues"]][:3])
rd = dff.validate_design_system_derivation({"HOMEPAGE_SOURCE":"INVENTED_BY_AGENT"})
print("     validate_design_system_derivation(garbage)   ->", rd["status"], [i["code"] for i in rd["issues"]][:3])
print("   >> Gate passed anyway:", r["status"]=="PASS")
print()

print("=== C2: fabricated screenshot receipts (no file on disk, digest = 64 zeros) ===")
fake = {"screenshots":[{"surface_id":s,"actual_rendered":True,"engine_identity":"REAL_BROWSER",
   "screenshot_path":"/nonexistent/%s.png"%s.lower(),"screenshot_sha256":"0"*64}
   for s in ("DESKTOP_FULL_PAGE","DESKTOP_HERO","DESKTOP_MID_PAGE","DESKTOP_PRIMARY_CONVERSION",
   "MOBILE_FULL_PAGE","MOBILE_HERO","MOBILE_NAV_OPEN","PRIMARY_INTERACTIVE_STATE","REDUCED_MOTION_STATE")]}
rv = validate_rendered_visual_evidence(fake)
print("   validate_rendered_visual_evidence ->", rv["status"], "| issues:", [i["code"] for i in rv["issues"]] or "NONE")
print("   any file actually on disk:", any(os.path.exists(s["screenshot_path"]) for s in fake["screenshots"]))
