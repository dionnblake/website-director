(() => {
  const root = document.documentElement;
  const body = document.body;
  const reduceMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointerQuery = window.matchMedia("(hover: hover) and (pointer: fine)");
  const state = {
    reduced: reduceMotionQuery.matches,
    ticking: false,
    menuOpen: false,
    lastFocused: null,
    fieldTimer: 0,
    entryTimer: 0,
  };

  const clamp = (value, min = 0, max = 1) => Math.min(Math.max(value, min), max);
  const byId = (id) => document.getElementById(id);

  if (finePointerQuery.matches) body.classList.add("has-pointer");

  /* Header and menu */
  const header = document.querySelector("[data-header]");
  const menuToggle = document.querySelector(".menu-toggle");
  const menuPanel = byId("menuPanel");
  const menuLinks = [...document.querySelectorAll(".menu-panel-nav a")];

  const getMenuFocusable = () =>
    [menuToggle, ...menuLinks].filter((element) => element && !element.disabled && !element.hasAttribute("hidden"));

  const closeMenu = (returnFocus = true) => {
    if (!menuPanel || !menuToggle) return;
    state.menuOpen = false;
    menuPanel.hidden = true;
    menuToggle.setAttribute("aria-expanded", "false");
    body.classList.remove("menu-open");
    if (returnFocus && state.lastFocused && typeof state.lastFocused.focus === "function") {
      state.lastFocused.focus();
    }
  };

  const openMenu = () => {
    if (!menuPanel || !menuToggle) return;
    state.lastFocused = document.activeElement;
    state.menuOpen = true;
    menuPanel.hidden = false;
    menuToggle.setAttribute("aria-expanded", "true");
    body.classList.add("menu-open");
    menuLinks[0]?.focus();
  };

  menuToggle?.addEventListener("click", () => {
    state.menuOpen ? closeMenu() : openMenu();
  });

  menuLinks.forEach((link) => link.addEventListener("click", () => closeMenu(false)));

  document.addEventListener("keydown", (event) => {
    if (!state.menuOpen) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeMenu();
      return;
    }
    if (event.key !== "Tab") return;
    const focusable = getMenuFocusable();
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (!first || !last) return;
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  const updateHeader = () => header?.classList.toggle("is-scrolled", window.scrollY > 24);
  window.addEventListener("scroll", updateHeader, { passive: true });
  updateHeader();

  /* Field guide tabs */
  const fieldData = {
    body: {
      label: "A body you trust",
      kicker: "The starting line",
      message: "Train for the life you want to carry. Strength is not a look. It is more options in a hard week.",
      action: "Find your first move",
      position: "50% 50%",
    },
    health: {
      label: "Make the baseline visible",
      kicker: "The honest audit",
      message: "Notice what gives you energy and what quietly takes it. Better health starts with a clearer read of your own days.",
      action: "Read the baseline",
      position: "50% 34%",
    },
    style: {
      label: "Wear the signal",
      kicker: "A visual standard",
      message: "The goal is not more clothes. It is a smaller set of choices that makes the man you are becoming easier to recognize.",
      action: "Find your uniform",
      position: "52% 48%",
    },
    mind: {
      label: "Clear the internal noise",
      kicker: "The quiet work",
      message: "A stronger mind is not a louder one. Make space for the decisions you keep postponing and the ideas worth keeping.",
      action: "Open the practice",
      position: "48% 40%",
    },
    work: {
      label: "Point your effort somewhere",
      kicker: "The useful pressure",
      message: "Ambition gets lighter when it has a direction. Choose the work that earns your attention, then make it visible.",
      action: "Set the direction",
      position: "50% 62%",
    },
    life: {
      label: "Make room for more of it",
      kicker: "The bigger frame",
      message: "The point is not to optimize every minute. It is to build a life with enough margin to feel like yours again.",
      action: "Make the room",
      position: "50% 68%",
    },
  };

  const fieldStage = document.querySelector(".field-stage");
  const fieldImage = byId("fieldImage");
  const fieldImageLabel = byId("fieldImageLabel");
  const fieldKicker = byId("fieldKicker");
  const fieldMessage = byId("fieldMessage");
  const fieldAction = byId("fieldAction");
  const fieldButtons = [...document.querySelectorAll(".field-button")];

  const updateField = (key) => {
    const next = fieldData[key];
    if (!next) return;
    window.clearTimeout(state.fieldTimer);
    fieldStage?.classList.add("is-changing");
    state.fieldTimer = window.setTimeout(() => {
      if (fieldImage) {
        fieldImage.style.objectPosition = next.position;
        fieldImage.alt = next.label + ".";
      }
      if (fieldImageLabel) fieldImageLabel.textContent = next.label;
      if (fieldKicker) fieldKicker.textContent = next.kicker;
      if (fieldMessage) fieldMessage.textContent = next.message;
      if (fieldAction) fieldAction.textContent = next.action;
      fieldStage?.classList.remove("is-changing");
    }, state.reduced ? 0 : 150);

    fieldButtons.forEach((button) => {
      const active = button.dataset.field === key;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", String(active));
      if (active) button.setAttribute("tabindex", "0");
      else button.setAttribute("tabindex", "-1");
    });
  };

  fieldButtons.forEach((button, index) => {
    button.addEventListener("click", () => updateField(button.dataset.field));
    if (finePointerQuery.matches) button.addEventListener("pointerenter", () => updateField(button.dataset.field));
    button.addEventListener("keydown", (event) => {
      const keys = ["ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp", "Home", "End"];
      if (!keys.includes(event.key)) return;
      event.preventDefault();
      let nextIndex = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = (index + 1) % fieldButtons.length;
      if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = (index - 1 + fieldButtons.length) % fieldButtons.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = fieldButtons.length - 1;
      fieldButtons[nextIndex]?.focus();
    });
  });

  if (fieldButtons[0]) fieldButtons[0].setAttribute("tabindex", "0");
  fieldButtons.slice(1).forEach((button) => button.setAttribute("tabindex", "-1"));

  /* Starting-point picker */
  const entryData = {
    energy: {
      kicker: "Start with your baseline",
      message: "Sleep, movement, food, and a calendar that leaves room to think. Make the floor stronger before you chase the ceiling.",
      action: "Build the floor",
    },
    confidence: {
      kicker: "Start with a visible win",
      message: "Keep one promise to yourself every day for a week. Confidence grows from evidence you can remember.",
      action: "Choose the promise",
    },
    direction: {
      kicker: "Start with a clean decision",
      message: "Name the next chapter in plain language. Then remove one commitment that keeps pulling you backward.",
      action: "Name the chapter",
    },
  };

  const entryTabs = [...document.querySelectorAll(".entry-tab")];
  const entryKicker = byId("entryKicker");
  const entryMessage = byId("entryMessage");
  const entryAction = byId("entryAction");
  const entryCount = byId("entryCount");

  const updateEntry = (key) => {
    const next = entryData[key];
    if (!next) return;
    window.clearTimeout(state.entryTimer);
    document.querySelector(".entry-panel")?.classList.add("is-changing");
    state.entryTimer = window.setTimeout(() => {
      if (entryKicker) entryKicker.textContent = next.kicker;
      if (entryMessage) entryMessage.textContent = next.message;
      if (entryAction) entryAction.textContent = next.action;
      document.querySelector(".entry-panel")?.classList.remove("is-changing");
    }, state.reduced ? 0 : 120);

    entryTabs.forEach((button, index) => {
      const active = button.dataset.entry === key;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", String(active));
      button.setAttribute("tabindex", active ? "0" : "-1");
      if (active && entryCount) entryCount.textContent = String(index + 1).padStart(2, "0") + " / 03";
    });
  };

  entryTabs.forEach((button, index) => {
    button.addEventListener("click", () => updateEntry(button.dataset.entry));
    button.addEventListener("keydown", (event) => {
      const keys = ["ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp", "Home", "End"];
      if (!keys.includes(event.key)) return;
      event.preventDefault();
      let nextIndex = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = (index + 1) % entryTabs.length;
      if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = (index - 1 + entryTabs.length) % entryTabs.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = entryTabs.length - 1;
      entryTabs[nextIndex]?.focus();
    });
  });

  if (entryTabs[0]) entryTabs[0].setAttribute("tabindex", "0");
  entryTabs.slice(1).forEach((button) => button.setAttribute("tabindex", "-1"));

  /* Progress sequence */
  const progressData = [
    {
      step: "STEP 01 / 04",
      status: "Clear the floor",
      message: "Start with the basics you keep skipping. Protect your sleep. Put movement on the calendar. Make the floor stronger.",
      value: "01 / 04",
      aria: "Stage one, clear the floor",
    },
    {
      step: "STEP 02 / 04",
      status: "Build the base",
      message: "Give your week a shape that can survive real work, real people, and the occasional bad day.",
      value: "02 / 04",
      aria: "Stage two, build the base",
    },
    {
      step: "STEP 03 / 04",
      status: "Raise the standard",
      message: "Choose the few standards that change how you enter a room, spend a morning, and talk to yourself.",
      value: "03 / 04",
      aria: "Stage three, raise the standard",
    },
    {
      step: "STEP 04 / 04",
      status: "Carry it forward",
      message: "The point is not a perfect streak. It is knowing how to return to the work when life gets loud.",
      value: "04 / 04",
      aria: "Stage four, carry it forward",
    },
  ];

  const momentumRange = byId("momentumRange");
  const progressStage = byId("progressStage");
  const progressStep = byId("progressStep");
  const progressStatus = byId("progressStatus");
  const progressNumber = byId("progressNumber");
  const progressMessage = byId("progressMessage");
  const momentumValue = byId("momentumValue");

  const updateProgress = () => {
    if (!momentumRange) return;
    const index = Number(momentumRange.value);
    const next = progressData[index] || progressData[0];
    progressStage?.style.setProperty("--progress", String(index / (progressData.length - 1)));
    if (progressStep) progressStep.textContent = next.step;
    if (progressStatus) progressStatus.textContent = next.status;
    if (progressNumber) progressNumber.textContent = String(index + 1).padStart(2, "0");
    if (progressMessage) progressMessage.textContent = next.message;
    if (momentumValue) momentumValue.textContent = next.value;
    momentumRange.setAttribute("aria-valuetext", next.aria);
  };

  momentumRange?.addEventListener("input", updateProgress);
  updateProgress();

  /* Scroll scenes and chapter rail */
  const hero = document.querySelector("[data-hero]");
  const parallaxMedia = document.querySelector("[data-parallax-media]");
  const railLinks = [...document.querySelectorAll("[data-rail-link]")];
  const sectionTargets = ["top", "turning", "framework", "start", "notes", "progress", "briefing"]
    .map((id) => byId(id))
    .filter(Boolean);

  const updateRail = () => {
    if (!sectionTargets.length) return;
    const marker = Math.min(window.innerHeight * 0.42, window.innerHeight - 1);
    let activeSection = sectionTargets[0];
    let closestDistance = Number.POSITIVE_INFINITY;

    sectionTargets.forEach((section) => {
      const rect = section.getBoundingClientRect();
      const containsMarker = rect.top <= marker && rect.bottom >= marker;
      const distance = containsMarker ? 0 : Math.min(Math.abs(rect.top - marker), Math.abs(rect.bottom - marker));
      if (distance < closestDistance) {
        activeSection = section;
        closestDistance = distance;
      }
    });

    railLinks.forEach((link) => {
      const active = link.dataset.railLink === activeSection.id;
      link.classList.toggle("is-active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    body.dataset.activeSection = activeSection.id;
  };

  const updateScrollScenes = () => {
    state.ticking = false;
    if (hero && !state.reduced) {
      const heroRect = hero.getBoundingClientRect();
      const heroProgress = clamp(-heroRect.top / Math.max(hero.offsetHeight * 0.82, 1));
      hero.style.setProperty("--hero-progress", heroProgress.toFixed(3));
    }
    updateRail();
  };

  const requestSceneUpdate = () => {
    if (state.ticking) return;
    state.ticking = true;
    window.requestAnimationFrame(updateScrollScenes);
  };

  window.addEventListener("scroll", requestSceneUpdate, { passive: true });
  window.addEventListener("resize", requestSceneUpdate);
  requestSceneUpdate();

  /* Reveal on entry */
  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
    );
    document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));
  } else {
    document.querySelectorAll(".reveal").forEach((element) => element.classList.add("is-visible"));
  }

  /* Pointer depth */
  if (finePointerQuery.matches && parallaxMedia) {
    let pointerFrame = 0;
    let pointerX = 0;
    let pointerY = 0;

    const applyPointerDepth = () => {
      pointerFrame = 0;
      if (state.reduced) return;
      parallaxMedia.style.setProperty("--pointer-x", pointerX.toFixed(2) + "px");
      parallaxMedia.style.setProperty("--pointer-y", pointerY.toFixed(2) + "px");
    };

    window.addEventListener(
      "pointermove",
      (event) => {
        pointerX = (event.clientX / window.innerWidth - 0.5) * -12;
        pointerY = (event.clientY / window.innerHeight - 0.5) * -8;
        if (!pointerFrame) pointerFrame = window.requestAnimationFrame(applyPointerDepth);
      },
      { passive: true }
    );
  }

  /* Local email capture */
  const briefingForm = byId("briefingForm");
  const emailInput = byId("email");
  const formStatus = byId("formStatus");
  const formButton = briefingForm?.querySelector("button");

  briefingForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!emailInput?.checkValidity()) {
      formStatus.textContent = "Add a valid email to enter the briefing.";
      formStatus.className = "form-status is-error";
      emailInput?.setAttribute("data-state", "error");
      emailInput?.focus();
      formButton?.setAttribute("data-state", "error");
      return;
    }
    formStatus.textContent = "You're on the list. First briefing soon.";
    formStatus.className = "form-status is-success";
    emailInput?.setAttribute("data-state", "success");
    formButton?.setAttribute("data-state", "success");
    emailInput.value = "";
    emailInput.placeholder = "You're in.";
  });

  /* Cursor label on fine pointers */
  const cursorOrb = byId("cursorOrb");
  const cursorLabel = byId("cursorLabel");
  let pointerFrame = 0;
  let pointerX = 0;
  let pointerY = 0;

  const moveCursor = () => {
    pointerFrame = 0;
    if (!cursorOrb) return;
    cursorOrb.style.left = pointerX + "px";
    cursorOrb.style.top = pointerY + "px";
  };

  if (finePointerQuery.matches && cursorOrb) {
    window.addEventListener(
      "pointermove",
      (event) => {
        pointerX = event.clientX;
        pointerY = event.clientY;
        if (!pointerFrame) pointerFrame = window.requestAnimationFrame(moveCursor);
      },
      { passive: true }
    );

    document.querySelectorAll("[data-cursor]").forEach((element) => {
      element.addEventListener("pointerenter", () => {
        if (cursorLabel) cursorLabel.textContent = element.dataset.cursor || "";
        cursorOrb.classList.add("is-active");
      });
      element.addEventListener("pointerleave", () => cursorOrb.classList.remove("is-active"));
    });
  }

  const onReducedMotionChange = (event) => {
    state.reduced = event.matches;
    if (state.reduced) {
      hero?.style.setProperty("--hero-progress", "0");
      parallaxMedia?.style.setProperty("--pointer-x", "0px");
      parallaxMedia?.style.setProperty("--pointer-y", "0px");
    }
    requestSceneUpdate();
  };

  if (typeof reduceMotionQuery.addEventListener === "function") {
    reduceMotionQuery.addEventListener("change", onReducedMotionChange);
  } else {
    reduceMotionQuery.addListener?.(onReducedMotionChange);
  }

  const year = byId("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
