(() => {
  const radioSelector = 'input[type="radio"]';

  function radioFromEvent(event) {
    const path =
      typeof event.composedPath === "function"
        ? event.composedPath()
        : [event.target];
    return (
      path.find(
        (node) =>
          node &&
          typeof node.matches === "function" &&
          node.matches(radioSelector)
      ) || null
    );
  }

  function contextFor(option) {
    const idMatch = option.id.match(/^(.*)_opt_\d+$/);
    const form =
      option.closest('[id$="_form"]') ||
      (idMatch ? document.getElementById(idMatch[1] + "_form") : null);
    if (!form) return null;

    const radios = Array.from(form.querySelectorAll(radioSelector));
    if (!radios.includes(option)) return null;

    const checkButton = Array.from(
      form.querySelectorAll(
        'button, input[type="button"], input[type="submit"]'
      )
    ).find((button) =>
      (button.innerText || button.textContent || button.value || "")
        .replace(/\s+/g, " ")
        .trim()
        .toLowerCase()
        .includes("check me")
    );

    if (!checkButton) return null;
    return { form, radios, checkButton };
  }

  function lockAndCheck(context) {
    if (context.form.dataset.firstAnswerLocked === "true") return;

    context.form.dataset.firstAnswerLocked = "true";
    context.checkButton.click();
    context.radios.forEach((radio) => {
      radio.disabled = true;
    });
    context.checkButton.hidden = true;
    context.checkButton.setAttribute("aria-hidden", "true");
    context.checkButton.style.setProperty("display", "none", "important");
  }

  function handleChange(event) {
    const option = radioFromEvent(event);
    if (!option || !option.checked) return;

    const context = contextFor(option);
    if (!context || context.form.dataset.firstAnswerPending === "true") return;

    context.form.dataset.firstAnswerPending = "true";
    window.setTimeout(() => lockAndCheck(context), 0);
  }

  document.addEventListener("change", handleChange, true);
})();