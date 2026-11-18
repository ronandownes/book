/* Compact A/B/C/PP navigation beside the PreTeXt reading toolbar.
   The separate masthead brand logo remains one book-home link. */
(() => {
  "use strict";
  const resources = [
    { colour: "red",   short: "A",  label: "Apps",        href: "https://ronandownes.github.io/maths/" },
    { colour: "green", short: "B",  label: "Book",        href: "https://ronandownes.github.io/book/" },
    { colour: "blue",  short: "C",  label: "Calculators", href: "https://ronandownes.github.io/calculator/" },
    { colour: "black", short: "PP", label: "Past Papers", href: "https://ronandownes.github.io/pastpapers/" }
  ];
  if (!document.querySelector('link[data-maths-navigation="3"]')) {
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "quick-links.css?v=3";
    css.setAttribute("data-maths-navigation", "2");
    document.head.append(css);
  }
  function makeNavigation(className, ariaLabel) {
    const nav = document.createElement("nav");
    nav.className = className;
    nav.setAttribute("aria-label", ariaLabel);
    for (const item of resources) {
      const a = document.createElement("a");
      a.className = "book-resource-link book-resource-" + item.colour;
      a.href = item.href;
      a.title = item.short + " · " + item.label;
      a.setAttribute("aria-label", item.label);
      if (item.colour === "black") {
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      }
      const label = document.createElement("span");
      label.className = "book-shortcut-label";
      label.textContent = item.short;
      label.setAttribute("aria-hidden", "true");
      a.append(label);
      nav.append(a);
    }
    return nav;
  }

  // Keep the masthead SVG as a single linked logo. Only these toolbar
  // shortcuts are individual A, B, C and PP navigation links.

  // Keep the compact links in the page toolbar, including while reading.
  if (!document.querySelector(".book-abcd-quick-links")) {
    const nav = makeNavigation("book-abcd-quick-links",
      "Quick links: A Apps, B Book, C Calculators, PP Past Papers");
    const toolbar = document.querySelector(
      ".ptx-navbar,.ptx-toolbar,.ptx-navbar-global,.ptx-page-navbar"
    );
    if (toolbar) {
      toolbar.append(nav);
    } else {
      const masthead = document.querySelector(".ptx-banner,header#masthead,header");
      if (masthead) masthead.insertAdjacentElement("afterend", nav);
      else document.body.prepend(nav);
      nav.classList.add("book-abcd-standalone");
    }
  }
})();
