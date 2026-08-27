# PRODUCTION PRE-FLIGHT REVIEW: [PROJECT NAME]

> **Date Completed:** YYYY-MM-DD  
> **Lead QA:** Website Director Production Subsystem  
> **Reference Standard:** `PRODUCTION-CHECKLIST.md`

---

## 1. Verification Audit Table

| Area | Check Item | Status (PASS / FAIL / N/A) | Notes / Observations |
| :--- | :--- | :---: | :--- |
| **Viewports** | Desktop (1440px+), Tablet, Mobile (375px) | [PASS / FAIL] | [Zero horizontal overflow, clean responsive reflow] |
| **Touch Targets** | All interactive targets $\ge 44\text{px} \times 44\text{px}$ | [PASS / FAIL] | [Validated on touch emulation] |
| **Navigation** | Sticky header, mobile drawer, active states | [PASS / FAIL] | [Drawer locks scroll, smooth transition] |
| **Forms** | Validation, error copy, loading states | [PASS / FAIL] | [Tested invalid and valid submission flows] |
| **Links & Buttons** | Zero dead links, `rel="noopener noreferrer"` | [PASS / FAIL] | [All external links verified] |
| **Keyboard / A11y**| Focus rings, tab order, modal ESC escape | [PASS / FAIL] | [Full tab navigation validated] |
| **Contrast** | WCAG AA compliance ($\ge 4.5:1$ text contrast) | [PASS / FAIL] | [Checked via automated contrast audit] |
| **Typography** | Responsive clamp scaling, font-display swap | [PASS / FAIL] | [Zero FOUT/FOIT jank detected] |
| **Performance** | LCP $< 2.5\text{s}$, CLS $< 0.1$, INP $< 200\text{ms}$ | [PASS / FAIL] | [Lighthouse / Core Web Vitals audit] |
| **Images** | WebP/AVIF format, lazy loading, aspect ratio| [PASS / FAIL] | [All images optimized and sized] |
| **SEO & Meta** | Title, meta description, canonical, OG tags | [PASS / FAIL] | [Social share cards rendering accurately] |
| **SEO Strategy Fidelity** | Pages/keywords match `keyword-map.md`; sitemap, robots, schema, no stuffing (`PRODUCTION-CHECKLIST.md` §5.1) | [PASS / FAIL] | [Cite any drift from the locked SEO spec] |
| **Favicon & 404** | Favicon package configured, custom 404 page | [PASS / FAIL] | [Custom 404 tested] |
| **Console Clean** | Zero JS errors, 404 asset failures | [PASS / FAIL] | [Clean browser console] |
| **Build Status** | Clean production bundle without warnings | [PASS / FAIL] | [Executed `npm run build` cleanly] |

---

## 2. Identified Blocker Remediation
- *Blocker 1:* [Description & resolution, or "None"]
- *Blocker 2:* [Description & resolution, or "None"]

---

## 3. Final Deployment Authorization
- [ ] **ALL PRE-FLIGHT CHECKS PASSED:** Build is authorized for live commercial deployment.
- [ ] **DEPLOYMENT BLOCKED:** Outstanding issues must be remediated prior to launch.
