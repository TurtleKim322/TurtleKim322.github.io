(function () {
  function initializeCategorySidebar() {
    var sidebar = document.querySelector('[data-category-sidebar]');
    if (!sidebar) return;

    var toggle = sidebar.querySelector('.category-sidebar__toggle');
    var menu = sidebar.querySelector('.category-sidebar__menu');
    var groups = sidebar.querySelectorAll('[data-category-group]');
    var storageKey = 'blog-category-open-groups';
    var savedGroups = {};
    sidebar.querySelectorAll('[aria-current="page"]').forEach(function (link) {
      var parent = link.closest('[data-category-group]');
      while (parent) {
        parent.open = true;
        parent = parent.parentElement.closest('[data-category-group]');
      }
    });

    try {
      savedGroups = JSON.parse(window.localStorage.getItem(storageKey) || '{}');
    } catch (error) {
      savedGroups = {};
    }

    groups.forEach(function (group) {
      var key = group.getAttribute('data-category-group');
      var isCurrent = group.closest('.is-current') !== null || group.querySelector('.is-current') !== null;
      if (isCurrent) {
        group.open = true;
      } else if (Object.prototype.hasOwnProperty.call(savedGroups, key)) {
        group.open = savedGroups[key];
      }

      group.addEventListener('toggle', function () {
        try {
          var states = JSON.parse(window.localStorage.getItem(storageKey) || '{}');
          states[key] = group.open;
          window.localStorage.setItem(storageKey, JSON.stringify(states));
        } catch (error) {
          // The accordion remains usable when browser storage is unavailable.
        }
      });
    });

    function updateMobileMenu() {
      var isMobile = window.matchMedia('(max-width: 760px)').matches;
      toggle.hidden = !isMobile;
      if (!isMobile) {
        menu.hidden = false;
        toggle.setAttribute('aria-expanded', 'true');
      } else {
        menu.hidden = toggle.getAttribute('aria-expanded') !== 'true';
      }
    }

    toggle.addEventListener('click', function () {
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      menu.hidden = expanded;
    });

    updateMobileMenu();
    window.addEventListener('resize', updateMobileMenu);


  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCategorySidebar);
  } else {
    initializeCategorySidebar();
  }
}());
