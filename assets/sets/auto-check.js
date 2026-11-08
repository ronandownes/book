(() => {
  const selector = 'ul[data-component="multiplechoice"][data-multipleanswers="false"]';

  function labelOf(button) {
    return (button.innerText || button.textContent || button.value || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function findCheckButton(question) {
    const section = question.closest(".multiplechoice_section");
    if (!section) return null;
    return Array.from(section.querySelectorAll('button, input[type="button"], input[type="submit"]'))
      .find((button) => labelOf(button) === "check me") || null;
  }

  function checkAndLock(question) {
    if (question.dataset.firstAnswerLocked) return;
    const checkButton = findCheckButton(question);
    if (!checkButton) return;

    question.dataset.firstAnswerLocked = "true";
    checkButton.click();
    question.querySelectorAll('input[type="radio"]').forEach((option) => {
      option.disabled = true;
    });
    checkButton.hidden = true;
  }

  document.addEventListener("change", (event) => {
    const option = event.target;
    if (!(option instanceof HTMLInputElement) || option.type !== "radio" || !option.checked) return;
    const question = option.closest(selector);
    if (!question) return;
    checkAndLock(question);
  });
})();