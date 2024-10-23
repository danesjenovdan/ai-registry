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

function toggleFilterDropdown() {
  const filters = document.querySelector(".registry-filters");
  const button = filters.querySelector(".filter-button");
  const options = filters.querySelector(".filter-options");

  button.addEventListener("click", () => {
    const isHidden = window.getComputedStyle(options).display === "none";
    options.style.display = isHidden ? "" : "none";
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

  actions.style.display = "";
  collapsible.style.height = "";
  collapsible.offsetHeight; // force reflow

  if (content.offsetHeight < collapsible.offsetHeight) {
    actions.style.display = "none";
    collapsible.style.height = "auto";
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
  const pills = document.querySelectorAll(".pill");
  pills.forEach((pill) => {
    pill.addEventListener("mouseenter", () => {
      const tooltip = pill.querySelector(".pill-tooltip-container");
      tooltip.style.display = "";
    });

    pill.addEventListener("mouseleave", () => {
      const tooltip = pill.querySelector(".pill-tooltip-container");
      tooltip.style.display = "none";
    });
  });
}

(function main() {
  toggleFilterDropdown();
  toggleSortDropdown();
  toggleRegistryEntries();
  togglePillTooltips();
})();
