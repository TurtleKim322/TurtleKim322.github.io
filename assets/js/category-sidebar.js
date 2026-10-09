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

    function filterCategoryArchive() {
      if (!document.querySelector('[data-category-archive]')) return;
      var slug = window.location.hash.slice(1);
      var sections = document.querySelectorAll('[data-category-archive]');
      sections.forEach(function (section) {
        section.classList.remove('is-selected-category', 'is-filter-parent');
        if (section.querySelector(':scope > [data-category-archive]')) section.classList.add('is-category-branch');
      });
      if (!slug) {
        sections.forEach(function (section) { section.hidden = false; });
        return;
      }
      var selected = document.getElementById(decodeURIComponent(slug));
      if (selected && selected.hasAttribute('data-category-archive')) {
        selected.classList.add('is-selected-category');
        var ancestor = selected.parentElement.closest('[data-category-archive]');
        while (ancestor) {
          ancestor.classList.add('is-filter-parent');
          ancestor = ancestor.parentElement.closest('[data-category-archive]');
        }
      }
      sections.forEach(function (section) {
        section.hidden = section.id !== slug && !(selected && section.contains(selected));
      });
      if (selected) selected.scrollIntoView({ block: 'start' });
    }

    filterCategoryArchive();
    window.addEventListener('hashchange', filterCategoryArchive);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCategorySidebar);
  } else {
    initializeCategorySidebar();
  }
}());
