(() => {
  const componentSelector = 'ul[data-component="multiplechoice"]';
  const radioSelector = 'input[type="radio"]';

  function liveContext(option) {
    const form = option.closest('[id$="_form"]');
    if (form && form.id.endsWith("_form")) {
      const questionId = form.id.slice(0, -5);
      const question = document.getElementById(questionId);
      if (
        question &&
        question.matches(componentSelector) &&
        (question.getAttribute("data-multipleanswers") || "").trim().toLowerCase() === "false"
      ) {
        return { question, form };
      }
    }

    const question = option.closest(
      'ul[data-component="multiplechoice"][data-multipleanswers="false" i]'
    );
    if (!question) return null;
    const formScope =
      document.getElementById(question.id + "_form") ||
      question.closest(".ptx-runestone-container") ||
      question.closest(".multiplechoice_section");
    return { question, form: formScope || question };
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
      context.question.closest(".multiplechoice_section")
    ].filter((scope, index, all) => scope && all.indexOf(scope) === index);

    for (const scope of scopes) {
      const found = Array.from(
        scope.querySelectorAll('button, input[type="button"], input[type="submit"]')
      ).find((button) => buttonText(button) === "check me");
      if (found) return found;
    }
    return null;
  }

  function lockChoices(context) {
    context.form.querySelectorAll(radioSelector).forEach((radio) => {
      radio.disabled = true;
    });
    context.question.querySelectorAll(radioSelector).forEach((radio) => {
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

  document.addEventListener(
    "change",
    (event) => {
      const option = event.target;
      if (!(option instanceof HTMLInputElement) || option.type !== "radio" || !option.checked) return;

      const context = liveContext(option);
      if (!context || context.question.dataset.firstAnswerPending === "true") return;

      context.question.dataset.firstAnswerPending = "true";
      context.form.querySelectorAll(radioSelector).forEach((radio) => {
        if (radio !== option) radio.disabled = true;
      });
      context.question.querySelectorAll(radioSelector).forEach((radio) => {
        if (radio !== option) radio.disabled = true;
      });
      window.setTimeout(() => submitFirstChoice(context), 0);
    },
    true
  );
})();
