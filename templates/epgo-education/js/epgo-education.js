/* 英语陪跑GO - 主JS */
(function () {
  'use strict';

  /* 导航滚动变色 */
  function initNavScroll() {
    var nav = document.getElementById('mainNav');
    if (!nav) return;
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  /* 滚动进入动画 */
  function initAnimate() {
    var els = document.querySelectorAll('[data-animate]');
    if (!els.length || !window.IntersectionObserver) {
      els.forEach(function(el){ el.classList.add('animated'); });
      return;
    }
    var ob = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) { e.target.classList.add('animated'); ob.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function(el){ ob.observe(el); });
  }

  /* 数字动画 */
  function initCountUp() {
    var els = document.querySelectorAll('[data-countup]');
    if (!els.length || !window.IntersectionObserver) return;
    var ob = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        var el = e.target, target = +el.dataset.countup, suffix = el.dataset.suffix || '';
        var start = performance.now(), dur = 1200;
        function tick(now) {
          var p = Math.min((now - start) / dur, 1);
          var ease = 1 - Math.pow(1 - p, 3);
          el.textContent = (Number.isInteger(target) ? Math.round(target * ease) : (target * ease).toFixed(1)) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        ob.unobserve(el);
      });
    }, { threshold: 0.5 });
    els.forEach(function(el){ ob.observe(el); });
  }

  /* 平滑锚点 */
  function initScroll() {
    document.addEventListener('click', function(e){
      var a = e.target.closest('a[href^="#"]');
      if (!a || a.getAttribute('href') === '#') return;
      var t = document.querySelector(a.getAttribute('href'));
      if (!t) return;
      e.preventDefault();
      var navH = (document.getElementById('mainNav') || {}).offsetHeight || 60;
      window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - navH - 12, behavior: 'smooth' });
    });
  }

  /* 弹窗 */
  function getModal() { return document.getElementById('qrcode-modal'); }

  function initModal() {
    var m = getModal();
    if (!m) return;
    m.addEventListener('click', function(e){ if (e.target === m) closeModal(); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeModal(); });
  }

  function showModal() {
    var m = getModal();
    if (m) { m.classList.add('show'); document.body.style.overflow = 'hidden'; }
  }

  function closeModal() {
    var m = getModal();
    if (m) { m.classList.remove('show'); document.body.style.overflow = ''; }
  }

  /* 手机导航 */
  function toggleNav(btn) {
    var menu = document.getElementById('navMenu');
    if (!menu) return;
    menu.classList.toggle('show');
  }

  /* 初始化 */
  function init() {
    initNavScroll();
    initAnimate();
    initCountUp();
    initScroll();
    initModal();
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();

  window.epgoEducation = {
    showQRCode: showModal,
    closeQRCode: closeModal,
    toggleNav: toggleNav
  };
})();
