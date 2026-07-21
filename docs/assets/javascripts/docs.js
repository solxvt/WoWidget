document.addEventListener("DOMContentLoaded", () => {
  const lightbox = document.createElement("div");
  lightbox.className = "ww-lightbox";
  lightbox.setAttribute("role", "dialog");
  lightbox.setAttribute("aria-modal", "true");
  lightbox.innerHTML = '<button class="ww-lightbox__close" aria-label="Close image">×</button><img alt="Expanded documentation screenshot">';
  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector("img");
  const closeLightbox = () => {
    lightbox.classList.remove("is-open");
    lightboxImage.removeAttribute("src");
  };

  document.querySelectorAll(".doc-screenshot img").forEach((image) => {
    image.addEventListener("click", () => {
      lightboxImage.src = image.currentSrc || image.src;
      lightboxImage.alt = image.alt || "Expanded documentation screenshot";
      lightbox.classList.add("is-open");
    });
  });

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox || event.target.closest(".ww-lightbox__close")) closeLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeLightbox();
  });

  document.querySelectorAll(".copy-button").forEach((button) => {
    button.addEventListener("click", async () => {
      const value = button.dataset.copy || "";
      try {
        await navigator.clipboard.writeText(value);
        const oldText = button.textContent;
        button.textContent = "Copied";
        window.setTimeout(() => { button.textContent = oldText; }, 1400);
      } catch {
        button.textContent = "Copy failed";
      }
    });
  });
});

// FAQ live search. Kept independent from troubleshooting search so both pages
// can evolve without sharing fragile selectors or markup assumptions.
document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#faq-search");
  if (!input) return;

  const clearButton = document.querySelector("#faq-search-clear");
  const count = document.querySelector("#faq-result-count");
  const empty = document.querySelector("#faq-empty");
  const items = Array.from(document.querySelectorAll("[data-faq-item]"));
  const categories = Array.from(document.querySelectorAll("[data-faq-category]"));
  const popular = document.querySelector(".faq-popular");
  const categoryNav = document.querySelector(".faq-categories");

  const normalize = (value) => value.toLowerCase().replace(/\s+/g, " ").trim();

  const filter = () => {
    const query = normalize(input.value);
    let visibleCount = 0;

    items.forEach((item) => {
      const haystack = normalize(`${item.textContent} ${item.dataset.search || ""}`);
      const matches = !query || query.split(" ").every((term) => haystack.includes(term));
      item.hidden = !matches;
      if (matches) visibleCount += 1;
      if (query && matches) item.open = true;
      if (!query) item.open = false;
    });

    categories.forEach((category) => {
      const hasVisibleItem = Array.from(category.querySelectorAll("[data-faq-item]")).some((item) => !item.hidden);
      category.hidden = !hasVisibleItem;
    });

    if (popular) popular.hidden = Boolean(query);
    if (categoryNav) categoryNav.hidden = Boolean(query);
    if (empty) empty.hidden = visibleCount !== 0;
    if (count) count.textContent = query
      ? `${visibleCount} matching question${visibleCount === 1 ? "" : "s"}`
      : `Showing all ${items.length} questions`;
  };

  input.addEventListener("input", filter);
  clearButton?.addEventListener("click", () => {
    input.value = "";
    filter();
    input.focus();
  });

  filter();
});

