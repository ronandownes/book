(() => {
  const componentSelector = 'ul[data-component="multiplechoice"]';
  const radioSelector = 'input[type="radio"]';

  function matchingInPath(event, selector) {
    const path = typeof event.composedPath === "function" ? event.composedPath() : [event.target];
    return path.find((node) => node && typeof node.matches === "function" && node.matches(selector)) || null;
  }

  function contextFor(option, event) {
    const path = typeof event.composedPath === "function" ? event.composedPath() : [];
    const form = path.find((node) => node && node.id && node.id.endsWith("_form")) || null;
    const questionId = form ? form.id.slice(0, -5) : "";
    const root = form && typeof form.getRootNode === "function" ? form.getRootNode() : document;
    let question =
      (questionId && root.getElementById ? root.getElementById(questionId) : null) ||
      (questionId ? document.getElementById(questionId) : null);

    if (!question && option.id) {
      const match = option.id.match(/^(.*)_opt_[^_]+$/);
      if (match) {
        question =
          (root.getElementById ? root.getElementById(match[1]) : null) ||
          document.getElementById(match[1]);
      }
    }
    if (!question) question = option.closest(componentSelector);

    if (
      !question ||
      !question.matches(componentSelector) ||
      (question.getAttribute("data-multipleanswers") || "").trim().toLowerCase() !== "false"
    ) {
      return null;
    }

    const liveForm =
      form ||
      (question.id ? document.getElementById(question.id + "_form") : null) ||
      option.closest('[id$="_form"]') ||
      question.closest(".ptx-runestone-container") ||
      question.closest(".multiplechoice_section") ||
      question;

    return { question, form: liveForm };
  }

  function buttonText(button) {
    return (button.innerText || button.textContent || button.value || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function checkButton(context) {
    const scopes = [
      context.form,
      context.question.getRootNode(),
      context.question.closest(".ptx-runestone-container"),
      context.question.closest(".multiplechoice_section"),
      context.question.parentElement
    ].filter((scope, index, all) => scope && all.indexOf(scope) === index);

    for (const scope of scopes) {
      const found = Array.from(
        scope.querySelectorAll('button, input[type="button"], input[type="submit"]')
      ).find((button) => buttonText(button) === "check me");
      if (found) return found;
    }
    return null;
  }

  function radios(context) {
    const found = new Set();
    [context.form, context.question, context.question.getRootNode()].forEach((scope) => {
      if (scope) scope.querySelectorAll(radioSelector).forEach((radio) => found.add(radio));
    });
    return Array.from(found);
  }

  function lockChoices(context) {
    radios(context).forEach((radio) => {
      radio.disabled = true;
    });
  }

  function submitFirstChoice(context, attempts = 0) {
    if (context.question.dataset.firstAnswerLocked === "true") return;

    const button = checkButton(context);
    if (!button || button.disabled) {
      if (attempts < 20) {
        window.setTimeout(() => submitFirstChoice(context, attempts + 1), 50);
      }
      return;
    }

    context.question.dataset.firstAnswerLocked = "true";
    button.click();
    lockChoices(context);
    button.hidden = true;
    button.setAttribute("aria-hidden", "true");
    button.style.setProperty("display", "none", "important");
  }

  function beginChoice(context, option) {
    if (!option.checked || context.question.dataset.firstAnswerPending === "true") return;

    context.question.dataset.firstAnswerPending = "true";
    radios(context).forEach((radio) => {
      if (radio !== option) radio.disabled = true;
    });
    window.setTimeout(() => submitFirstChoice(context), 0);
  }

  function handleChoice(event) {
    const option = matchingInPath(event, radioSelector);
    if (!option) return;

    const context = contextFor(option, event);
    if (!context) return;

    if (event.type === "change") {
      beginChoice(context, option);
    } else {
      window.setTimeout(() => beginChoice(context, option), 0);
    }
  }

  document.addEventListener("click", handleChoice, true);
  document.addEventListener("change", handleChoice, true);
})();
