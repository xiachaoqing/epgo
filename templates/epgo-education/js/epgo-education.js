/* ========================================
   EPGO教育模板 - JavaScript
   英语陪跑GO | go.xiachaoqing.com
   ======================================== */

(function () {
  'use strict';

  /* -------- 导航栏滚动变色 -------- */
  function initNavScroll() {
    var nav = document.querySelector('.met-head');
    if (!nav) return;
    function onScroll() {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* -------- 滚动进入动画 -------- */
  function initScrollAnimations() {
    var els = document.querySelectorAll('[data-animate]');
    if (!els.length) return;

    if (!window.IntersectionObserver) {
      els.forEach(function (el) { el.classList.add('animated'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var delay = entry.target.dataset.delay || 0;
        setTimeout(function () {
          entry.target.classList.add('animated');
        }, +delay);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    els.forEach(function (el, i) {
      if (!el.dataset.delay) el.dataset.delay = i * 80;
      observer.observe(el);
    });
  }

  /* -------- 数字计数动画 -------- */
  function initCountUp() {
    var nums = document.querySelectorAll('[data-countup]');
    if (!nums.length || !window.IntersectionObserver) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseFloat(el.dataset.countup);
        var suffix = el.dataset.suffix || '';
        var duration = 1400;
        var start = performance.now();

        function update(now) {
          var p = Math.min((now - start) / duration, 1);
          var ease = p === 1 ? 1 : 1 - Math.pow(2, -10 * p);
          var val = target * ease;
          el.textContent = (Number.isInteger(target) ? Math.round(val) : val.toFixed(1)) + suffix;
          if (p < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
        observer.unobserve(el);
      });
    }, { threshold: 0.5 });

    nums.forEach(function (el) { observer.observe(el); });
  }

  /* -------- 平滑滚动 -------- */
  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      var navH = (document.querySelector('.met-head') || {}).offsetHeight || 0;
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - navH - 16, behavior: 'smooth' });
    });
  }

  /* -------- 二维码弹窗 -------- */
  var modal = null;
  function getModal() { return modal || (modal = document.getElementById('qrcode-modal')); }

  function showModal() {
    var m = getModal();
    if (m) { m.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
  }

  function closeModal() {
    var m = getModal();
    if (m) { m.style.display = 'none'; document.body.style.overflow = ''; }
  }

  function initQRModal() {
    var m = getModal();
    if (!m) return;
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
  }

  /* -------- 服务卡片点击 -------- */
  function initServiceCards() {
    document.querySelectorAll('.service-card').forEach(function (card) {
      card.addEventListener('click', function () {
        var a = this.closest('a') || this.querySelector('a');
        if (a && a.href && !/javascript|#$/.test(a.href)) window.location.href = a.href;
      });
    });
  }

  /* -------- 初始化 -------- */
  function init() {
    initNavScroll();
    initScrollAnimations();
    initCountUp();
    initSmoothScroll();
    initQRModal();
    initServiceCards();
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();

  /* -------- 全局 API -------- */
  window.epgoEducation = { showQRCode: showModal, closeQRCode: closeModal };

})();
