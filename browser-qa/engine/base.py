"""BROWSER_QA_ENGINE adapter interface (Website Director V2.8).

The *policy* (BROWSER-REGRESSION-QA-PROTOCOL.md, the plan template, the assertion
catalogue, the evidence schema) is canonical and permanent. The *engine* that
drives a browser is replaceable. Every engine returns the same
``PageObservation`` shape so the assertion modules and the runner never depend on
Playwright, Puppeteer, CDP, or any specific automation library.

Two engines ship:

* ``simulation`` -- deterministic, dependency-free. Reads a fixture directory
  (``index.html`` + optional ``qa-fixture.json``) and materialises the
  observation from declared fixture data. Used for the framework's own
  negative-control validation so the suite runs anywhere with only the stdlib.
* ``playwright`` -- reference real-browser adapter. Requires ``playwright`` and
  its browsers; used against generated Website Director projects.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Verdict vocabulary (BROWSER-REGRESSION-QA-PROTOCOL.md sec 21)
# ---------------------------------------------------------------------------
PASS = "PASS"
FAIL = "FAIL"
FLAKY = "FLAKY"
BLOCKED = "BLOCKED"
NOT_APPLICABLE = "NOT_APPLICABLE"
VERDICTS = (PASS, FAIL, FLAKY, BLOCKED, NOT_APPLICABLE)

# Console / network classification (protocol sec 9 & sec 10)
KNOWN_NON_BLOCKING_WARNING = "KNOWN_NON_BLOCKING_WARNING"
TEST_ENVIRONMENT_NOISE = "TEST_ENVIRONMENT_NOISE"
APPLICATION_DEFECT = "APPLICATION_DEFECT"
THIRD_PARTY_DEFECT = "THIRD_PARTY_DEFECT"


@dataclass
class ConsoleMessage:
    level: str            # "error" | "warning" | "info" | "log"
    text: str
    classification: str = APPLICATION_DEFECT


@dataclass
class NetworkRequest:
    url: str
    status: int
    resource_type: str    # "document" | "script" | "stylesheet" | "image" | "font" | "xhr" | "fetch"
    ok: bool
    from_cache: bool = False
    third_party: bool = False
    blocked_allowed: bool = False   # documented optional third-party failure


@dataclass
class AnalyticsEvent:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)
    count: int = 1
    trigger: Optional[str] = None


@dataclass
class LayoutMetrics:
    viewport_width: int
    document_scroll_width: int
    client_width: int
    body_width: int
    has_horizontal_overflow: bool
    clipped_interactive_refs: List[str] = field(default_factory=list)
    zero_size_interactive_refs: List[str] = field(default_factory=list)
    offscreen_control_refs: List[str] = field(default_factory=list)
    fixed_nav_overlap: bool = False
    layout_shift_after_load: float = 0.0
    primary_cta_visible: bool = True


@dataclass
class FormState:
    form_ref: str
    fields_have_labels: bool = True
    invalid_shows_error: bool = True
    error_message_visible: bool = True
    submit_disabled_while_pending: bool = True
    duplicate_submit_prevented: bool = True
    success_state_on_success: bool = True
    success_state_on_server_reject: bool = False        # must stay False
    success_event_on_server_reject: bool = False        # must stay False
    keyboard_submittable: bool = True
    focus_moves_on_error: bool = True
    consent_gate_respected: bool = True


@dataclass
class KeyboardTrace:
    primary_nav_reachable: bool = True
    visible_focus_ring: bool = True
    menu_toggle_operable: bool = True
    dialog_escape_closes: bool = True
    no_keyboard_trap: bool = True
    primary_cta_reachable: bool = True


@dataclass
class SecurityObservation:
    is_https: bool = True
    mixed_content_urls: List[str] = field(default_factory=list)
    response_headers: Dict[str, str] = field(default_factory=dict)
    insecure_cookies: List[str] = field(default_factory=list)
    dom_secret_hits: List[str] = field(default_factory=list)
    third_party_scripts: List[str] = field(default_factory=list)
    analytics_active_before_consent: bool = False
    consent_reject_reachable: bool = True
    disclosure_routes_resolve: bool = True


@dataclass
class PerfSample:
    lcp_ms: Optional[float] = None
    cls: Optional[float] = None
    inp_ms: Optional[float] = None
    long_tasks: int = 0
    measurement_kind: str = "SYNTHETIC"     # SYNTHETIC | FIELD


# ---------------------------------------------------------------------------
# Accessibility (Website Director V2.9). The automated *engine* (axe-core, ...)
# is replaceable; ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md is the policy authority.
# ---------------------------------------------------------------------------
ENGINE_UNAVAILABLE = "BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE"
SCREEN_READER_UNAVAILABLE = "BLOCKED_SCREEN_READER_ENVIRONMENT"


@dataclass
class A11yViolation:
    rule_id: str
    impact: str            # "minor" | "moderate" | "serious" | "critical"
    wcag: str = ""
    target: str = ""
    help_text: str = ""


@dataclass
class AccessibilityObservation:
    engine_name: Optional[str] = None            # None => not run
    engine_version: Optional[str] = None
    engine_status: str = "NOT_RUN"               # NOT_RUN | RAN | ENGINE_UNAVAILABLE
    violations: List[A11yViolation] = field(default_factory=list)
    missing_accessible_name_refs: List[str] = field(default_factory=list)
    contrast_failures: List[str] = field(default_factory=list)     # "fg on bg = 2.9:1 @ selector"
    focus_visible: bool = True
    focus_obscured_refs: List[str] = field(default_factory=list)
    focus_obscured_indeterminate: bool = False   # engine could not decide -> MANUAL_REQUIRED
    landmarks: List[str] = field(default_factory=list)             # e.g. ["header","nav","main","footer"]
    heading_order_ok: bool = True
    h1_count: int = 1
    page_lang: str = "en"
    page_title: str = ""
    skip_link_present: Optional[bool] = None
    color_only_state_refs: List[str] = field(default_factory=list)
    small_target_refs: List[str] = field(default_factory=list)     # below the project minimum
    tiny_target_refs: List[str] = field(default_factory=list)      # below the WCAG 24px floor, no exception
    reflow_failures: List[str] = field(default_factory=list)       # at the reflow target width
    text_spacing_failures: List[str] = field(default_factory=list)
    unlabelled_field_refs: List[str] = field(default_factory=list)
    unassociated_error_refs: List[str] = field(default_factory=list)
    drag_without_alternative_refs: List[str] = field(default_factory=list)
    meaningful_images_missing_alt: List[str] = field(default_factory=list)
    decorative_images_exposed: List[str] = field(default_factory=list)
    dialogs: List[Dict[str, Any]] = field(default_factory=list)    # {ref, role, has_name, initial_focus, escape_closes, focus_returns, contained}
    keyboard_trap_refs: List[str] = field(default_factory=list)
    screen_reader_status: str = "NOT_RUN"        # NOT_RUN | COMPLETED | SCREEN_READER_UNAVAILABLE
    manual_keyboard_result: Optional[str] = None  # None | "PASS" | "FAIL" (declared by the manual harness/fixture)


@dataclass
class PageObservation:
    """Everything an assertion module is allowed to read about one page render."""
    route: str
    viewport: int
    engine: str
    browser: str
    reduced_motion: bool = False
    final_url: str = ""
    title: str = ""
    console: List[ConsoleMessage] = field(default_factory=list)
    network: List[NetworkRequest] = field(default_factory=list)
    layout: Optional[LayoutMetrics] = None
    forms: List[FormState] = field(default_factory=list)
    keyboard: Optional[KeyboardTrace] = None
    security: Optional[SecurityObservation] = None
    analytics_events: List[AnalyticsEvent] = field(default_factory=list)
    perf: Optional[PerfSample] = None
    images_zero_dimension: List[str] = field(default_factory=list)
    broken_assets: List[str] = field(default_factory=list)
    placeholder_images: List[str] = field(default_factory=list)
    reduced_motion_hidden_content: List[str] = field(default_factory=list)
    render_signature: str = ""          # deterministic visual fingerprint for regression
    nav_open_after_toggle: Optional[bool] = None
    nav_closed_after_route_change: Optional[bool] = None
    placeholder_hash_links: List[str] = field(default_factory=list)
    a11y: Optional[AccessibilityObservation] = None
    raw: Dict[str, Any] = field(default_factory=dict)


class BrowserQAEngine:
    """Abstract engine. Concrete engines implement ``observe``."""

    name = "abstract"
    supports_real_browser = False

    def __init__(self, project_root: str, config: Optional[Dict[str, Any]] = None):
        self.project_root = os.path.abspath(project_root)
        self.config = config or {}

    def available(self) -> bool:
        raise NotImplementedError

    def start(self) -> None:  # optional: bring up a local static server, launch browser
        pass

    def stop(self) -> None:   # MUST tear down every child process / server / profile
        pass

    def observe(self, route: str, viewport: int, *, reduced_motion: bool = False,
                browser: str = "chromium", interactions: Optional[List[Dict[str, Any]]] = None,
                ) -> PageObservation:
        raise NotImplementedError

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc):
        self.stop()
        return False


def load_engine(name: str, project_root: str, config: Optional[Dict[str, Any]] = None) -> BrowserQAEngine:
    name = (name or "simulation").lower()
    if name == "simulation":
        from .simulation_engine import SimulationEngine
        return SimulationEngine(project_root, config)
    if name == "playwright":
        from .playwright_engine import PlaywrightEngine
        return PlaywrightEngine(project_root, config)
    raise ValueError("unknown BROWSER_QA_ENGINE %r (known: simulation, playwright)" % name)


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
