"""Small provider-neutral CMS fixture used by the V2.5 handoff tests.

This is a disposable behavior fixture, not a copy of a historical website.
"""

import hashlib
import json
import os
import re
import shutil
from datetime import datetime


CONTENT_TYPES = {
    "project": {
        "required": ["id", "title", "slug", "summary", "status", "hero_image", "industry", "lead_architect"],
        "allowed": ["id", "title", "slug", "summary", "status", "hero_image", "industry", "year", "lead_architect", "featured", "seo"],
        "max_title": 80,
        "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    },
    "team_member": {
        "required": ["id", "name", "slug", "role", "bio", "status"],
        "allowed": ["id", "name", "slug", "role", "bio", "status", "portrait", "seo"],
        "max_title": 60,
        "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    },
    "journal_entry": {
        "required": ["id", "title", "slug", "summary", "status", "published_date", "author_id", "body"],
        "allowed": ["id", "title", "slug", "summary", "status", "published_date", "author_id", "body", "seo"],
        "max_title": 100,
        "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    },
}

ROLE_PERMISSIONS = {
    "OWNER": {"can_edit_content": True, "can_publish": True, "can_archive": True, "can_manage_infrastructure": True},
    "EDITOR": {"can_edit_content": True, "can_publish": True, "can_archive": True, "can_manage_infrastructure": False},
    "VIEW_ONLY": {"can_edit_content": False, "can_publish": False, "can_archive": False, "can_manage_infrastructure": False},
}


class SyntheticCMS:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.content_dir = os.path.join(base_dir, "content")
        self.backups_dir = os.path.join(base_dir, "backups")

    def _path(self, content_type):
        return os.path.join(self.content_dir, {
            "project": "projects.json",
            "team_member": "team.json",
            "journal_entry": "journal.json",
        }[content_type])

    def check_permission(self, role, capability):
        return ROLE_PERMISSIONS.get(role, {}).get(capability, False)

    def load_content(self, content_type):
        path = self._path(content_type)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def save_content(self, content_type, items):
        os.makedirs(self.content_dir, exist_ok=True)
        with open(self._path(content_type), "w", encoding="utf-8") as handle:
            json.dump(items, handle, indent=2)

    def validate_item(self, content_type, item, existing_items=None):
        schema = CONTENT_TYPES.get(content_type)
        if schema is None:
            return False, "Unknown content type"
        existing_items = existing_items or []
        for field in item:
            if field not in schema["allowed"]:
                return False, "Unknown field rejected: " + field
        for field in schema["required"]:
            if item.get(field) in (None, ""):
                return False, "Missing required field: " + field
        title = item.get("title", item.get("name", ""))
        if len(title) > schema["max_title"]:
            return False, "Title/Name exceeds maximum length"
        if item.get("status") not in ("DRAFT", "IN_REVIEW", "APPROVED", "PUBLISHED", "ARCHIVED"):
            return False, "Invalid status"
        if not re.match(schema["slug"], item.get("slug", "")):
            return False, "Invalid slug format"
        if any(other.get("id") != item.get("id") and other.get("slug") == item.get("slug") for other in existing_items):
            return False, "Duplicate slug rejected: " + item["slug"]
        return True, "VALID"

    def edit_item(self, role, content_type, item_id, updates):
        if not self.check_permission(role, "can_edit_content"):
            return False, "Role is forbidden from editing content."
        items = self.load_content(content_type)
        index = next((i for i, item in enumerate(items) if item.get("id") == item_id), -1)
        if index < 0:
            return False, "Item not found."
        old = items[index]
        updated = dict(old)
        updated.update(updates)
        valid, message = self.validate_item(content_type, updated, items)
        if not valid:
            return False, message
        if old.get("status") == "PUBLISHED" and old.get("slug") != updated.get("slug"):
            self.record_redirect("/{}/{}".format(content_type, old["slug"]), "/{}/{}".format(content_type, updated["slug"]), "Slug updated on published item")
        items[index] = updated
        self.save_content(content_type, items)
        return True, "Item updated successfully."

    def record_redirect(self, source, destination, reason):
        path = os.path.join(self.content_dir, "redirects.json")
        redirects = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                redirects = json.load(handle)
        redirects.append({"source_path": source, "destination_path": destination, "status_code": 301,
                          "created_at": datetime.utcnow().isoformat() + "Z", "reason": reason})
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(redirects, handle, indent=2)

    def attempt_design_change(self, role, target_property, new_value):
        return False, "CMS_OPERATION_REJECTED: developer-controlled locked brand element"

    def get_public_listing(self, content_type):
        return [item for item in self.load_content(content_type) if item.get("status") == "PUBLISHED"]

    def _digest(self, root):
        hasher = hashlib.sha256()
        for current, _, files in sorted(os.walk(root)):
            for name in sorted(files):
                with open(os.path.join(current, name), "rb") as handle:
                    hasher.update(handle.read())
        return hasher.hexdigest()

    def create_backup(self, backup_name="snapshot-01"):
        path = os.path.join(self.backups_dir, backup_name)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(self.backups_dir, exist_ok=True)
        shutil.copytree(self.content_dir, path)
        return self._digest(path), path

    def restore_backup(self, backup_name="snapshot-01"):
        backup = os.path.join(self.backups_dir, backup_name)
        if not os.path.exists(backup):
            return False, "Backup not found", None
        if os.path.exists(self.content_dir):
            shutil.rmtree(self.content_dir)
        shutil.copytree(backup, self.content_dir)
        return True, "Restored successfully", self._digest(self.content_dir)
