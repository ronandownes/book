/* Classroom displays reuse native PreTeXt content and its already-rendered maths. */
(() => {
  "use strict";

  function install() {
    const settings = [
      {id: "ty-news-story", title: "From Chess to Mathematical Discovery", label: "slide", expected: 18},
      {id: "ty-number-theory-projects", title: "20 Number Theory Projects", label: "project", expected: 20}
    ];
    for (const setting of settings) {
      const section = document.getElementById(setting.id);
      if (!section || section.dataset.tyDisplayReady) continue;
      const slides = [...section.querySelectorAll(":scope > .subsection")];
      if (slides.length !== setting.expected) continue;
      section.dataset.tyDisplayReady = "true";
      const isStory = setting.id === "ty-news-story";
      if (isStory) {
        section.classList.add("ty-story-page");
        slides.forEach(slide => {
          for (const preview of slide.querySelectorAll(".video-box > div[onclick]")) {
            preview.setAttribute("role", "button");
            preview.setAttribute("aria-label", "Play the AlphaGo documentary");
            preview.tabIndex = 0;
            preview.addEventListener("keydown", event => {
              if (event.key === "Enter" || event.key === " ") { event.preventDefault(); preview.click(); }
            });
          }
          for (const frame of slide.querySelectorAll("iframe.video")) frame.title = "AlphaGo — the official documentary";
          for (const paragraph of slide.querySelectorAll(":scope > .para")) {
            if (/^(Source|Sources|History|Results|Context|Background|Read further):/.test(paragraph.textContent.trim())) {
              paragraph.classList.add("ty-story-source");
            }
            if (paragraph.querySelector('a[href*="youtube.com/watch"]')) paragraph.classList.add("ty-story-video-link");
          }
        });
      }
      const titles = slides.map(slide =>
        (slide.querySelector(":scope > .heading .title") || slide.querySelector(":scope > .heading"))
          .textContent.trim());

      const toolbar = document.createElement("div");
      toolbar.className = "ty-display-toolbar";
      const launch = document.createElement("button");
      launch.type = "button";
      launch.className = "ty-display-launch";
      launch.textContent = isStory ? "Start the visual classroom story" : "Display the 20 project choices";
      launch.setAttribute("aria-haspopup", "dialog");
      const help = document.createElement("p");
      help.textContent = "One idea at a time · arrow keys to move · Esc to return to the book";
      toolbar.append(launch, help);
      const firstHeading = section.querySelector(":scope > .heading");
      if (firstHeading) firstHeading.after(toolbar);
      else section.prepend(toolbar);

      const dialog = document.createElement("dialog");
      dialog.className = "ty-display-dialog";
      if (isStory) dialog.classList.add("ty-story-dialog");
      dialog.setAttribute("aria-labelledby", `${setting.id}-display-title`);
      dialog.innerHTML = `
        <header class="ty-display-header">
          <div><p class="ty-display-kicker"></p><p class="ty-display-counter" aria-live="polite"></p></div>
          <div class="ty-display-tools">
            <button type="button" class="ty-display-smaller" aria-label="Make display text smaller">A−</button>
            <button type="button" class="ty-display-larger" aria-label="Make display text larger">A+</button>
            <button type="button" class="ty-display-fullscreen">Full screen</button>
            <button type="button" class="ty-display-close">Close ×</button>
          </div>
        </header>
        <nav class="ty-display-chooser"><label>Choose a <span></span> <select></select></label></nav>
        <section class="ty-display-scroll" tabindex="0">
          <h2 id="${setting.id}-display-title"></h2>
          <div class="ty-display-content"></div>
        </section>
        <footer class="ty-display-footer">
          <button type="button" class="ty-display-previous">← Previous</button>
          <p>Test · explain · check</p>
          <button type="button" class="ty-display-next">Next →</button>
        </footer>`;
      document.body.append(dialog);
      dialog.querySelector(".ty-display-kicker").textContent = `TY Maths · ${setting.title}`;
      dialog.querySelector(".ty-display-chooser span").textContent = setting.label;
      const chooser = dialog.querySelector("select");
      titles.forEach((title, index) => {
        const option = document.createElement("option");
        option.value = String(index);
        option.textContent = `${index + 1}. ${title}`;
        chooser.append(option);
      });
      const counter = dialog.querySelector(".ty-display-counter");
      const heading = dialog.querySelector("h2");
      const viewport = dialog.querySelector(".ty-display-scroll");
      const content = dialog.querySelector(".ty-display-content");
      const previous = dialog.querySelector(".ty-display-previous");
      const next = dialog.querySelector(".ty-display-next");
      const fullscreen = dialog.querySelector(".ty-display-fullscreen");
      let position = 0;
      let active = null;
      let placeholder = null;
      let returnFocus = launch;
      let scale = 1;

      function restore() {
        if (active && placeholder?.parentNode) placeholder.replaceWith(active);
        active = null;
        placeholder = null;
      }
      function render(index) {
        restore();
        position = Math.max(0, Math.min(slides.length - 1, index));
        active = slides[position];
        placeholder = document.createComment("TY display: original content returns here");
        active.replaceWith(placeholder);
        content.replaceChildren(active);
        heading.textContent = `${position + 1}. ${titles[position]}`;
        counter.textContent = `${isStory ? "Slide" : "Project"} ${position + 1} of ${slides.length}`;
        chooser.value = String(position);
        previous.disabled = position === 0;
        next.disabled = position === slides.length - 1;
        viewport.scrollTop = 0;
      }
      function open(index, origin) {
        returnFocus = origin;
        render(index);
        dialog.showModal();
        viewport.focus();
      }
      function changeScale(delta) {
        scale = Math.max(0.8, Math.min(1.5, Math.round((scale + delta) * 10) / 10));
        dialog.style.setProperty("--ty-display-scale", String(scale));
      }
      launch.addEventListener("click", () => open(0, launch));
      slides.forEach((slide, index) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "ty-project-launch";
        button.setAttribute("aria-haspopup", "dialog");
        button.textContent = `Display ${setting.label} ${index + 1}`;
        slide.querySelector(":scope > .heading").after(button);
        button.addEventListener("click", () => open(index, button));
      });
      previous.addEventListener("click", () => render(position - 1));
      next.addEventListener("click", () => render(position + 1));
      chooser.addEventListener("change", () => render(Number(chooser.value)));
      dialog.querySelector(".ty-display-close").addEventListener("click", () => dialog.close());
      dialog.querySelector(".ty-display-smaller").addEventListener("click", () => changeScale(-0.1));
      dialog.querySelector(".ty-display-larger").addEventListener("click", () => changeScale(0.1));
      function updateFullscreenLabel() {
        const expanded = document.fullscreenElement === dialog || dialog.classList.contains("ty-display-expanded");
        fullscreen.textContent = expanded ? "Restore view" : "Full screen";
        fullscreen.setAttribute("aria-pressed", String(expanded));
      }
      fullscreen.addEventListener("click", async () => {
        try {
          if (document.fullscreenElement) await document.exitFullscreen();
          else if (dialog.classList.contains("ty-display-expanded")) dialog.classList.remove("ty-display-expanded");
          else if (document.fullscreenEnabled) await dialog.requestFullscreen();
          else dialog.classList.add("ty-display-expanded");
        } catch (_) { dialog.classList.add("ty-display-expanded"); }
        updateFullscreenLabel();
      });
      document.addEventListener("fullscreenchange", updateFullscreenLabel);
      dialog.addEventListener("close", () => {
        restore();
        dialog.classList.remove("ty-display-expanded");
        if (document.fullscreenElement === dialog) document.exitFullscreen().catch(() => {});
        updateFullscreenLabel();
        returnFocus.focus();
      });
      dialog.addEventListener("keydown", event => {
        if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest("select,input,textarea")) return;
        if (event.key === "ArrowRight") { event.preventDefault(); render(position + 1); }
        if (event.key === "ArrowLeft") { event.preventDefault(); render(position - 1); }
        if (event.key === "Home") { event.preventDefault(); render(0); }
        if (event.key === "End") { event.preventDefault(); render(slides.length - 1); }
      });
      window.addEventListener("beforeprint", () => { if (dialog.open) dialog.close(); });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", install, {once: true});
  else install();
})();
