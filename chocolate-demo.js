/**
 * Srinithi - Chocolate Online Ordering Website / App Demo Engine
 * Interactive Storefront Simulator & Figma UI/UX Architecture Inspector
 */

(function () {
  'use strict';

  // Sample verified chocolate catalog
  const products = [
    {
      id: 'choco-1',
      name: 'Belgian Dark Truffle',
      category: 'Artisan Dark',
      desc: '85% Single-origin cocoa shell filled with velvety dark chocolate ganache.',
      price: 249,
      icon: '🍫',
      tag: 'Best Seller'
    },
    {
      id: 'choco-2',
      name: 'Hazelnut Praline Box',
      category: 'Nut Confections',
      desc: 'Slow-roasted hazelnuts blended with delicate milk chocolate and crushed wafer.',
      price: 329,
      icon: '🌰',
      tag: 'Chef Special'
    },
    {
      id: 'choco-3',
      name: 'Caramel Silk Swirl',
      category: 'Gourmet Caramel',
      desc: 'Golden butter caramel infused with Himalayan pink salt in smooth cocoa.',
      price: 199,
      icon: '🍯',
      tag: 'Popular'
    },
    {
      id: 'choco-4',
      name: 'Ruby Berry Velvet',
      category: 'Ruby Cocoa',
      desc: 'Naturally ruby-hued cocoa beans blended with wild raspberry & strawberry crunch.',
      price: 279,
      icon: '🍓',
      tag: 'New Edition'
    }
  ];

  let cart = [];
  let currentTab = 'storefront'; // 'storefront' or 'wireframe'

  function initChocolateDemo() {
    const modalBody = document.getElementById('choco-modal-content');
    if (!modalBody) return;

    renderDemoUI(modalBody);
  }

  function renderDemoUI(container) {
    container.innerHTML = `
      <div class="choco-demo-container">
        <!-- View Mode Switcher -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; flex-wrap:wrap; gap:12px;">
          <div style="display:flex; gap:8px;">
            <button id="tab-storefront-btn" class="btn ${currentTab === 'storefront' ? 'btn-primary' : 'btn-glass'}" style="padding:8px 16px; font-size:0.85rem;">
              🛍️ Live Storefront Demo
            </button>
            <button id="tab-wireframe-btn" class="btn ${currentTab === 'wireframe' ? 'btn-primary' : 'btn-glass'}" style="padding:8px 16px; font-size:0.85rem;">
              🎨 Figma UI/UX Wireframe Mode
            </button>
          </div>
          
          <div class="choco-cart-pill" id="cart-counter-pill" style="cursor:pointer;">
            🛒 Cart: <span id="cart-count">0</span> items (₹<span id="cart-total">0</span>)
          </div>
        </div>

        <div id="demo-dynamic-view">
          ${currentTab === 'storefront' ? renderStorefrontHTML() : renderWireframeHTML()}
        </div>

        <!-- Checkout Success Notice (Hidden by default) -->
        <div id="checkout-success-banner" style="display:none; margin-top:20px; padding:16px 20px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); border-radius:12px; color:#10b981; text-align:center;">
          <h4 style="color:#10b981; margin-bottom:6px;">🎉 Demo Order Simulated Successfully!</h4>
          <p style="font-size:0.9rem; color:#f8fafc;">This demonstrates the user-friendly ordering flow and frictionless checkout interface authored by Srinithi.</p>
        </div>
      </div>
    `;

    bindEvents(container);
  }

  function renderStorefrontHTML() {
    return `
      <div class="choco-demo-hud">
        <div>
          <span style="font-family:'Outfit',sans-serif; font-weight:700; color:#f59e0b; font-size:1.15rem;">Cacao Delights</span>
          <span style="font-size:0.75rem; color:#94a3b8; margin-left:8px; font-family:'JetBrains Mono',monospace;">v1.0 UI Prototype</span>
        </div>
        <div style="font-size:0.82rem; color:#cbd5e1;">
          Designed in Figma • Implemented in HTML/CSS
        </div>
      </div>

      <div class="choco-products-grid">
        ${products.map(p => `
          <div class="choco-card" data-id="${p.id}">
            <span class="choco-badge">${p.tag}</span>
            <div class="choco-thumb">${p.icon}</div>
            <h4 class="choco-name">${p.name}</h4>
            <p class="choco-desc">${p.desc}</p>
            <div class="choco-footer">
              <span class="choco-price">₹${p.price}</span>
              <button class="btn-add-choco" onclick="window.ChocolateDemo.addToCart('${p.id}')">
                + Add
              </button>
            </div>
          </div>
        `).join('')}
      </div>

      <div style="margin-top:24px; display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.3); padding:16px; border-radius:12px; border:1px solid rgba(255,255,255,0.06); flex-wrap:wrap; gap:12px;">
        <div style="font-size:0.88rem; color:#94a3b8;">
          Prototype Status: <strong>Ready for checkout simulation</strong>
        </div>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-glass" style="padding:8px 16px; font-size:0.85rem;" onclick="window.ChocolateDemo.clearCart()">
            Clear Cart
          </button>
          <button class="btn btn-primary" style="padding:8px 20px; font-size:0.85rem;" onclick="window.ChocolateDemo.checkout()">
            Complete Demo Order →
          </button>
        </div>
      </div>
    `;
  }

  function renderWireframeHTML() {
    return `
      <div style="background:rgba(12,18,36,0.9); border:1px solid rgba(157,78,221,0.3); border-radius:14px; padding:24px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:18px;">
          <span style="font-size:1.5rem;">🎨</span>
          <div>
            <h4 style="font-size:1.2rem; color:#ffffff;">Figma / Canva UI/UX Architecture</h4>
            <p style="font-size:0.85rem; color:#94a3b8;">Design System & Information Architecture designed by Srinithi</p>
          </div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px; margin-top:20px;">
          <div style="background:rgba(255,255,255,0.03); border:1px dashed rgba(0,240,255,0.3); border-radius:10px; padding:16px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#00f0ff; margin-bottom:8px;">01. USER JOURNEY</div>
            <h5 style="margin-bottom:6px;">Browse & Discover</h5>
            <p style="font-size:0.82rem; color:#94a3b8;">Clean product listing highlighting flavor notes, cocoa percentage, and pricing for effortless selection.</p>
          </div>

          <div style="background:rgba(255,255,255,0.03); border:1px dashed rgba(157,78,221,0.3); border-radius:10px; padding:16px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#9d4edd; margin-bottom:8px;">02. INTERACTION FLOW</div>
            <h5 style="margin-bottom:6px;">Instant Add-to-Cart</h5>
            <p style="font-size:0.82rem; color:#94a3b8;">Single-click item addition with instantaneous visual counter and real-time total calculation.</p>
          </div>

          <div style="background:rgba(255,255,255,0.03); border:1px dashed rgba(16,185,129,0.3); border-radius:10px; padding:16px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#10b981; margin-bottom:8px;">03. VISUAL STYLING</div>
            <h5 style="margin-bottom:6px;">Warm Cocoa Glassmorphism</h5>
            <p style="font-size:0.82rem; color:#94a3b8;">Rich dark chocolate tones paired with golden amber highlights and modern frosted glass elements.</p>
          </div>
        </div>
      </div>
    `;
  }

  function bindEvents(container) {
    const storefrontBtn = container.querySelector('#tab-storefront-btn');
    const wireframeBtn = container.querySelector('#tab-wireframe-btn');

    if (storefrontBtn) {
      storefrontBtn.addEventListener('click', () => {
        currentTab = 'storefront';
        renderDemoUI(container);
      });
    }

    if (wireframeBtn) {
      wireframeBtn.addEventListener('click', () => {
        currentTab = 'wireframe';
        renderDemoUI(container);
      });
    }

    updateCartDisplay();
  }

  function addToCart(productId) {
    const item = products.find(p => p.id === productId);
    if (!item) return;

    cart.push(item);
    updateCartDisplay();

    if (window.AudioFx) window.AudioFx.playClick();
    if (window.Portfolio) window.Portfolio.showToast(`Added ${item.name} to Chocolate Cart! 🍫`);
  }

  function clearCart() {
    cart = [];
    updateCartDisplay();
    const banner = document.getElementById('checkout-success-banner');
    if (banner) banner.style.display = 'none';
    if (window.Portfolio) window.Portfolio.showToast('Cart cleared');
  }

  function checkout() {
    if (cart.length === 0) {
      if (window.Portfolio) window.Portfolio.showToast('Please add at least one chocolate to cart first! 🍫');
      return;
    }

    const banner = document.getElementById('checkout-success-banner');
    if (banner) {
      banner.style.display = 'block';
      banner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    if (window.AudioFx) window.AudioFx.playSuccess();
    if (window.Portfolio) window.Portfolio.showToast(`Order Placed for ₹${calculateTotal()}! Great experience.`);
  }

  function calculateTotal() {
    return cart.reduce((sum, item) => sum + item.price, 0);
  }

  function updateCartDisplay() {
    const countEl = document.getElementById('cart-count');
    const totalEl = document.getElementById('cart-total');

    if (countEl) countEl.textContent = cart.length;
    if (totalEl) totalEl.textContent = calculateTotal();
  }

  // Expose global controller
  window.ChocolateDemo = {
    init: initChocolateDemo,
    addToCart,
    clearCart,
    checkout
  };
})();
