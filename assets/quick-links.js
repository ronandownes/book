/* Four direct Maths-resource links. The large masthead dots and compact
   PreTeXt toolbar shortcuts both point to Apps, Book, Calculators, Past Papers.
   Leave the book structure, section navigation and original SVG intact. */
(() => {
  "use strict";
  const resources = [
    { colour: "red",   short: "A",  label: "Apps",        href: "https://ronandownes.github.io/maths/" },
    { colour: "green", short: "B",  label: "Book",        href: "https://ronandownes.github.io/book/" },
    { colour: "blue",  short: "C",  label: "Calculators", href: "https://ronandownes.github.io/calculator/" },
    { colour: "black", short: "PP", label: "Past Papers", href: "https://ronandownes.github.io/pastpapers/" }
  ];
  if (!document.querySelector('link[data-maths-navigation="2"]')) {
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "quick-links.css?v=2";
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

  // Replace only the SVG's enclosing link. This is a visual navigation change,
  // not a change to the actual PreTeXt source or its Parts/chapters/sections.
  const logo = Array.from(document.images).find(img =>
    (img.getAttribute("src") || "").includes("four-dots.svg")
  );
  const logoLink = logo && logo.closest("a");
  if (logoLink && logoLink.querySelectorAll("img").length === 1 &&
      logoLink.textContent.trim() === "" &&
      !document.querySelector(".book-main-quick-links")) {
    logoLink.replaceWith(makeNavigation("book-main-quick-links",
      "Maths resources: Apps, Book, Calculators and Past Papers"));
  }

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
