# MORROW & VALE - RELEASE & DEPLOYMENT RUNBOOK

> **Technical Procedures for Setup, Build, Testing, Release & Rollback**  
> **Audience:** Technical Maintainers & DevOps Engineers  

---

## 1. Local Setup & Verification

1. Clone repository:
   git clone https://github.com/morrowvale-synthetic/website.git
2. Run deterministic validation suite:
   python tests/test_v2_5_client_handoff.py

---

## 2. Deployment Workflow
1. Draft to Staging: Push changes to staging branch. CI generates preview deployment.
2. Production Release: Open PR to main. Merge initiates zero-downtime deployment.

---

## 3. Rollback Procedures

### 3.1 Content Rollback
To restore content fixtures to a previous verified snapshot, run cms.restore_backup('snapshot-01').

### 3.2 Code Rollback
To roll back the static build artifact:
   git revert HEAD --no-edit
   git push origin main
