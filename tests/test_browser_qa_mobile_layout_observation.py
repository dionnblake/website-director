"""Regression coverage for layout metrics around mobile-nav route probes.

The responsive layout observation belongs to the page's baseline render.  A
mobile-navigation route-change probe may change the scroll position, but it
must not redefine whether the initial primary CTA is visible at the viewport.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / "browser-qa"))

from engine.playwright_engine import PlaywrightEngine  # noqa: E402


class MobileNavigationLayoutObservationTests(unittest.TestCase):
    def test_route_probe_does_not_hide_baseline_primary_cta(self):
        with tempfile.TemporaryDirectory(prefix="wd-bqa-mobile-layout-") as temp_dir:
            project_root = Path(temp_dir)
            production = project_root / "production"
            production.mkdir()
            (production / "index.html").write_text(
                """<!doctype html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body>
  <header>
    <button type="button" data-qa="mobile-nav-toggle" aria-controls="site-menu" aria-expanded="false">Menu</button>
    <nav id="site-menu" hidden><a href="#method">Method</a></nav>
  </header>
  <main>
    <section style="height: 700px"><a data-qa="primary-cta" href="#contact">Primary CTA</a></section>
    <section id="method" style="height: 1400px">Method</section>
    <section id="contact">Contact</section>
  </main>
  <script>
    const toggle = document.querySelector('[data-qa="mobile-nav-toggle"]');
    const menu = document.getElementById('site-menu');
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      menu.hidden = !open;
    });
    menu.querySelector('a').addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      menu.hidden = true;
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        toggle.setAttribute('aria-expanded', 'false');
        menu.hidden = true;
      }
    });
  </script>
</body></html>""",
                encoding="utf-8",
            )

            engine = PlaywrightEngine(str(project_root), {"serve_dir": "production"})
            if not engine.available():
                self.fail("Playwright is required for this real-browser regression test")
            engine.start()
            try:
                observation = engine.observe("/", 375, browser="chromium")
            finally:
                engine.stop()

            self.assertIsNotNone(observation.layout)
            self.assertTrue(
                observation.layout.primary_cta_visible,
                "baseline CTA visibility was evaluated after the mobile route probe",
            )
            self.assertTrue(observation.nav_closed_after_route_change)


if __name__ == "__main__":
    unittest.main()
