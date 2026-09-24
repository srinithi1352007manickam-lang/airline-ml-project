/**
 * Srinithi - 3D Portfolio Main Logic Engine
 * Preloader, 3D Tilt Physics, Counters, Modals, Command Palette & Interactive Handlers
 */

(function () {
  'use strict';

  // State
  let activeModal = null;

  document.addEventListener('DOMContentLoaded', () => {
    initPreloader();
    initNavbarScroll();
    initIntersectionAnimations();
    initMetricCounters();
    init3DTilt();
    initModals();
    initCommandPalette();
    initContactForm();
    initMobileNav();
    initAudioButtons();
  });

  /* ------------------------------------------------------------------------
     1. PRELOADER
     ------------------------------------------------------------------------ */
  function initPreloader() {
    const preloader = document.getElementById('preloader');
    const progressBar = document.getElementById('preloader-progress');
    const progressText = document.getElementById('preloader-percent');

    if (!preloader) return;

    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.floor(Math.random() * 18) + 10;
      if (progress > 100) progress = 100;

      if (progressBar) progressBar.style.width = progress + '%';
      if (progressText) progressText.textContent = progress + '%';

      if (progress === 100) {
        clearInterval(interval);
        setTimeout(() => {
          preloader.classList.add('loaded');
          // Trigger first reveal
          document.querySelectorAll('.reveal-fade-up, .reveal-fade-left, .reveal-fade-right').forEach((el) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
              el.classList.add('active');
            }
          });
        }, 400);
      }
    }, 45);
  }

  /* ------------------------------------------------------------------------
     2. NAVBAR SCROLL & ACTIVE SPY
     ------------------------------------------------------------------------ */
  function initNavbarScroll() {
    const navbar = document.querySelector('.navbar-hud');
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
      const scrollY = window.pageYOffset;

      if (navbar) {
        if (scrollY > 50) {
          navbar.classList.add('scrolled');
        } else {
          navbar.classList.remove('scrolled');
        }
      }

      // Active section spy
      sections.forEach((section) => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 120;
        const sectionId = section.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          navLinks.forEach((link) => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${sectionId}`) {
              link.classList.add('active');
            }
          });
        }
      });
    }, { passive: true });
  }

  /* ------------------------------------------------------------------------
     3. INTERSECTION OBSERVER ANIMATIONS
     ------------------------------------------------------------------------ */
  function initIntersectionAnimations() {
    const elements = document.querySelectorAll('.reveal-fade-up, .reveal-fade-left, .reveal-fade-right');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    elements.forEach((el) => observer.observe(el));
  }

  /* ------------------------------------------------------------------------
     4. METRIC NUMBER COUNTERS
     ------------------------------------------------------------------------ */
  function initMetricCounters() {
    const counters = document.querySelectorAll('.counter-val');
    let hasCounted = false;

    const metricsSection = document.querySelector('.metrics-section');
    if (!metricsSection) return;

    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !hasCounted) {
        hasCounted = true;
        counters.forEach((counter) => {
          const target = +counter.getAttribute('data-target');
          const duration = 1500;
          const stepTime = 20;
          const totalSteps = duration / stepTime;
          const increment = target / totalSteps;
          let current = 0;

          const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
              counter.textContent = target;
              clearInterval(timer);
            } else {
              counter.textContent = Math.floor(current);
            }
          }, stepTime);
        });
      }
    }, { threshold: 0.3 });

    observer.observe(metricsSection);
  }

  /* ------------------------------------------------------------------------
     5. 3D CARD TILT PHYSICS & SPECULAR GLARE
     ------------------------------------------------------------------------ */
  function init3DTilt() {
    const cards = document.querySelectorAll('.tilt-card');

    cards.forEach((card) => {
      // Inject glare element if missing
      if (!card.querySelector('.tilt-glare-effect')) {
        const glare = document.createElement('div');
        glare.className = 'tilt-glare-effect';
        card.appendChild(glare);
      }

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -12; // tilt angle
        const rotateY = ((x - centerX) / centerX) * 12;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(10px)`;
        card.style.setProperty('--mouse-x', `${(x / rect.width) * 100}%`);
        card.style.setProperty('--mouse-y', `${(y / rect.height) * 100}%`);
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
      });
    });
  }

  /* ------------------------------------------------------------------------
     6. MODAL SYSTEM (CHOCOLATE DEMO & RESUME VIEWER)
     ------------------------------------------------------------------------ */
  function initModals() {
    // Chocolate demo triggers
    document.querySelectorAll('[data-open-demo="chocolate"]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal('choco-modal');
        if (window.ChocolateDemo) window.ChocolateDemo.init();
      });
    });

    // Resume triggers
    document.querySelectorAll('[data-open-modal="resume"]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal('resume-modal');
      });
    });

    // Close buttons
    document.querySelectorAll('.modal-close-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        closeAllModals();
      });
    });

    // Backdrop click
    document.querySelectorAll('.modal-backdrop').forEach((backdrop) => {
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) {
          closeAllModals();
        }
      });
    });

    // ESC key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeAllModals();
      }
    });
  }

  function openModal(modalId) {
    closeAllModals();
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.add('open');
    activeModal = modal;
    document.body.style.overflow = 'hidden';

    if (window.AudioFx) window.AudioFx.playClick();
  }

  function closeAllModals() {
    document.querySelectorAll('.modal-backdrop').forEach((m) => m.classList.remove('open'));
    activeModal = null;
    document.body.style.overflow = '';
  }

  /* ------------------------------------------------------------------------
     7. COMMAND PALETTE (CTRL + K / HUD BUTTON)
     ------------------------------------------------------------------------ */
  function initCommandPalette() {
    const cmdBackdrop = document.getElementById('cmd-modal');
    const cmdInput = document.getElementById('cmd-search-input');
    const cmdList = document.getElementById('cmd-results-list');
    const openBtn = document.getElementById('nav-cmd-btn');

    const commands = [
      { id: 'sec-hero', title: 'Home / Hero Overview', category: 'Navigation', action: () => scrollToSection('hero') },
      { id: 'sec-skills', title: 'Technical Skills Matrix', category: 'Skills', action: () => scrollToSection('skills') },
      { id: 'sec-projects', title: 'Chocolate Ordering Project', category: 'Projects', action: () => scrollToSection('projects') },
      { id: 'demo-choco', title: 'Launch Interactive Chocolate App Demo', category: 'Demo', action: () => openModal('choco-modal') },
      { id: 'sec-education', title: 'Education & Academic Journey', category: 'Education', action: () => scrollToSection('education') },
      { id: 'sec-strengths', title: 'Strengths & Personal Details', category: 'Profile', action: () => scrollToSection('strengths') },
      { id: 'modal-resume', title: 'Open Print-Ready Resume', category: 'Resume', action: () => openModal('resume-modal') },
      { id: 'sec-contact', title: 'Contact Srinithi (Call / Mail / WhatsApp)', category: 'Contact', action: () => scrollToSection('contact') },
      { id: 'copy-email', title: 'Copy Email Address to Clipboard', category: 'Quick Action', action: () => copyText('srinithi1352007manicakm@gmail.com', 'Email address copied!') },
      { id: 'copy-phone', title: 'Copy Phone Number (9345471710)', category: 'Quick Action', action: () => copyText('9345471710', 'Phone number copied!') },
      { id: 'toggle-audio', title: 'Toggle Ambient Synthesizer Sound', category: 'Audio', action: () => { if (window.AudioFx) window.AudioFx.toggleSound(); } }
    ];

    function renderCommandList(filter = '') {
      if (!cmdList) return;
      const filtered = commands.filter((c) =>
        c.title.toLowerCase().includes(filter.toLowerCase()) ||
        c.category.toLowerCase().includes(filter.toLowerCase())
      );

      if (filtered.length === 0) {
        cmdList.innerHTML = `<li style="padding:16px; text-align:center; color:var(--text-muted);">No matching commands found.</li>`;
        return;
      }

      cmdList.innerHTML = filtered.map((c, i) => `
        <li class="cmd-item ${i === 0 ? 'selected' : ''}" data-cmd-id="${c.id}">
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:0.75rem; color:var(--accent-cyan); font-family:'JetBrains Mono',monospace; background:rgba(0,240,255,0.1); padding:2px 8px; border-radius:4px;">${c.category}</span>
            <span style="font-size:0.92rem; color:var(--text-bright);">${c.title}</span>
          </div>
          <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:var(--text-muted);">ENTER ↵</span>
        </li>
      `).join('');

      cmdList.querySelectorAll('.cmd-item').forEach((item) => {
        item.addEventListener('click', () => {
          const cmdId = item.getAttribute('data-cmd-id');
          const targetCmd = commands.find((c) => c.id === cmdId);
          if (targetCmd) {
            closeAllModals();
            targetCmd.action();
          }
        });
      });
    }

    if (openBtn) {
      openBtn.addEventListener('click', () => {
        openModal('cmd-modal');
        renderCommandList();
        setTimeout(() => cmdInput && cmdInput.focus(), 100);
      });
    }

    if (cmdInput) {
      cmdInput.addEventListener('input', (e) => {
        renderCommandList(e.target.value);
      });

      cmdInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const selected = cmdList.querySelector('.cmd-item.selected') || cmdList.querySelector('.cmd-item');
          if (selected) {
            const cmdId = selected.getAttribute('data-cmd-id');
            const targetCmd = commands.find((c) => c.id === cmdId);
            if (targetCmd) {
              closeAllModals();
              targetCmd.action();
            }
          }
        }
      });
    }

    // Ctrl + K or Cmd + K shortcut
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (cmdBackdrop && cmdBackdrop.classList.contains('open')) {
          closeAllModals();
        } else {
          openModal('cmd-modal');
          renderCommandList();
          setTimeout(() => cmdInput && cmdInput.focus(), 100);
        }
      }
    });
  }

  /* ------------------------------------------------------------------------
     8. TOAST NOTIFICATIONS & COPY TO CLIPBOARD
     ------------------------------------------------------------------------ */
  function showToast(message) {
    let toast = document.getElementById('hud-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'hud-toast';
      toast.className = 'toast-hud';
      document.body.appendChild(toast);
    }

    toast.innerHTML = `<span>✨</span><span>${message}</span>`;
    toast.classList.add('show');

    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  function copyText(text, successMsg) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(successMsg);
        if (window.AudioFx) window.AudioFx.playSuccess();
      }).catch(() => {
        fallbackCopyText(text, successMsg);
      });
    } else {
      fallbackCopyText(text, successMsg);
    }
  }

  function fallbackCopyText(text, successMsg) {
    const el = document.createElement('textarea');
    el.value = text;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    showToast(successMsg);
  }

  /* ------------------------------------------------------------------------
     9. CONTACT FORM SIMULATION
     ------------------------------------------------------------------------ */
  function initContactForm() {
    const form = document.getElementById('contact-portfolio-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = form.querySelector('[name="name"]').value.trim();
      const email = form.querySelector('[name="email"]').value.trim();
      const message = form.querySelector('[name="message"]').value.trim();

      if (!name || !email || !message) {
        showToast('Please fill in all fields before sending.');
        return;
      }

      // Simulate sending
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Sending Transmission... 🛰️';

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Message Sent! ✨';
        form.reset();
        showToast(`Thank you, ${name}! Your message has been routed to Srinithi.`);
        if (window.AudioFx) window.AudioFx.playSuccess();

        setTimeout(() => {
          submitBtn.innerHTML = originalText;
        }, 4000);
      }, 1200);
    });
  }

  /* ------------------------------------------------------------------------
     10. MOBILE NAVIGATION DRAWER
     ------------------------------------------------------------------------ */
  function initMobileNav() {
    const toggleBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (toggleBtn && navLinks) {
      toggleBtn.addEventListener('click', () => {
        navLinks.classList.toggle('mobile-open');
        toggleBtn.textContent = navLinks.classList.contains('mobile-open') ? '✕' : '☰';
      });

      navLinks.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          navLinks.classList.remove('mobile-open');
          if (toggleBtn) toggleBtn.textContent = '☰';
        });
      });
    }
  }

  function initAudioButtons() {
    const soundBtn = document.getElementById('sound-toggle-btn');
    if (soundBtn && window.AudioFx) {
      soundBtn.addEventListener('click', () => {
        window.AudioFx.toggleSound();
      });
    }

    // Attach hover blips to buttons
    document.querySelectorAll('.btn, .nav-link, .skill-tag, .metric-card').forEach((el) => {
      el.addEventListener('mouseenter', () => {
        if (window.AudioFx) window.AudioFx.playHover();
      });
    });
  }

  function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // Global exposure
  window.Portfolio = {
    showToast,
    copyText,
    openModal,
    closeAllModals
  };
})();
