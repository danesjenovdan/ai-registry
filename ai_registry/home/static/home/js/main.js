function debounce(func, timeout = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(this, args);
    }, timeout);
  };
}

//

function addNewsletterListeners() {
  const form = document.querySelector(".page-footer .newsletter-form");
  if (form) {
    const emailEl = form.querySelector("#newsletter-email");

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const campaign_slug = "danes-je-nov-dan";
      const segment_id = 21;
      const email = emailEl.value;

      let url = `https://moj.djnd.si/${campaign_slug}/prijava?segment_id=${segment_id}`;
      url += `&email=${encodeURIComponent(email)}`;
      window.open(`${url}`, `_blank`);
      this.loading = false;
    });
  }
}

function toggleFilterDropdown() {
  const filters = document.querySelector(".registry-filters");
  const button = filters.querySelector(".filter-button");
  const options = filters.querySelector(".filter-options");

  button.addEventListener("click", () => {
    const isHidden = window.getComputedStyle(options).display === "none";
    if (isHidden) {
      options.style.display = "";
      button.classList.add("active");
    } else {
      options.style.display = "none";
      button.classList.remove("active");
    }
  });
}

function toggleSortDropdown() {
  const filters = document.querySelector(".registry-filters");
  const button = filters.querySelector(".sort-button");
  const options = filters.querySelector(".sort-options");

  button.addEventListener("click", () => {
    const isHidden = window.getComputedStyle(options).display === "none";
    options.style.display = isHidden ? "" : "none";
  });
}

function checkCollapsibleEntry(entry) {
  const collapsible = entry.querySelector(".entry-collapsible");
  const content = entry.querySelector(".entry-content");
  const actions = entry.querySelector(".entry-actions");

  const isCollapsed = entry.classList.contains("collapsed");

  if (isCollapsed) {
    actions.style.display = "";
    collapsible.style.height = "";
    collapsible.offsetHeight; // force reflow

    if (content.offsetHeight < collapsible.offsetHeight) {
      actions.style.display = "none";
      collapsible.style.height = "auto";
    }
  }
}

function toggleRegistryEntries() {
  const entries = document.querySelectorAll(".registry-entry");
  entries.forEach(checkCollapsibleEntry);

  window.addEventListener(
    "resize",
    debounce(() => {
      entries.forEach(checkCollapsibleEntry);
    })
  );

  // Add event listener to the document and delegate the event to the button.
  // This way we can add new entries to the page without having to add event
  // listeners to each one.
  document.addEventListener("click", (event) => {
    const button = event.target.closest(".registry-entry .expand-button");
    if (button) {
      const entry = button.closest(".registry-entry");
      const collapsible = entry.querySelector(".entry-collapsible");
      const content = entry.querySelector(".entry-content");

      const isCollapsed = entry.classList.contains("collapsed");

      if (isCollapsed) {
        collapsible.style.height = `${content.offsetHeight}px`;
        collapsible.addEventListener(
          "transitionend",
          () => {
            collapsible.style.height = "auto";
          },
          { once: true }
        );
        entry.classList.remove("collapsed");
      } else {
        collapsible.style.height = `${collapsible.offsetHeight}px`;
        collapsible.offsetHeight; // force reflow
        collapsible.style.height = "";
        entry.classList.add("collapsed");
      }

      const newText = button.dataset.toggleText;
      button.dataset.toggleText = button.textContent;
      button.textContent = newText;
    }
  });
}

