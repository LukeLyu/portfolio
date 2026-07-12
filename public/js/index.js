(function () {
  const body = document.body;
  const projectPages = document.getElementById('projectPages');
  if (!projectPages) return;

  const projects = Array.from(projectPages.querySelectorAll('.project.page-project'));
  const thumbs = Array.from(document.querySelectorAll('#projectThumbs a.project'));
  const cache = new Map();

  function normalizeHash(hash) {
    if (!hash || hash === '#') return '';
    let path = hash.replace(/^#/, '');
    if (!path.startsWith('/')) path = '/' + path;
    if (!path.endsWith('/')) path += '/';
    return path;
  }

  function findProject(url) {
    return projects.find((p) => p.getAttribute('data-url') === url);
  }

  function setLoading(loading) {
    body.classList.toggle('index-loading', loading);
  }

  function closeProject() {
    body.classList.remove('index-page-open', 'page-open');
    projectPages.classList.remove('page-open');
    projects.forEach((p) => p.classList.remove('active-project'));
    thumbs.forEach((t) => t.classList.remove('active-project'));
    setLoading(false);
  }

  function injectContent(projectEl, html) {
    const wrapper = document.createElement('div');
    wrapper.className = 'project-injected-content';
    wrapper.innerHTML = html;
    projectEl.querySelectorAll('.project-injected-content').forEach((n) => n.remove());
    const source = projectEl.querySelector('.project-content-source');
    if (source) {
      projectEl.insertBefore(wrapper, source);
    } else {
      projectEl.appendChild(wrapper);
    }
    projectEl.classList.add('sqs-dynamic-data-ready');
    wrapper.querySelectorAll('.image-block-outer-wrapper').forEach((el) => {
      el.classList.add('sqs-text-ready', 'animation-loaded');
    });
  }

  function updateProjectNav(url) {
    const nav = projectPages.querySelector('#projectNav');
    if (!nav) return;

    const idx = projects.findIndex((p) => p.getAttribute('data-url') === url);
    const prevSpan = nav.querySelector('.prev-project');
    const nextSpan = nav.querySelector('.next-project');
    if (!prevSpan || !nextSpan) return;

    if (idx > 0) {
      prevSpan.classList.remove('disabled');
      prevSpan.dataset.url = projects[idx - 1].getAttribute('data-url');
    } else {
      prevSpan.classList.add('disabled');
      delete prevSpan.dataset.url;
    }

    if (idx >= 0 && idx < projects.length - 1) {
      nextSpan.classList.remove('disabled');
      nextSpan.dataset.url = projects[idx + 1].getAttribute('data-url');
    } else {
      nextSpan.classList.add('disabled');
      delete nextSpan.dataset.url;
    }
  }

  async function loadProjectContent(projectEl) {
    if (projectEl.classList.contains('sqs-dynamic-data-ready')) return;

    const source = projectEl.querySelector('.project-content-source');
    if (source) {
      injectContent(projectEl, source.innerHTML);
      return;
    }

    const url = projectEl.getAttribute('data-url');
    if (cache.has(url)) {
      injectContent(projectEl, cache.get(url));
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(url);
      const text = await res.text();
      const doc = new DOMParser().parseFromString(text, 'text/html');
      const content = doc.querySelector('#page .content')?.innerHTML || '';
      cache.set(url, content);
      injectContent(projectEl, content);
    } finally {
      setLoading(false);
    }
  }

  async function openProject(url, scrollTop) {
    const projectEl = findProject(url);
    if (!projectEl) return;

    closeProject();
    setLoading(true);

    await loadProjectContent(projectEl);

    projectEl.classList.add('active-project');
    const thumb = thumbs.find((t) => t.getAttribute('href') === url);
    if (thumb) thumb.classList.add('active-project');

    body.classList.add('index-page-open', 'page-open');
    projectPages.classList.add('page-open');
    updateProjectNav(url);
    setLoading(false);

    if (scrollTop) {
      window.scrollTo({ top: 0, behavior: 'instant' in document.documentElement.style ? 'instant' : 'auto' });
    }
  }

  function openFromHash() {
    const url = normalizeHash(window.location.hash);
    if (!url) {
      closeProject();
      return;
    }
    const switchingProject = body.classList.contains('page-open');
    openProject(url, switchingProject);
  }

  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', (e) => {
      e.preventDefault();
      const url = thumb.getAttribute('href');
      window.location.hash = url;
    });
  });

  projectPages.addEventListener('click', (e) => {
    const backLink = e.target.closest('.back-to-work');
    if (backLink) {
      e.preventDefault();
      if (window.location.hash) {
        window.location.hash = '';
      } else {
        closeProject();
      }
      return;
    }

    const prev = e.target.closest('.prev-project:not(.disabled)');
    if (prev?.dataset.url) {
      e.preventDefault();
      window.location.hash = prev.dataset.url;
      return;
    }

    const next = e.target.closest('.next-project:not(.disabled)');
    if (next?.dataset.url) {
      e.preventDefault();
      window.location.hash = next.dataset.url;
    }
  });

  window.addEventListener('hashchange', openFromHash);

  if (window.location.hash && window.location.hash !== '#') {
    body.classList.add('index-loading');
    openFromHash();
  }
})();
