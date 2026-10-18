// The viewer for /photography/. The collage is plain links to the full-size
// files, so with JavaScript off a click still opens the photo on its own;
// this upgrades those links into a dialog that steps through them in order.
(() => {
  const links = [...document.querySelectorAll(".photos a")];
  if (!links.length) return;

  const icon = (d) =>
    `<svg viewBox="0 0 24 24" width="36" height="36" fill="none"
          stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
          stroke-linejoin="round" aria-hidden="true"><path d="${d}" /></svg>`;

  document.body.insertAdjacentHTML(
    "beforeend",
    `<dialog class="lightbox" aria-label="photo viewer">
       <button class="lightbox-close" type="button" aria-label="close">
         ${icon("M18 6 6 18M6 6l12 12")}
       </button>
       <button class="lightbox-prev" type="button" aria-label="previous photo">
         ${icon("m15 18-6-6 6-6")}
       </button>
       <figure>
         <img alt="" />
         <figcaption>
           <span class="lightbox-camera"></span>
           <span class="lightbox-title"></span>
           <span class="lightbox-count"></span>
         </figcaption>
       </figure>
       <button class="lightbox-next" type="button" aria-label="next photo">
         ${icon("m9 18 6-6-6-6")}
       </button>
     </dialog>`,
  );

  const box = document.querySelector(".lightbox");
  const figure = box.querySelector("figure");
  const img = box.querySelector("img");
  const title = box.querySelector(".lightbox-title");
  const camera = box.querySelector(".lightbox-camera");
  const count = box.querySelector(".lightbox-count");
  const playClick = () => window.site?.playClick();
  let index = 0;
  // The order the viewer steps through. The mosaic packs tiles densely, so
  // what's on screen can differ from the list; this is re-read on every open
  // because the layout changes with the window.
  let order = links;

  // Top to bottom, then left to right, by where each tile's corner sits.
  function visualOrder() {
    const at = new Map(links.map((l) => [l, l.getBoundingClientRect()]));
    return [...links].sort(
      (a, b) =>
        Math.round(at.get(a).top - at.get(b).top) ||
        at.get(a).left - at.get(b).left,
    );
  }

  // One photo has nowhere to step to.
  if (links.length < 2) box.classList.add("single");

  const wrap = (i) => (i + order.length) % order.length;

  function show(i) {
    index = wrap(i);
    const link = order[index];
    img.src = link.href;
    img.alt = link.querySelector("img").alt;
    title.textContent = link.dataset.title;
    // Hidden when unknown, so the caption's gap doesn't hold an empty slot.
    camera.textContent = link.dataset.camera ?? "";
    camera.hidden = !link.dataset.camera;
    count.textContent = `${index + 1} / ${order.length}`;
    // The collage images are lazy, so the neighbours may not be fetched yet;
    // warming them now keeps the next step from showing a stale frame.
    new Image().src = order[wrap(index + 1)].href;
    new Image().src = order[wrap(index - 1)].href;
  }

  function step(by) {
    show(index + by);
    playClick();
  }

  links.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      order = visualOrder();
      show(order.indexOf(link));
      document.documentElement.classList.add("lightbox-open");
      box.showModal();
      playClick();
    });
  });

  box.querySelector(".lightbox-prev").addEventListener("click", () => step(-1));
  box.querySelector(".lightbox-next").addEventListener("click", () => step(1));
  box.querySelector(".lightbox-close").addEventListener("click", () => box.close());

  // Clicking the dark space around the photo closes it, the photo itself
  // doesn't. Escape is handled by the dialog itself.
  box.addEventListener("click", (e) => {
    if (e.target === box || e.target === figure) box.close();
  });

  box.addEventListener("close", () => {
    document.documentElement.classList.remove("lightbox-open");
    // Hand focus back to the photo that was open, which may not be the one
    // that was clicked, so keyboard users land where they left off.
    order[index].focus({ preventScroll: true });
  });

  box.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") step(-1);
    else if (e.key === "ArrowRight") step(1);
  });

  // Phones get a swipe as well as the arrows.
  let touchX = null;
  box.addEventListener("pointerdown", (e) => {
    if (e.pointerType === "touch") touchX = e.clientX;
  });
  box.addEventListener("pointerup", (e) => {
    if (touchX === null) return;
    const dx = e.clientX - touchX;
    touchX = null;
    if (Math.abs(dx) > 50 && links.length > 1) step(dx < 0 ? 1 : -1);
  });
})();