function togglePillTooltips() {
  // Add event listener to the document and delegate the event to the element.
  // This way we can add new entries to the page without having to add event
  // listeners to each one.
  document.addEventListener("focusin", (event) => {
    const pill = event.target.closest(".pill.has-tooltip");
    if (pill) {
      const tooltip = pill.querySelector(".pill-tooltip-container");
      if (tooltip) {
        // reset visibility and position
        tooltip.style.display = "";
        tooltip.style.top = "auto";
        tooltip.style.right = "auto";

        // position tooltip
        const left = pill.offsetLeft + pill.offsetWidth - tooltip.offsetWidth;
        const top = pill.offsetTop - window.scrollY;
        tooltip.style.position = "fixed";
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
      }
    }
  });
  document.addEventListener("focusout", (event) => {
    const pill = event.target.closest(".pill.has-tooltip");
    if (pill) {
      const tooltip = pill.querySelector(".pill-tooltip-container");
      if (tooltip) {
        tooltip.style.display = "none";
      }
    }
  });
  document.addEventListener("scroll", () => {
    if (document.activeElement.matches(".pill.has-tooltip")) {
      document.activeElement.blur();
    }
  });
}

function setupTabbedInstitutionData() {
  document.querySelectorAll(".tab-content-container").forEach((container) => {
    const entry = container.closest(".registry-entry");
    const tabLinksContainer = entry.querySelector(".tab-links");
    const tabLinkScrollerContainer = tabLinksContainer.querySelector(
      ".tab-link-scroller-container"
    );
    const tabLinkScroller =
      tabLinksContainer.querySelector(".tab-link-scroller");

    // Activate first tab link
    const firstTabLink = tabLinksContainer.querySelector(".tab-link");
    firstTabLink.classList.add("active");

    // Set scroller container height to match tab link height
    tabLinkScroller.style.paddingBottom = "32px"; // account for scrollbar
    let tabHeight = Number.parseFloat(
      window.getComputedStyle(firstTabLink).height
    );
    tabHeight += Number.parseFloat(
      window.getComputedStyle(firstTabLink).marginTop
    );
    tabHeight += Number.parseFloat(
      window.getComputedStyle(firstTabLink).marginBottom
    );
    tabLinkScrollerContainer.style.height = `${tabHeight}px`;

    // Show scroll arrows if needed
    if (tabLinkScroller.scrollWidth > tabLinkScrollerContainer.clientWidth) {
      tabLinkScrollerContainer.insertAdjacentHTML(
        "afterbegin",
        `<button class="tab-link-scroller-button left" aria-label="Scroll left">
          &#9664;
        </button>`
      );
      tabLinkScrollerContainer.insertAdjacentHTML(
        "beforeend",
        `<button class="tab-link-scroller-button right" aria-label="Scroll right">
          &#9654;
        </button>`
      );

      const leftButton = tabLinkScrollerContainer.querySelector(
        ".tab-link-scroller-button.left"
      );
      const rightButton = tabLinkScrollerContainer.querySelector(
        ".tab-link-scroller-button.right"
      );

      leftButton.addEventListener("click", () => {
        tabLinkScroller.scrollBy({ left: -100, behavior: "smooth" });
      });
      rightButton.addEventListener("click", () => {
        tabLinkScroller.scrollBy({ left: 100, behavior: "smooth" });
      });
    }

    // Hide all tab contents except the first one
    const tabContents = container.querySelectorAll(".tab-content");
    Array.from(tabContents)
      .slice(1)
      .forEach((content) => {
        content.classList.add("hidden");
      });
  });

  document.querySelectorAll(".tab-link").forEach((tabLink) => {
    tabLink.addEventListener("click", (event) => {
      event.preventDefault();
      const entry = tabLink.closest(".registry-entry");
      const tabLinks = entry.querySelector(".tab-links");
      const tabContents = entry.querySelectorAll(".tab-content");

      // Deactivate all tabs
      const tabs = tabLinks.querySelectorAll(".tab-link");
      tabs.forEach((t) => t.classList.remove("active"));

      // Activate clicked tab
      tabLink.classList.add("active");

      // Show corresponding tab content
      const targetTab = tabLink.dataset.tab;
      tabContents.forEach((content) => {
        if (content.dataset.tab === targetTab) {
          content.classList.remove("hidden");
        } else {
          content.classList.add("hidden");
        }
      });
    });
  });
}

(function main() {
  addNewsletterListeners();
  toggleFilterDropdown();
  toggleSortDropdown();
  toggleRegistryEntries();
  togglePillTooltips();
  setupTabbedInstitutionData();
})();
