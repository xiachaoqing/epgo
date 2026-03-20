/* ========================================
   EPGO教育模板 - JavaScript功能脚本
   ======================================== */

(function() {
  'use strict';

  // 初始化函数
  function init() {
    initServiceCards();
    initContentItems();
    initScrollAnimations();
    initQRCodeModal();
    initSmoothScroll();
  }

  // 服务卡片交互效果
  function initServiceCards() {
    const cards = document.querySelectorAll('.service-card');
    cards.forEach((card, index) => {
      // 添加延迟动画
      card.style.animationDelay = (index * 0.1) + 's';

      // 添加点击事件
      card.addEventListener('click', function(e) {
        const link = this.querySelector('a');
        if (link) {
          window.location.href = link.href;
        }
      });
    });
  }

  // 内容项目交互效果
  function initContentItems() {
    const items = document.querySelectorAll('.content-item');
    items.forEach((item) => {
      item.addEventListener('mouseenter', function() {
        this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.15)';
      });

      item.addEventListener('mouseleave', function() {
        this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
      });
    });
  }

  // 滚动动画
  function initScrollAnimations() {
    const elements = document.querySelectorAll('[data-animate]');

    if (!window.IntersectionObserver) {
      // 降级处理
      elements.forEach(el => {
        el.classList.add('animated');
      });
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    });

    elements.forEach(el => {
      observer.observe(el);
    });
  }

  // 二维码弹窗
  function initQRCodeModal() {
    const qrcodeBtn = document.getElementById('qrcode-modal-btn');
    const modal = document.getElementById('qrcode-modal');
    const closeBtn = document.querySelector('.qrcode-modal-close');

    if (!qrcodeBtn) return;

    qrcodeBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        if (modal) {
          modal.style.display = 'none';
          document.body.style.overflow = 'auto';
        }
      });
    }

    if (modal) {
      modal.addEventListener('click', function(e) {
        if (e.target === modal) {
          modal.style.display = 'none';
          document.body.style.overflow = 'auto';
        }
      });
    }
  }

  // 平滑滚动
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;

        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  // 页面加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 导出全局函数
  window.epgoEducation = {
    // 公众号二维码弹窗
    showQRCode: function() {
      const modal = document.getElementById('qrcode-modal');
      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }
    },

    closeQRCode: function() {
      const modal = document.getElementById('qrcode-modal');
      if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
      }
    },

    // 滚动到指定元素
    scrollTo: function(selector) {
      const element = document.querySelector(selector);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };
})();
