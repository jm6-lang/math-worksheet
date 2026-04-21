// ============================================
// 小二郎资源网 - 交互效果脚本
// 复制到你的主题 JS 文件中
// ============================================

document.addEventListener('DOMContentLoaded', function() {
  
  // ---------- 数字滚动动画 ----------
  function animateCounter(element, target, suffix = '') {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target + suffix;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current) + suffix;
      }
    }, 30);
  }
  
  // 触发数字动画
  const statNumbers = document.querySelectorAll('.stat-number[data-count]');
  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-count'));
        const suffix = el.textContent.includes('TB') ? 'TB+' : 
                       el.textContent.includes('+') ? '+' : '';
        animateCounter(el, target, suffix);
        observer.unobserve(el);
      }
    });
  }, observerOptions);
  
  statNumbers.forEach(num => observer.observe(num));
  
  // ---------- 搜索框焦点效果 ----------
  const searchInput = document.querySelector('.hero-search input');
  const searchBtn = document.querySelector('.hero-search button');
  
  if (searchInput && searchBtn) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        performSearch(searchInput.value);
      }
    });
    
    searchBtn.addEventListener('click', () => {
      performSearch(searchInput.value);
    });
  }
  
  function performSearch(query) {
    if (query.trim()) {
      window.location.href = '/?s=' + encodeURIComponent(query.trim());
    }
  }
  
  // ---------- 分类卡片入场动画 ----------
  const categoryCards = document.querySelectorAll('.category-card');
  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 50);
        cardObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  categoryCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    cardObserver.observe(card);
  });
  
  // ---------- 鼠标跟随光效（可选） ----------
  const heroSection = document.querySelector('.hero-section');
  if (heroSection && !window.matchMedia('(pointer: coarse)').matches) {
    heroSection.addEventListener('mousemove', (e) => {
      const rect = heroSection.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      
      heroSection.style.setProperty('--mouse-x', x + '%');
      heroSection.style.setProperty('--mouse-y', y + '%');
    });
  }
  
  // ---------- 滚动显示导航（可选） ----------
  let lastScroll = 0;
  const header = document.querySelector('header') || document.querySelector('.site-header');
  
  if (header) {
    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll > 100) {
        header.style.background = 'rgba(10, 10, 15, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
      } else {
        header.style.background = 'transparent';
        header.style.backdropFilter = 'none';
      }
      
      lastScroll = currentScroll;
    });
  }
  
});
