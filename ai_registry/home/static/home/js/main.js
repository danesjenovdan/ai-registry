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
    const email = form.querySelector("#newsletter-email");
    const checkbox = form.querySelector("#newsletter-checkbox");
    const submit = form.querySelector("button[type=submit]");

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email.value,
          segment_id: 21,
        }),
      };

      // load start
      email.disabled = true;
      checkbox.disabled = true;
      submit.disabled = true;

      fetch("https://podpri.lb.djnd.si/api/subscribe/", options)
        .then((response) => response.json())
        .then((data) => {
          if (data.msg === "mail sent") {
            email.value = "";
            checkbox.checked = false;
            // load end
            email.disabled = false;
            checkbox.disabled = false;
            submit.disabled = false;
            alert(
              "Hvala! Poslali smo ti sporočilo s povezavo, na kateri lahko potrdiš prijavo!"
            );
          } else {
            // load end
            email.disabled = false;
            checkbox.disabled = false;
            submit.disabled = false;
            alert("Prišlo je do napake :(");
          }
        })
        .catch((error) => {
          console.error(error);
          // load end
          email.disabled = false;
          checkbox.disabled = false;
          submit.disabled = false;
          alert("Prišlo je do napake :(");
        });
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

    // Activate first tab link
    const firstTabLink = tabLinksContainer.querySelector(".tab-link");
    firstTabLink.classList.add("active");

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
