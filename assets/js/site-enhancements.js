(function () {
  var root = document.documentElement;
  var button = document.querySelector('[data-theme-toggle]');
  var storageKey = 'turtlekim-theme';

  function syncUtterancesTheme() {
    var theme = root.getAttribute('data-theme') === 'dark' ? 'github-dark' : 'github-light';
    document.querySelectorAll('iframe.utterances-frame').forEach(function (frame) {
      if (!frame.dataset.themeSyncBound) {
        frame.addEventListener('load', function () {
          frame.contentWindow.postMessage({ type: 'set-theme', theme: themeFromRoot() }, 'https://utteranc.es');
        });
        frame.dataset.themeSyncBound = 'true';
      }
      frame.contentWindow.postMessage({ type: 'set-theme', theme: theme }, 'https://utteranc.es');
    });
  }

  function themeFromRoot() {
    return root.getAttribute('data-theme') === 'dark' ? 'github-dark' : 'github-light';
  }

  function applyTheme(theme, persist) {
    var dark = theme === 'dark';
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    if (button) {
      button.setAttribute('aria-label', dark ? '라이트 모드로 전환' : '다크 모드로 전환');
      button.setAttribute('aria-pressed', String(dark));
      button.querySelector('span').textContent = dark ? '☀' : '☾';
    }
    syncUtterancesTheme();
    if (persist) {
      try { window.localStorage.setItem(storageKey, dark ? 'dark' : 'light'); } catch (error) { /* Keep theme usable when storage is blocked. */ }
    }
  }

  if (window.MutationObserver) {
    new MutationObserver(syncUtterancesTheme).observe(document.documentElement, { childList: true, subtree: true });
  }
  window.addEventListener('load', syncUtterancesTheme);

  var initial = root.getAttribute('data-theme') || 'light';
  applyTheme(initial, false);

  if (button) {
    button.addEventListener('click', function () {
      applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', true);
    });
  }
}());
