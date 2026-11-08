(() => {
  const componentSelector = 'ul[data-component="multiplechoice"]';
  const radioSelector = 'input[type="radio"]';

  function contextFor(option) {
    let question = null;
    let form = null;
    const match = option.id && option.id.match(/^(.*)_opt_[^_]+$/);

    if (match) {
      question = document.getElementById(match[1]);
      form = document.getElementById(match[1] + "_form");
    }

    if (!question) {
      const liveForm = option.closest('[id$="_form"]');
      if (liveForm && liveForm.id.endsWith("_form")) {
        form = liveForm;
        question = document.getElementById(liveForm.id.slice(0, -5));
      }
    }

    if (!question) {
      question = option.closest(componentSelector);
    }

    if (
      !question ||
      !question.matches(componentSelector) ||
      (question.getAttribute("data-multipleanswers") || "").trim().toLowerCase() !== "false"
    ) {
      return null;
    }

    form =
      form ||
      document.getElementById(question.id + "_form") ||
      question.closest(".ptx-runestone-container") ||
      question.closest(".multiplechoice_section") ||
      question;

    return { question, form };
  }

  function radioFrom(target) {
    if (!target || typeof target.closest !== "function") return null;
    if (target.matches && target.matches(radioSelector)) return target;

    const label = target.closest("label");
    const control = label && label.control;
    if (control && control.type === "radio") return control;

    return target.closest(radioSelector);
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
    [context.form, context.question].forEach((scope) => {
      if (scope) scope.querySelectorAll(radioSelector).forEach((radio) => found.add(radio));
    });
    return Array.from(found);
  }

  function lockChoices(context, chosen) {
    radios(context).forEach((radio) => {
      radio.disabled = true;
    });
    if (chosen) chosen.disabled = true;
  }

  function submitFirstChoice(context, chosen, attempts = 0) {
    if (context.question.dataset.firstAnswerLocked === "true") return;

    const button = checkButton(context);
    if (!button || button.disabled) {
      if (attempts < 20) {
        window.setTimeout(() => submitFirstChoice(context, chosen, attempts + 1), 50);
      }
      return;
    }

    context.question.dataset.firstAnswerLocked = "true";
    button.click();
    lockChoices(context, chosen);
    button.hidden = true;
    button.setAttribute("aria-hidden", "true");
    button.style.setProperty("display", "none", "important");
  }

  function beginChoice(option) {
    if (!option.checked) return;

    const context = contextFor(option);
    if (!context || context.question.dataset.firstAnswerPending === "true") return;

    context.question.dataset.firstAnswerPending = "true";
    radios(context).forEach((radio) => {
      if (radio !== option) radio.disabled = true;
    });
    window.setTimeout(() => submitFirstChoice(context, option), 0);
  }

  function handleChoice(event) {
    const option = radioFrom(event.target);
    if (!option) return;

    if (event.type === "change") {
      beginChoice(option);
    } else {
      window.setTimeout(() => beginChoice(option), 0);
    }
  }

  document.addEventListener("click", handleChoice, true);
  document.addEventListener("change", handleChoice, true);
})();
