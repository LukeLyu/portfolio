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
    projects.forEach((p) => p.classList.remove('active-project'));
    thumbs.forEach((t) => t.classList.remove('active-project'));
    setLoading(false);
  }

  function injectContent(projectEl, html) {
    const wrapper = document.createElement('div');
    wrapper.className = 'project-injected-content';
    wrapper.innerHTML = html;
    projectEl.querySelectorAll('.project-injected-content').forEach((n) => n.remove());
    projectEl.appendChild(wrapper);
    projectEl.classList.add('sqs-dynamic-data-ready');
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
    setLoading(false);

    if (scrollTop) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  function openFromHash() {
    const url = normalizeHash(window.location.hash);
    if (!url) {
      closeProject();
      return;
    }
    openProject(url, false);
  }

  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', (e) => {
      e.preventDefault();
      const url = thumb.getAttribute('href');
      window.location.hash = url;
    });
  });

  window.addEventListener('hashchange', openFromHash);

  if (window.location.hash && window.location.hash !== '#') {
    body.classList.add('index-loading');
    openFromHash();
  }
})();
