(function () {
  var root = document.documentElement;
  var themeBtn = document.querySelector('.theme');
  themeBtn.addEventListener('click', function () {
    var dark = root.dataset.theme
      ? root.dataset.theme === 'dark'
      : window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
  });

  var menu = document.querySelector('.menu');
  menu.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    menu.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('.side a').forEach(function (a) {
    a.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
  });

  // 本頁目錄：捲動時標出目前段落
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  var heads = links.map(function (a) { return document.getElementById(decodeURIComponent(a.hash.slice(1))); });
  function onScroll() {
    var y = window.scrollY + 120, idx = -1;
    heads.forEach(function (h, i) { if (h && h.offsetTop <= y) idx = i; });
    links.forEach(function (a, i) { a.classList.toggle('on', i === idx); });
  }
  if (links.length) { window.addEventListener('scroll', onScroll, { passive: true }); onScroll(); }
})();
