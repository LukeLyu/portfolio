(function () {
  const mobileMenuLink = document.getElementById('mobileMenuLink');
  const mobileNav = document.getElementById('mobileNav');

  if (mobileMenuLink && mobileNav) {
    mobileMenuLink.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
      document.body.classList.toggle('mobile-nav-open');
    });
  }

  document.querySelectorAll('#mobileNav a').forEach((link) => {
    link.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      document.body.classList.remove('mobile-nav-open');
    });
  });
})();