// Troubleshooting knowledge-base search and category filtering.
// This is intentionally isolated from the FAQ filter because each page has
// different markup and interaction requirements.
(() => {
  const initializeTroubleshooting = () => {
    const input = document.querySelector("#troubleshooting-search");
    if (!input || input.dataset.wwInitialized === "true") return;
    input.dataset.wwInitialized = "true";

    const clearButton = document.querySelector("#troubleshooting-clear");
    const status = document.querySelector("#troubleshooting-results");
    const empty = document.querySelector("#troubleshooting-empty");
    const categories = document.querySelector(".support-categories");
    const quickCheck = document.querySelector(".support-quick-check");
    const items = Array.from(document.querySelectorAll("[data-support-item]"));
    const sections = Array.from(document.querySelectorAll("[data-support-section]"));

    const normalize = (value) => (value || "")
      .toLowerCase()
      .replace(/[“”‘’]/g, "")
      .replace(/\s+/g, " ")
      .trim();

    const applyFilter = () => {
      const query = normalize(input.value);
      const terms = query.split(" ").filter(Boolean);
      let visibleCount = 0;

      items.forEach((item) => {
        const haystack = normalize(`${item.textContent} ${item.dataset.search || ""}`);
        const matches = terms.length === 0 || terms.every((term) => haystack.includes(term));
        item.hidden = !matches;
        if (matches) visibleCount += 1;

        if (query && matches) item.open = true;
        if (!query) item.open = false;
      });

      sections.forEach((section) => {
        const hasMatch = Array.from(section.querySelectorAll("[data-support-item]"))
          .some((item) => !item.hidden);
        section.hidden = !hasMatch;
      });

      if (clearButton) clearButton.hidden = !query;
      if (categories) categories.hidden = Boolean(query);
      if (quickCheck) quickCheck.hidden = Boolean(query);
      if (empty) empty.hidden = visibleCount !== 0;
      if (status) {
        status.textContent = query
          ? `${visibleCount} matching solution${visibleCount === 1 ? "" : "s"}`
          : `Browse all ${items.length} troubleshooting solutions`;
      }
    };

    input.addEventListener("input", applyFilter);
    clearButton?.addEventListener("click", () => {
      input.value = "";
      applyFilter();
      input.focus();
    });

    document.querySelectorAll(".support-categories a").forEach((link) => {
      link.addEventListener("click", () => {
        const id = link.getAttribute("href")?.slice(1);
        const target = id ? document.getElementById(id) : null;
        if (!target) return;
        window.setTimeout(() => target.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
      });
    });

    applyFilter();
  };

  document.addEventListener("DOMContentLoaded", initializeTroubleshooting);
  if (typeof document$ !== "undefined") document$.subscribe(initializeTroubleshooting);
})();

// Builds desktop dropdowns from Material's own nested navigation tree.
(() => {
  const descriptions = {
    "Installation": "Download and install WoWidget.",
    "Blizzard Setup": "Create Blizzard API credentials.",
    "Discord Setup": "Create and authorize the Discord app.",
    "Widget Setup": "Configure and publish the profile widget.",
    "Application Setup": "Connect the finished configuration.",
    "Character Selection": "Search for and select a character.",
    "Portrait Studio": "Generate and position the character model.",
    "Updating Your Widget": "Run manual and automatic refreshes.",
    "Widget Variables": "Browse supported data fields and types.",
    "FAQ": "Learn how WoWidget works.",
    "Frequently Asked Questions": "Learn how WoWidget works.",
    "Troubleshooting": "Resolve common setup and update issues."
  };

  let portal;
  let activeTrigger;
  let closeTimer;

  const normalize = (url) => {
    const parsed = new URL(url, window.location.href);
    return parsed.pathname.replace(/index\.html$/, "").replace(/\/+$/, "/");
  };

  const ensurePortal = () => {
    if (portal?.isConnected) return portal;
    portal = document.createElement("div");
    portal.className = "ww-tabs-portal";
    portal.setAttribute("role", "menu");
    portal.addEventListener("mouseenter", () => window.clearTimeout(closeTimer));
    portal.addEventListener("mouseleave", scheduleClose);
    document.body.appendChild(portal);
    return portal;
  };

  const findDrawerSection = (tabLink) => {
    const target = normalize(tabLink.href);
    const candidates = document.querySelectorAll(
      ".md-nav--primary .md-nav__item--nested > .md-nav__link"
    );

    return [...candidates].find((link) => {
      const sameTitle = link.textContent.trim() === tabLink.textContent.trim();
      let samePath = false;
      try { samePath = normalize(link.href) === target; } catch (_) {}
      return sameTitle || samePath;
    })?.parentElement ?? null;
  };

  const getChildren = (tabLink) => {
    const section = findDrawerSection(tabLink);
    if (!section) return [];

    const nestedNav = section.querySelector(":scope > .md-nav");
    if (!nestedNav) return [];

    return [...nestedNav.querySelectorAll(":scope > .md-nav__list > .md-nav__item > .md-nav__link")]
      .filter((link) => link.href && !link.classList.contains("md-nav__link--index"))
      .map((link) => ({
        title: link.textContent.trim(),
        href: link.href
      }));
  };

  const positionPortal = (trigger) => {
    const rect = trigger.getBoundingClientRect();
    const menu = ensurePortal();
    const left = Math.min(rect.left, window.innerWidth - menu.offsetWidth - 16);
    menu.style.top = `${Math.round(rect.bottom + 7)}px`;
    menu.style.left = `${Math.max(8, Math.round(left))}px`;
  };

  const openMenu = (trigger, items) => {
    window.clearTimeout(closeTimer);
    const menu = ensurePortal();
    const current = normalize(window.location.href);
    const label = trigger.textContent.trim();

    menu.replaceChildren();
    const heading = document.createElement("span");
    heading.className = "ww-tabs-portal__label";
    heading.textContent = label;
    menu.appendChild(heading);

    items.forEach(({ title, href }) => {
      const link = document.createElement("a");
      link.className = "ww-tabs-portal__link";
      link.href = href;
      link.setAttribute("role", "menuitem");
      if (normalize(href) === current) link.classList.add("is-current");

      const strong = document.createElement("strong");
      strong.textContent = title;
      const small = document.createElement("small");
      small.textContent = descriptions[title] || "Open this documentation article.";
      link.append(strong, small);
      menu.appendChild(link);
    });

    if (activeTrigger && activeTrigger !== trigger) {
      activeTrigger.dataset.wwMenuOpen = "false";
      activeTrigger.setAttribute("aria-expanded", "false");
    }

    activeTrigger = trigger;
    trigger.dataset.wwMenuOpen = "true";
    trigger.setAttribute("aria-expanded", "true");
    menu.classList.add("is-visible");
    requestAnimationFrame(() => positionPortal(trigger));
  };

  function closeMenu() {
    portal?.classList.remove("is-visible");
    if (activeTrigger) {
      activeTrigger.dataset.wwMenuOpen = "false";
      activeTrigger.setAttribute("aria-expanded", "false");
    }
    activeTrigger = null;
  }

  function scheduleClose() {
    window.clearTimeout(closeTimer);
    closeTimer = window.setTimeout(closeMenu, 130);
  }

  const enhanceTabs = () => {
    const tabs = document.querySelectorAll(".md-tabs__item > .md-tabs__link");
    tabs.forEach((trigger) => {
      if (trigger.dataset.wwChecked === "true") return;
      const children = getChildren(trigger);
      trigger.dataset.wwChecked = "true";
      if (!children.length) return; // Home and About remain normal links.

      trigger.dataset.wwHasMenu = "true";
      trigger.dataset.wwMenuOpen = "false";
      trigger.setAttribute("aria-haspopup", "menu");
      trigger.setAttribute("aria-expanded", "false");

      trigger.addEventListener("mouseenter", () => openMenu(trigger, children));
      trigger.addEventListener("mouseleave", scheduleClose);
      trigger.addEventListener("focus", () => openMenu(trigger, children));
      trigger.addEventListener("click", (event) => {
        if (!window.matchMedia("(min-width: 1220px)").matches) return;
        if (trigger.dataset.wwMenuOpen !== "true") {
          event.preventDefault();
          openMenu(trigger, children);
        }
      });
    });
  };

  const initialize = () => {
    enhanceTabs();
    // Material can rebuild navigation after instant page changes.
    const observer = new MutationObserver(enhanceTabs);
    const tabs = document.querySelector(".md-tabs");
    const drawer = document.querySelector(".md-nav--primary");
    if (tabs) observer.observe(tabs, { childList: true, subtree: true });
    if (drawer) observer.observe(drawer, { childList: true, subtree: true });
  };

  window.addEventListener("resize", () => {
    if (activeTrigger && portal?.classList.contains("is-visible")) {
      positionPortal(activeTrigger);
    }
  });
  window.addEventListener("scroll", closeMenu, { passive: true });
  document.addEventListener("click", (event) => {
    if (event.target.closest(".ww-tabs-portal") || event.target.closest(".md-tabs__item")) return;
    closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  document.addEventListener("DOMContentLoaded", initialize);
  if (typeof document$ !== "undefined") document$.subscribe(initialize);
})();

