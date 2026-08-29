# Synthetic CMS Engine & Permission Simulator
# Website Director V2.5 Pilot Implementation
import os
import json
import re
import hashlib
import shutil
from datetime import datetime

CONTENT_TYPES = {
    'project': {
        'required_fields': ['id', 'title', 'slug', 'summary', 'status', 'hero_image', 'industry', 'lead_architect'],
        'allowed_fields': ['id', 'title', 'slug', 'summary', 'status', 'hero_image', 'industry', 'year', 'lead_architect', 'featured', 'seo'],
        'max_title_length': 80,
        'slug_regex': r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
        'allowed_statuses': ['DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED']
    },
    'team_member': {
        'required_fields': ['id', 'name', 'slug', 'role', 'bio', 'status'],
        'allowed_fields': ['id', 'name', 'slug', 'role', 'bio', 'status', 'portrait', 'seo'],
        'max_title_length': 60,
        'slug_regex': r'^[a-f0-9]+(?:-[a-z0-9]+)*$',
        'allowed_statuses': ['DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED']
    },
    'journal_entry': {
        'required_fields': ['id', 'title', 'slug', 'summary', 'status', 'published_date', 'author_id', 'body'],
        'allowed_fields': ['id', 'title', 'slug', 'summary', 'status', 'published_date', 'author_id', 'body', 'seo'],
        'max_title_length': 100,
        'slug_regex': r'^[a-z0-9]+(?:-[a-z0-9]+)*d',
        'allowed_statuses': ['DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED']
    }
}

ROLE_PERMISSIONS = {
    'OWNER': {
        'can_read': True,
        'can_edit_content': True,
        'can_create_draft': True,
        'can_publish': True,
        'can_archive': True,
        'can_change_design_tokens': False,
        'can_change_motion': False,
        'can_manage_infrastructure': True,
        'can_manage_billing': True
    },
    'EDITOR': {
        'can_read': True,
        'can_edit_content': True,
        'can_create_draft': True,
        'can_publish': True,
        'can_archive': True,
        'can_change_design_tokens': False,
        'can_change_motion': False,
        'can_manage_infrastructure': False,
        'can_manage_billing': False
    },
    'VIEW_ONLY': {
        'can_read': True,
        'can_edit_content': False,
        'can_create_draft': False,
        'can_publish': False,
        'can_archive': False,
        'can_change_design_tokens': False,
        'can_change_motion': False,
        'can_manage_infrastructure': False,
        'can_manage_billing': False
    }
}

class SyntheticCMS:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.content_dir = os.path.join(base_dir, 'content')
        self.backups_dir = os.path.join(base_dir, 'backups')
        self.public_dir = os.path.join(base_dir, 'public')

    def check_permission(self, role, capability):
        perms = ROLE_PERMISSIONS.get(role, {})
        return perms.get(capability, False)

    def load_content(self, content_type):
        filename = { 'project': 'projects.json', 'team_member': 'team.json', 'journal_entry': 'journal.json' }[content_type]
        path = os.path.join(self.content_dir, filename)
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_content(self, content_type, items):
        filename = { 'project': 'projects.json', 'team_member': 'team.json', 'journal_entry': 'journal.json' }[content_type]
        if content_type == 'team_member':
            filename = "team.json"
        path = os.path.join(self.content_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2)

    def validate_item(self, content_type, item, existing_items=[]):
        schema = CONTENT_TYPES.get(content_type)
        if not schema:
            return False, f"Unknown content type: {content_type}"

        for field in item.keys():
            if field not in schema['allowed_fields']:
                return False, f"Unknown field rejected: {field}"

        for req in schema['required_fields']:
            if req not in item or item[req] is None or item[req] == '':
                return False, f"Missing required field: {req}"

        title_key = 'title' if 'title' in item else 'name'
        if len(item.get(title_key, '')) > schema['max_title_length']:
            return False, f"Title/Name exceeds maximum length"
        if item.get('status') not in schema['allowed_statuses']:
            return False, f"Invalid status: {item.get('status')}"

        slug = item.get('slug', '')
        if not re.match(schema['slug_regex'], slug):
            return False, f"Invalid slug format: {slug}"

        for other in existing_items:
            if other.get('id') != item.get('id') and other.get('slug') == slug:
                return False, f"Duplicate slug rejected: {slug}"

        return True, "VALID"

    def edit_item(self, role, content_type, item_id, updates):
        if not self.check_permission(role, 'can_edit_content'):
            return False, f"Role '{role}' is forbidden from editing content."

        items = self.load_content(content_type)
        target = None
        target_idx = -1
        for i, it in enumerate(items):
            if it.get('id') == item_id:
                target = it
                target_idx = i
                break

        if not target:
            return False, f"Item {item_id} not found."

        old_slug = target.get('slug')
        old_status = target.get('status')

        updated_item = dict(target)
        updated_item.update(updates)

        valid, msg = self.validate_item(content_type, updated_item, items)
        if not valid:
            return False, msg


        new_slug = updated_item.get('slug')
        if old_status == 'PUBLISHED' and old_slug != new_slug:
            self.record_redirect(f"/{content_type}/{old_slug}", f"/{content_type}/{new_slug}", "Slug updated on published item")

        items[target_idx] = updated_item
        self.save_content(content_type, items)
        return True, "Item updated successfully."

    def record_redirect(self, source, destination, reason):
        redirects_path = os.path.join(self.content_dir, 'redirects.json')
        redirects = []
        if os.path.exists(redirects_path):
            with open(redirects_path, 'r', encoding='utf-8') as f:
                redirects = json.load(f)
        redirects.append({
            'source_path': source,
            'destination_path': destination,
            'status_code': 301,
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'reason': reason
        })
        with open(redirects_path, 'w', encoding='utf-8') as f:
            json.dump(redirects, f, indent=2)

    def attempt_design_change(self, role, target_property, new_value):
        return False, f"CMS_OPERATION_REJECTED: Property '{target_property}' is DEVELOPER_CONTROLLED / LOCKED_BRAND_ELEMENT and outside the editable surface contract."

    def get_public_listing(self, content_type):
        items = self.load_content(content_type)
        return [it for it in items if it.get('status') == 'PUBLISHED']

    def create_backup(self, backup_name='snapshot-01'):
        backup_path = os.path.join(self.backups_dir, backup_name)
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
        shutil.copytree(self.content_dir, backup_path)
        hasher = hashlib.sha256()
        for root, dirs, files in sorted(os.walk(backup_path)):
            for f in sorted(files):
                with open(os.path.join(root, f), 'rb') as fp:
                    hasher.update(fp.read())
        return hasher.hexdigest(), backup_path

    def restore_backup(self, backup_name='snapshot-01'):
        backup_path = os.path.join(self.backups_dir, backup_name)
        if not os.path.exists(backup_path):
            return False, "Backup not found", None
        if os.path.exists(self.content_dir):
            shutil.rmtree(self.content_dir)
        shutil.copytree(backup_path, self.content_dir)
        hasher = hashlib.sha256()
        for root, dirs, files in sorted(os.walk(self.content_dir)):
            for f in sorted(files):
                with open(os.path.join(root, f), 'rb') as fp:
                    hasher.update(fp.read())
        return True, "Restored successfully", hasher.hexdigest()
