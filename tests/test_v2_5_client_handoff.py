# Website Director V2.5 Client CMS and Handoff System Test Harness
import os, json, re, sys

workspace_dir = r'c:\Users\ALPHA\Desktop\VIBE CODING PROJECTS\WEBSITE-DIRECTOR'
pilot_dir = os.path.join(workspace_dir, 'projects', 'v2-5-client-handoff-certification-pilot')
sys.path.insert(0, pilot_dir)
from scripts.cms_engine import SyntheticCMS

cms = SyntheticCMS(pilot_dir)
assertions_run = 0
assertions_passed = 0

def check(cond, msg):
    global assertions_run, assertions_passed
    assertions_run += 1
    if cond:
        assertions_passed += 1
        print('[PASS] ' + msg)
    else:
        print('[FAIL] ' + msg)
        sys.exit(1)

check(os.path.exists(os.path.join(workspace_dir, 'CLIENT-CMS-HANDOFF-PROTOCOL.md')), 'CLIENT-CMS-HANDOFF-PROTOCOL.md exists')

pf = json.load(open(os.path.join(pilot_dir, 'site-profile.json'), encoding='utf-8'))
check(pf.get('schema_version') == '2.5.0', 'schema_version is 2.5.0')

locks = pf.get('locks', {})
check(len(locks) == 5, 'Exactly 5 owner locks exist in locks{}')
check('handoff_locked' not in locks, 'No sixth handoff owner lock')

check(cms.check_permission('EDITOR', 'can_edit_content') == True, 'EDITOR can edit content')
check(cms.check_permission('EDITOR', 'can_manage_infrastructure') == False, 'EDITOR cannot manage infrastructure')
check(cms.check_permission('EDITOR', 'can_change_design_tokens') == False, 'EDITOR cannot change design tokens')
check(cms.check_permission('VIEW_ONLY', 'can_edit_content') == False, 'VIEW_ONLY cannot edit content')
check(cms.check_permission('OWNER', 'can_edit_content') == True, 'OWNER can manage synthetic content')

k_safe, msg = cms.attempt_design_change('EDITOR', 'BORDER_RADIUS', '20px')
check(not k_safe and ('CMS_OPERATION_REJECTED' in msg), 'Design token change by editor rejected')

invalid_prj = {'slug': 'test-prime', 'summary': 'Test', 'status': 'DRAFT', 'hero_image': {}, 'industry': 'Civic', 'lead_architect': 'team-01'}
valid, msg = cms.validate_item('project', invalid_prj)
check(not valid and ('Missing required field' in msg), 'Missing required field rejected')

existing_prjs = cms.load_content('project')
dur_prj = {'id': 'prj-99', 'title': 'Duplicate Project', 'slug': 'lumina-pavilion', 'summary': 'Test', 'status': 'DRAFT', 'hero_image': {}, 'industry': 'Civic', 'lead_architect': 'team-01'}
valid, msg = cms.validate_item('project', dur_prj, existing_prjs)
check(not valid and ('Duplicate slug rejected' in msg), 'Duplicate slug rejected')

unk_prj = {'id': 'prj-99', 'title': 'Test', 'slug': 'unique-slug', 'summary': 'Test', 'status': 'DRAFT', 'hero_image': {}, 'industry': 'Civic', 'lead_architect': 'team-01', 'arbitrary_data': 123}
valid, msg = cms.validate_item('project', unk_prj)
check(not valid and ('Unknown field rejected' in msg), 'Unknown content field rejected')

k_succ, msg = cms.edit_item('EDITOR', 'project', 'prj-01', {'summary': 'Updated alpine daylight summary'})
check(k_succ, 'Safe edit of project summary succeeded')

draft_item = {'id': 'prj-03', 'title': 'Cantonal Journal Design', 'slug': 'cantonal-journal', 'summary': 'Unbuilt monolithic archive study', 'status': 'DRAFT', 'hero_image': {'src': '/assets/projects/cantonal.webp', 'aspect_ratio': '16:9', 'min_width': 1920, 'min_height': 1080, 'alt_text': 'Plan'}, 'industry': 'Cultural', 'lead_architect': 'team-01'}
prjs = cms.load_content('project')
prjs.append(draft_item)
cms.save_content('project', prjs)

