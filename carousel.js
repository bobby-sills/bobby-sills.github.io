// The projects carousel and the index beneath it. Homepage only, so it is a
// separate file from site.js — loading it after site.js (both deferred, which
// runs them in order) is what makes window.site.playClick available here.
(() => {
  const items = document.querySelectorAll(".projects li");
  if (!items.length) return;

  const playClick = () => window.site?.playClick();
  let index = 0;

  function show(i, withSound) {
    index = (i + items.length) % items.length;
    items.forEach((item, n) => {
      item.hidden = n !== index;
    });
    document.documentElement.style.setProperty(
      "--project-count",
      '"' + (index + 1) + "/" + items.length + '"',
    );
    // The highlight is driven off aria-current, so the styling and what a
    // screen reader is told can't drift apart.
    navButtons.forEach((button, n) => {
      if (n === index) button.setAttribute("aria-current", "true");
      else button.removeAttribute("aria-current");
    });
    if (withSound) playClick();
  }

  const nav = document.querySelector(".project-nav");
  const navButtons = [...items].map((item, n) => {
    const button = document.createElement("button");
    button.type = "button";
    // The h3's card counter is a ::after, so this is just the title.
    button.textContent = item.querySelector("h3").textContent;
    button.addEventListener("click", () => show(n, true));
    const li = document.createElement("li");
    li.append(button);
    nav.append(li);
    return button;
  });

  document
    .querySelector(".prev")
    .addEventListener("click", () => show(index - 1, true));
  document
    .querySelector(".next")
    .addEventListener("click", () => show(index + 1, true));
  show(0);
})();
