(function () {
  'use strict';

  // Scope formatting to the four explicitly marked Home ordinals.
  const selector = '[data-tur-number-format="ordinal-2"][fs-numbercount-element="number"]';
  const observerKey = Symbol.for('tur.ai.ordinal-2.observer');

  function init() {
    document.querySelectorAll(selector).forEach(function (element) {
      if (element[observerKey]) return;

      function format() {
        const text = element.textContent;
        if (!/^\d{1,2}$/.test(text)) return;
        const formatted = text.padStart(2, '0');
        // An observer also sees its own write; equality makes that callback a no-op.
        if (formatted !== text) element.textContent = formatted;
      }

      const observer = new MutationObserver(format);
      observer.observe(element, { childList: true, characterData: true, subtree: true });
      Object.defineProperty(element, observerKey, { value: observer });
      format();
    });
  }

  // Footer DOM already exists. Install before the deferred Number Count initializes.
  init();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  }
})();
