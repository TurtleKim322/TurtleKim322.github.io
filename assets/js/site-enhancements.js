(function () {
  var root = document.documentElement;
  var button = document.querySelector('[data-theme-toggle]');
  var storageKey = 'turtlekim-theme';

  function applyTheme(theme, persist) {
    var dark = theme === 'dark';
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    if (button) {
      button.setAttribute('aria-label', dark ? '라이트 모드로 전환' : '다크 모드로 전환');
      button.setAttribute('aria-pressed', String(dark));
      button.querySelector('span').textContent = dark ? '☀' : '☾';
    }
    document.querySelectorAll('iframe.utterances-frame').forEach(function (frame) {
      frame.contentWindow.postMessage({ type: 'set-theme', theme: dark ? 'github-dark' : 'github-light' }, 'https://utteranc.es');
    });
    if (persist) {
      try { window.localStorage.setItem(storageKey, dark ? 'dark' : 'light'); } catch (error) { /* Keep theme usable when storage is blocked. */ }
    }
  }

  var initial = root.getAttribute('data-theme') || 'light';
  applyTheme(initial, false);

  if (button) {
    button.addEventListener('click', function () {
      applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', true);
    });
  }
}());