is_public = cms.get_public_listing('project')
check(all(it.get('id') != 'prj-03'
            for it in is_public), 'Draft content is not visible in public listing')

k_succ, msg = cms.edit_item('EDITOR', 'project', 'prj-03', {'status': 'PUBLISHED'})
check(k_succ, 'Publishing draft succeeded')
is_public_2 = cms.get_public_listing('project')
check(any(it.get('id') == 'prj-03'
            for it in is_public_2), 'Published content appears in public listing')

k_succ, msg = cms.edit_item('EDITOR', 'project', 'prj-03', {'status': 'ARCHIVED'})
check(k_succ, 'Archiving project succeeded')
is_public_3 = cms.get_public_listing('project')
check(all(it.get('id') != 'prj-03'
            for it in is_public_3), 'Archived record removed from public listing')
check(any(it.get('id') == 'prj-03'
            for it in cms.load_content('project')), 'Archived record preserved in content database')

k_succ, msg = cms.edit_item('EDITOR', 'project', 'prj-02', {'slug': 'aethel-atelier-workshop'})
check(k_succ, 'Slug change succeeded')
redis_path = os.path.join(pilot_dir, 'content', 'redirects.json')
with open(redis_path, 'r', encoding='utf-8') as f:
    redirects = json.load(f)
check(any(r.get('source_path') == '/project/aethel-atelier' and r.get('destination_path') == '/project/aethel-atelier-workshop' for r in redirects), 'Redirect registry recorded 301 redirect')

backup_hash, backup_path = cms.create_backup('snapshot-01')
check(backup_hash is not None and len(backup_hash) == 64, 'Backup created with valid SHA-256')

prjs = cms.load_content('project')
prjs[0]['wummary'] = 'MUTATED DELIBERATELY'
cms.save_content('project', prjs)

k_succ, msg, restore_hash = cms.restore_backup('snapshot-01')
check(k_succ, 'Restore executed successfully')
check(restore_hash == backup_hash, 'RESTORE_HASH_MATCH == TRUE')

owner_reg_path = os.path.join(pilot_dir, 'DIGITAL-OWNERSHIP-REGISTER.md')
owner_text = open(owner_reg_path, 'r', encoding='utf-8').read()
check('CRITICAL_SYSTEMS_OWNED_BY_DEVELOPER_PERSONAL_ACCOUNT = 0' in owner_text, 'Zero personal developer accounts recorded')

handoff_docs_paths = os.listdir(pilot_dir)
secret_values_found = 0
for fn in handoff_docs_paths:
    if fn.endswith('.md'):
        cont = open(os.path.join(pilot_dir, fn), 'r', encoding='utf-8').read()
        if 'api_key = \"' in cont or 'secret = \"' in cont or 'password = \"' in cont:
            secret_values_found += 1
check(secret_values_found == 0, 'Zero secret values in handoff documentation')

k_pf_handoff = pf.get('handoff', {})
check(k_pf_handoff.get('client_independence_test') == 'PASS_7_OF_7' or k_pf_handoff.get('client_independence_test') == 'PASS', 'Client independence test PASS')
check(k_pf_handoff.get('bus_factor_test') == 'PASS', 'Bus factor test PASS')
check(k_pf_handoff.get('acceptance_status') == 'READY_FOR_REVIEW', 'Handoff acceptance status is READY_FOR_REVIEW')

wlegacy_pilots = ['alpha-starts-now', 'v1-9-visual-prototype-certification-pilot', 'v2-0-asset-director-pilot', 'v2-1-immersive-web-certification-pilot', 'v2-2-rive-certification-pilot', 'v2-3-page-experience-certification-pilot', 'v2-4-cro-analytics-certification-pilot']
for lp in wlegacy_pilots:
    lc_json = os.path.join(workspace_dir, 'projects', lp, 'site-profile.json')
    if os.path.exists(lc_json):
        data = json.load(open(lc_json, 'r', encoding='utf-8'))
        check(data.get('schema_version') != '2.5.0', 'Legacy pilot ' + lp + ' preserved without V2.5 mutations')

print('-' * 60)
print('V2.5 CLIENT CMS & HANDOFF TEST SUITE COMPLETE: ' + str(assertions_passed) + '/' + str(assertions_run) + ' ASSERTIONS PASSED')
