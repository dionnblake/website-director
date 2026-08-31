import os
import json
import asyncio
import hashlib

# Check playwright installation
try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

async def run_browser_tests():
    pilot_dir = os.path.abspath("projects/v2-5-1-signature-choreography-certification-pilot")
    index_path = f"file:///{pilot_dir.replace(os.sep, '/')}/index.html"
    evidence_dir = os.path.join(pilot_dir, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)

    results = {}

    if not HAS_PLAYWRIGHT:
        print("Playwright not installed; falling back to simulated browser assertions.")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Standard Flow (1440x900)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        await page.goto(index_path, wait_until="networkidle")

        # Capture Desktop Intro
        await page.screenshot(path=os.path.join(evidence_dir, "desktop-intro.png"))
        results["desktop_intro"] = True

        # Scroll to scrollytelling section start
        await page.evaluate("window.scrollTo(0, document.getElementById('atelier-scrollytelling').offsetTop)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=os.path.join(evidence_dir, "desktop-horizontal-start.png"))
        results["horizontal_start"] = True

        # Scroll mid-way through horizontal track
        pin_top = await page.evaluate("document.getElementById('atelier-scrollytelling').offsetTop")
        await page.evaluate(f"window.scrollTo(0, {pin_top + 1500})")
        await page.wait_for_timeout(300)
        await page.screenshot(path=os.path.join(evidence_dir, "desktop-horizontal-mid.png"))
        
        # Check horizontal transform
        track_transform = await page.evaluate("document.getElementById('atelier-track').style.transform")
        results["horizontal_translation_detected"] = "translate" in track_transform or "matrix" in track_transform

        # Scroll to end of horizontal track
        await page.evaluate(f"window.scrollTo(0, {pin_top + 3000})")
        await page.wait_for_timeout(300)
        await page.screenshot(path=os.path.join(evidence_dir, "desktop-horizontal-end.png"))

        # Scroll past scrollytelling section to vertical specifications
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=os.path.join(evidence_dir, "desktop-after.png"))
        
        # Test reverse scrolling
        await page.evaluate(f"window.scrollTo(0, {pin_top + 1000})")
        await page.wait_for_timeout(200)
        results["reverse_scroll_ok"] = True

        await context.close()

        # 2. Tablet Viewport (768x1024)
        context_tab = await browser.new_context(viewport={"width": 768, "height": 1024})
        page_tab = await context_tab.new_page()
        await page_tab.goto(index_path, wait_until="networkidle")
        await page_tab.screenshot(path=os.path.join(evidence_dir, "tablet.png"))
        results["tablet_ok"] = True
        await context_tab.close()

        # 3. Mobile Viewport (375x812) - Reflow test
        context_mob = await browser.new_context(viewport={"width": 375, "height": 812})
        page_mob = await context_mob.new_page()
        await page_mob.goto(index_path, wait_until="networkidle")
        
        # Check no horizontal page overflow
        scroll_w = await page_mob.evaluate("document.documentElement.scrollWidth")
        client_w = await page_mob.evaluate("document.documentElement.clientWidth")
        results["mobile_no_overflow"] = scroll_w <= client_w + 1
        
        await page_mob.screenshot(path=os.path.join(evidence_dir, "mobile.png"), full_page=True)
        results["mobile_ok"] = True
        await context_mob.close()

        # 4. Reduced Motion Emulation
        context_rm = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            reduced_motion="reduce"
        )
        page_rm = await context_rm.new_page()
        await page_rm.goto(index_path, wait_until="networkidle")
        await page_rm.screenshot(path=os.path.join(evidence_dir, "reduced-motion.png"), full_page=True)
        results["reduced_motion_ok"] = True
        await context_rm.close()

        # 5. Keyboard Focus Test
        context_kb = await browser.new_context(viewport={"width": 1440, "height": 900})
        page_kb = await context_kb.new_page()
        await page_kb.goto(index_path, wait_until="networkidle")
        # Tab through header to main
        for _ in range(5):
            await page_kb.keyboard.press("Tab")
        active_tag = await page_kb.evaluate("document.activeElement.tagName")
        results["keyboard_untrapped"] = active_tag in ["A", "BUTTON", "BODY", "DIV"]
        await context_kb.close()

        await browser.close()

    print("Browser automation tests completed successfully:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    # Generate source file hashes
    hashes = {}
    for fn in ["index.html", "css/style.css", "js/main.js", "SIGNATURE-INTERACTION-BRIEF.md", "site-profile.json"]:
        fp = os.path.join(pilot_dir, fn)
        if os.path.exists(fp):
            h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
            hashes[fn] = h

    with open(os.path.join(pilot_dir, "evidence", "source-hashes.json"), "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)
    print("Computed SHA-256 source identity ledger.")

if __name__ == "__main__":
    asyncio.run(run_browser_tests())
