(() => {
  window.__dubseeUI?.destroy();
  const cleanups = [];
  const effects = new Set();
  cleanups.push(() => { effects.forEach(animation => animation.cancel()); effects.clear(); });
  const on = (target, type, fn, options = {}) => {
    target.addEventListener(type, fn, options);
    cleanups.push(() => target.removeEventListener(type, fn, options));
  };
  const reduced = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const compactMotion = typeof matchMedia === 'function' && matchMedia('(max-width: 980px)').matches;
  window.__dubseeUI = {destroy() { cleanups.splice(0).forEach(fn => fn()); }};

  document.querySelectorAll('.language-option').forEach(link => {
    on(link, 'click', () => { try { localStorage.setItem('dubsee-language', link.dataset.code); } catch (_) {} });
  });
  document.querySelectorAll('.language-picker, .mobile-menu').forEach(picker => {
    const search = picker.querySelector('[data-language-search]');
    if (search) on(search, 'input', () => {
      const value = search.value.toLocaleLowerCase().trim();
      picker.querySelectorAll('.language-option').forEach(link => {
        link.hidden = !link.textContent.toLocaleLowerCase().includes(value) && !link.dataset.code.includes(value);
      });
    });
    picker.querySelectorAll('a').forEach(link => on(link, 'click', () => { picker.open = false; }));
    on(document, 'click', event => { if (!picker.contains(event.target)) picker.open = false; });
    on(document, 'keydown', event => { if (event.key === 'Escape' && picker.open) { picker.open = false; picker.querySelector('summary').focus(); } });
  });

  document.querySelectorAll('[data-gallery-shift]').forEach(button => {
    on(button, 'click', () => {
      const track = button.closest('.gallery-section').querySelector('.gallery-track');
      const cards = track.querySelectorAll('figure');
      const step = cards.length > 1 ? Math.abs(cards[1].getBoundingClientRect().left - cards[0].getBoundingClientRect().left) : track.clientWidth;
      track.scrollBy({left: Number(button.dataset.galleryShift) * step * (getComputedStyle(track).direction === 'rtl' ? -1 : 1), behavior: reduced ? 'instant' : 'smooth'});
    });
  });

  document.querySelectorAll('[data-carousel]').forEach(track => {
    const controls = document.querySelector('[data-controls="' + track.id + '"]');
    if (!controls) return;
    const cards = Array.from(track.children);
    const dots = controls.querySelectorAll('[data-slide]');
    const previous = controls.querySelector('[data-direction="-1"]');
    const next = controls.querySelector('[data-direction="1"]');
    const count = controls.querySelector('[data-carousel-count]');
    let current = -1, frame = 0;
    const setActive = index => {
      if (index === current) return;
      const changed = current >= 0;
      current = index;
      if (changed && !reduced && !compactMotion) {
        const visual = cards[index].querySelector?.('picture img, :scope > svg');
        if (visual && typeof visual.animate === 'function') {
          const photo = visual.tagName.toLowerCase() === 'img';
          const animation = visual.animate(photo ? [{transform:'scale(1.065)',opacity:.78},{transform:'scale(1)',opacity:1}] : [{transform:'translateY(10px) scale(.85)',opacity:.45},{transform:'translateY(0) scale(1)',opacity:1}], {duration:photo?560:420,easing:'cubic-bezier(.2,.8,.3,1)'});
          effects.add(animation);
          animation.onfinish = animation.oncancel = () => effects.delete(animation);
        }
      }
      dots.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.slide) === index)));
      previous.disabled = index === 0;
      next.disabled = index === cards.length - 1;
      controls.style.setProperty('--carousel-progress', String((index + 1) / cards.length));
      if (count) {
        count.textContent = (index + 1) + ' / ' + cards.length;
        if (!reduced && typeof count.animate === 'function') count.animate([{opacity:.2,transform:'translateY(6px)'},{opacity:1,transform:'translateY(0)'}], {duration:250,easing:'ease-out'});
      }
    };
    const update = () => {
      frame = 0;
      const viewport = track.getBoundingClientRect();
      let active = 0, mostVisible = -1, closest = Infinity;
      cards.forEach((card, index) => {
        const rect = card.getBoundingClientRect();
        const visible = Math.max(0, Math.min(rect.right, viewport.right) - Math.max(rect.left, viewport.left));
        const distance = Math.abs((rect.left + rect.right) / 2 - (viewport.left + viewport.right) / 2);
        if (visible > mostVisible + 1 || (Math.abs(visible - mostVisible) <= 1 && distance < closest)) {
          mostVisible = visible; closest = distance; active = index;
        }
      });
      setActive(active);
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
    controls.querySelectorAll('button').forEach(button => on(button, 'click', () => {
      const index = button.hasAttribute('data-slide') ? Number(button.dataset.slide) : Math.max(0, Math.min(cards.length - 1, current + Number(button.dataset.direction)));
      const viewport = track.getBoundingClientRect(), target = cards[index].getBoundingClientRect();
      const style = getComputedStyle(track), rtl = style.direction === 'rtl';
      const inset = parseFloat(style[rtl ? 'paddingRight' : 'paddingLeft']) || 0;
      track.scrollBy({left: rtl ? target.right - (viewport.right - inset) : target.left - (viewport.left + inset), behavior: reduced ? 'instant' : 'smooth'});
    }));
    on(track, 'scroll', schedule, {passive:true});
    on(track, 'scrollend', schedule, {passive:true});
    on(track, 'touchend', schedule, {passive:true});
    on(window, 'resize', schedule, {passive:true});
    if (typeof IntersectionObserver === 'function') {
      const observer = new IntersectionObserver(schedule, {root:track,threshold:[0,.25,.5,.75,1]});
      cards.forEach(card => observer.observe(card));
      cleanups.push(() => observer.disconnect());
    }
    if (typeof ResizeObserver === 'function') {
      const observer = new ResizeObserver(schedule); observer.observe(track);
      cleanups.push(() => observer.disconnect());
    }
    cleanups.push(() => { if (frame) cancelAnimationFrame(frame); });
    update();
  });

  if (!reduced) {
    document.body.classList.add('motion-ready');
    cleanups.push(() => document.body.classList.remove('motion-ready'));
    if (typeof IntersectionObserver === 'function') {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('reveal-visible');
          entry.target.classList.remove('reveal-pending');
          observer.unobserve(entry.target);
        });
      }, {threshold:.08,rootMargin:'0px 0px -18px 0px'});
      const viewportBottom = (window.innerHeight || 0) * 0.92;
      document.querySelectorAll('.section-heading, .steps li, .story, .feature-card, .feature-tags').forEach(element => {
        if (compactMotion) {
          if (element.closest('[data-carousel]')) return;
          const rect = element.getBoundingClientRect();
          if (rect.top < viewportBottom && rect.bottom > 0) return;
        }
        const siblings = Array.from(element.parentElement.children);
        element.style.setProperty('--reveal-delay', (Math.max(0, siblings.indexOf(element)) % 3) * 90 + 'ms');
        element.classList.add('reveal-pending'); observer.observe(element);
        cleanups.push(() => element.classList.remove('reveal-pending','reveal-visible'));
      });
      cleanups.push(() => observer.disconnect());
    }
  }
})();
