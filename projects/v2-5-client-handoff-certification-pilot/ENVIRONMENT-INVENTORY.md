# MORROW & VALE - ENVIRONMENT INVENTORY & CONFIGURATION

> **Environment Specifications & Configuration Variables**  
> **Security Rule:** Zero Secret Values in Documentation  

---

## 1. Environments

### LOCAL
- Testing, content authoring, and verification.
- URL: http://localhost:3000
- Deploy Owner: Individual Developer / Editor.

### PREVIEW
- Staging environment for draft preview.
- URL: https://preview.morrowvale-synthetic.ch
- Deploy Owner: Automated CI Pipeline on staging.

### PRODUCTION
- Publicly accessible client website.
- URL: https://www.morrowvale-synthetic.ch
- Deploy Owner: Automated CI Pipeline on main.

---

## 2. Environment Variables Inventory

| Variable Name | Purpose | Environments | Owner | Secret? | Rotation Policy |
|---|---|---|---|---|---|
| `SITE_URL` | Canonical origin for metadata | All | Dev | No | N/A |
| `ANALYTICS_ENDPOINT` | Synthetic event telemetry | Preview, Prod | DevOps | No | Annual |
| `FORM_SUBMIT_URL` | Destination for inquiries | Preview, Prod | Operations | No | Annual |
| `INQUIRY_NOTIFICATION_EMAIL` | Destination mailbox | All | Admin | M | As needed |
| `DEPLOY_WEBHOOK_SECRET` | Token for CI deployments | CI / GitHub | DevOps | YES (Vault) | Bi-annual |
