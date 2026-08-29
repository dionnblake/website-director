# MORROW & VALE - CMS CONTENT MODEL SPECIFICATION

> **Technical Content Schemas & Field Validation Standards**  
> **Schema Version:** 2.5.0  

---

## 1. Content Types

### Type 1: `project`
- **Purpose:** Built architectural works and industrial design case studies.
- **Required Fields:** `id`, `title`, `slug`, `summary`, `status`, `hero_image`, `industry`, `lead_architect`.
- **Validation Rules:**
  - `title`: String, max length 80 characters.
  - `slug`: Regex ^{[a-z0-9]+}(?:-[a-z0-9]+)*$, must be unique across projects.
  - `status`: Enum ['DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED'].
  - `hero_image.aspect_ratio``: Required 16:9.
  - `hero_image.min_width`: 1920.

### Type 2: `team_member`
- **Purpose:** Studio principals, associates, and design leadership.
- **Required Fields:** `id`, `name`, `slug`, `role`, `bio`, `status`.
- **Validation Rules:**
  - `name`: String, max length 60 characters.
  - `slug`: Regex ^{[a-z0-9]+}(?:-[a-z0-9]+)*$, unique.
  - `status`: Enum ['DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED'].

### Type 3: `journal_entry`
- **Purpose:** Essays, architectural critiques, and monographs.
- **Required Fields:** `id`, `title`, `slug`, `summary`, `status`, `published_date`, `author_id`, `body`.
- **Validation Rules:**
  - `title`: String, max length 100 characters.
  - `published_date`: ISO 8601 Date (YYYY-MM-DD).
  - `author_id`: Must reference valid `team_member.id`.
  - `status`: Enum ['DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED'].
