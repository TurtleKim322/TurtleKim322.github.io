(function () {
  function initializeCategorySidebar() {
    var sidebar = document.querySelector('[data-category-sidebar]');
    if (!sidebar) return;

    var toggle = sidebar.querySelector('.category-sidebar__toggle');
    var menu = sidebar.querySelector('.category-sidebar__menu');
    var groups = sidebar.querySelectorAll('[data-category-group]');
    var storageKey = 'blog-category-open-groups';
    var savedGroups = {};
    var currentHash = '';

    try {
      currentHash = decodeURIComponent(window.location.hash.slice(1));
    } catch (error) {
      currentHash = window.location.hash.slice(1);
    }

    if (currentHash) {
      groups.forEach(function (group) {
        if (group.getAttribute('data-category-group') === currentHash) {
          group.closest('.category-sidebar__item').classList.add('is-current');
        }
      });

      sidebar.querySelectorAll('a[href*="#"]').forEach(function (link) {
        var linkHash = '';
        try {
          linkHash = decodeURIComponent(new URL(link.href, window.location.href).hash.slice(1));
        } catch (error) {
          linkHash = '';
        }
        if (linkHash === currentHash) {
          link.setAttribute('aria-current', 'page');
          var item = link.closest('li');
          if (item) item.classList.add('is-current');
          var parentGroup = link.closest('[data-category-group]');
          if (parentGroup) parentGroup.open = true;
        }
      });
    }

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
