// Chrome shared by every page: the sound toggles and the snail. Both the
// markup and the wiring live here, so a new page needs nothing but
//
//   <link rel="stylesheet" href="../style.css" />
//   <script src="../site.js" defer></script>
//
// Pages with their own controls can borrow the click sound through
// window.site.playClick().
(() => {
  // Assets resolve against this script's own URL rather than the page's, so
  // one copy serves every directory depth. Root-absolute paths would do the
  // same on a server but break the file:// case the audio code below still
  // deliberately handles.
  const BASE = new URL(".", document.currentScript.src);
  const asset = (path) => new URL(path, BASE).href;

  // localStorage throws on file:// in some browsers; a lost preference
  // shouldn't take the rest of the page down with it.
  function readPref(key, fallback) {
    try {
      const stored = localStorage.getItem(key);
      if (stored === "on") return true;
      if (stored === "off") return false;
    } catch {}
    return fallback;
  }

  function writePref(key, on) {
    try {
      localStorage.setItem(key, on ? "on" : "off");
    } catch {}
  }

  let sfxOn = readPref("sfx", true);
  let ambienceOn = readPref("ambience", false);

  // The icon's two states are picked by CSS off aria-pressed, so both buttons
  // are the same markup and only the label and the class differ.
  const ICON = `
    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
      <path d="M11 5 6 9H2v6h4l5 4z" fill="currentColor" />
      <g class="waves" fill="none" stroke="currentColor" stroke-width="1.8"
         stroke-linecap="round">
        <path d="M15 9.5a4 4 0 0 1 0 5" />
        <path d="M17.8 7a8 8 0 0 1 0 10" />
      </g>
      <path class="mute" d="M15 9.5l5 5m0-5l-5 5" fill="none"
            stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
    </svg>`;

  const toggleMarkup = (cls, label, pressed) =>
    `<button class="sound-toggle ${cls}" type="button" aria-pressed="${pressed}">
       ${ICON}<span>${label}</span>
     </button>`;

  // Rendered with the stored state already applied, so a returning visitor
  // never sees the buttons flip after paint.
  document.querySelector("main").insertAdjacentHTML(
    "afterbegin",
    `<div class="sound-controls">
       ${toggleMarkup("sfx-toggle", "effects", sfxOn)}
       ${toggleMarkup("ambience-toggle", "background", ambienceOn)}
     </div>`,
  );

  document.body.insertAdjacentHTML(
    "beforeend",
    `<div class="snail" aria-hidden="true">
       <img src="${asset("images/snail.png")}" alt="" />
     </div>`,
  );

  const click = new Audio(asset("sounds/click.mp3"));
  click.volume = 0.35;
  const boing = new Audio(asset("sounds/boing.mp3"));
  boing.volume = 0.5;
  const sfxToggle = document.querySelector(".sfx-toggle");
  const ambienceToggle = document.querySelector(".ambience-toggle");

  // The ambient loop is far heavier than the click, so it is only fetched
  // once someone actually asks for it.
  const ambienceVolume = 0.28;
  let ambience = null;
  let ambienceCtx = null;

  function playAmbienceElement() {
    if (!ambience) {
      ambience = new Audio(asset("sounds/ambience.mp3"));
      ambience.loop = true;
      ambience.volume = ambienceVolume;
    }
    ambience.play().catch(() => {});
  }

  // MP3 primes the decoder with ~1100 samples of silence and pads the last
  // frame out to 1152, so <audio loop> replays ~40ms of padding on every
  // pass — an audible gap. Web Audio loops the decoded buffer sample-
  // accurately instead, but decoding needs fetch, which file:// refuses;
  // the element above stays as the fallback for that case.
  function startAmbience() {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx || location.protocol === "file:") {
      playAmbienceElement();
      return;
    }
    ambienceCtx = new Ctx();
    fetch(asset("sounds/ambience.mp3"))
      .then((res) => res.arrayBuffer())
      .then((bytes) => ambienceCtx.decodeAudioData(bytes))
      .then((buffer) => {
        const gain = ambienceCtx.createGain();
        gain.gain.value = ambienceVolume;
        gain.connect(ambienceCtx.destination);
        const source = ambienceCtx.createBufferSource();
        source.buffer = buffer;
        source.loop = true;
        source.connect(gain);
        source.start();
        // Decoding outlives a quick toggle back off, and a context built
        // without a gesture starts suspended either way.
        if (ambienceOn) ambienceCtx.resume().catch(() => {});
      })
      .catch(() => {
        ambienceCtx = null;
        playAmbienceElement();
      });
  }

  function updateAmbience() {
    if (!ambienceOn) {
      if (ambienceCtx) ambienceCtx.suspend().catch(() => {});
      if (ambience) ambience.pause();
      return;
    }
    if (ambienceCtx) {
      ambienceCtx.resume().catch(() => {});
    } else if (ambience) {
      playAmbienceElement();
    } else {
      startAmbience();
    }
  }

  function render() {
    sfxToggle.setAttribute("aria-pressed", String(sfxOn));
    ambienceToggle.setAttribute("aria-pressed", String(ambienceOn));
  }

  function play(sound) {
    if (!sfxOn) return;
    sound.currentTime = 0;
    sound.play().catch(() => {});
  }

  function playClick() {
    play(click);
  }

  sfxToggle.addEventListener("click", () => {
    sfxOn = !sfxOn;
    render();
    playClick();
    writePref("sfx", sfxOn);
  });

  ambienceToggle.addEventListener("click", () => {
    ambienceOn = !ambienceOn;
    render();
    playClick();
    updateAmbience();
    writePref("ambience", ambienceOn);
  });

  const snail = document.querySelector(".snail");
  let hop = null;

  // A flat duration made wider screens crawl faster in absolute terms, so the
  // duration is scaled to the distance and px/s stays constant everywhere.
  const SNAIL_SPEED = 10.45; // px per second
  const SNAIL_START = 1 / 3; // viewport fraction it sits at on arrival
  const SNAIL_WIDTH = 55; // matches .snail in the stylesheet

  // Off the left edge, across, and off the right.
  function crawlKeyframes() {
    return [
      { transform: `translateX(${-SNAIL_WIDTH}px)` },
      { transform: `translateX(${window.innerWidth}px)` },
    ];
  }

  function crawlDuration() {
    return ((window.innerWidth + SNAIL_WIDTH) / SNAIL_SPEED) * 1000;
  }

  // Seeking by time rather than reshaping the keyframes keeps one source of
  // truth for the path: at this offset the start has advanced exactly
  // SNAIL_START of the viewport. Only the first pass is skipped into — the
  // loop runs whole from the left edge after that.
  function crawlStart() {
    return ((window.innerWidth * SNAIL_START + SNAIL_WIDTH) / SNAIL_SPEED) * 1000;
  }

  // The crawl is built here rather than declared in CSS and read back with
  // getAnimations(). Reading it back was a race: a CSS animation only exists
  // once style has been resolved, and the snail is injected a moment earlier,
  // so an engine that defers that work handed back an empty list. Everything
  // guarded by `if (crawl)` then silently did nothing — the snail kept the
  // animation's own left-edge start, and a click flipped the art without
  // turning it round, because only the flip sat outside the guard.
  const crawl = snail.animate(crawlKeyframes(), {
    duration: crawlDuration(),
    iterations: Infinity,
    easing: "linear",
  });
  crawl.currentTime = crawlStart();

  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      // The keyframes are in px now, so the far edge has to be rewritten as
      // well as the duration; progress through the lap is what carries over.
      const oldDuration = crawl.effect.getTiming().duration;
      const progress = (crawl.currentTime ?? 0) / oldDuration;
      const newDuration = crawlDuration();
      crawl.effect.setKeyframes(crawlKeyframes());
      crawl.effect.updateTiming({ duration: newDuration });
      crawl.currentTime = progress * newDuration;
    }, 150);
  });

  snail.addEventListener("click", () => {
    // Flipping playbackRate reverses in place, so there's no jump in x.
    crawl.playbackRate *= -1;
    snail.classList.toggle("facing-left");
    play(boing);
    if (hop) hop.cancel();
    hop = snail.animate(
      [{ translate: "0 0" }, { translate: "0 -10px" }, { translate: "0 0" }],
      { duration: 450, easing: "ease-out" },
    );
  });

  // A returning visitor arrives with the preference set but no gesture yet,
  // so autoplay is still blocked — retry once they interact.
  if (ambienceOn) {
    updateAmbience();
    document.addEventListener("click", updateAmbience, { once: true });
  }

  render();

  window.site = { playClick };
})();
