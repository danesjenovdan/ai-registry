function toggleRegistryEntries() {
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

(function main() {
  toggleRegistryEntries();
})();
