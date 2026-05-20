const toast = (message) => {
  const wrap = document.querySelector('.toast-container') || (() => {
    const el = document.createElement('div');
    el.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(el);
    return el;
  })();
  const item = document.createElement('div');
  item.className = 'toast show';
  item.innerHTML = `<div class="toast-body">${message}</div>`;
  wrap.appendChild(item);
  setTimeout(() => item.remove(), 3600);
};

document.addEventListener('submit', async (event) => {
  const form = event.target.closest('.ajax-cart-form');
  if (!form) return;
  event.preventDefault();
  const button = form.querySelector('button');
  button.disabled = true;
  button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
  const response = await fetch(form.action, {
    method: 'POST',
    headers: {'X-Requested-With': 'XMLHttpRequest'},
    body: new FormData(form)
  });
  button.disabled = false;
  button.innerHTML = '<i class="bi bi-plus-lg"></i>';
  if (response.ok) {
    const data = await response.json();
    const count = document.querySelector('#cart-count');
    if (count) count.textContent = data.count;
    toast('Added to cart');
  }
});

document.querySelectorAll('.cart-update input').forEach((input) => {
  input.addEventListener('change', async () => {
    const form = input.closest('form');
    const response = await fetch(form.action, {
      method: 'POST',
      headers: {'X-Requested-With': 'XMLHttpRequest'},
      body: new FormData(form)
    });
    if (!response.ok) return;
    const data = await response.json();
    form.closest('.cart-row').querySelector('.line-total').textContent = data.line_total;
    const total = document.querySelector('#cart-total');
    if (total) total.textContent = data.cart_total;
    toast('Cart updated');
  });
});

document.querySelectorAll('.toast').forEach((item) => setTimeout(() => item.remove(), 4200));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, {threshold: 0.12});
document.querySelectorAll('.reveal').forEach((el) => revealObserver.observe(el));

const counters = document.querySelectorAll('.counter');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting || entry.target.dataset.done) return;
    entry.target.dataset.done = '1';
    const target = Number(entry.target.dataset.target || 0);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 45));
    const timer = setInterval(() => {
      current = Math.min(target, current + step);
      entry.target.textContent = `${current}+`;
      if (current >= target) clearInterval(timer);
    }, 24);
  });
}, {threshold: 0.5});
counters.forEach((counter) => counterObserver.observe(counter));

const countdown = document.querySelector('.countdown');
if (countdown) {
  let remaining = Number(countdown.dataset.hours || 8) * 60 * 60;
  setInterval(() => {
    remaining = Math.max(0, remaining - 1);
    const h = String(Math.floor(remaining / 3600)).padStart(2, '0');
    const m = String(Math.floor((remaining % 3600) / 60)).padStart(2, '0');
    const s = String(remaining % 60).padStart(2, '0');
    document.querySelector('#hours').textContent = h;
    document.querySelector('#minutes').textContent = m;
    document.querySelector('#seconds').textContent = s;
  }, 1000);
}

const searchInput = document.querySelector('.live-search');
const suggestions = document.querySelector('#suggestions');
const terms = ['Nike sneakers', 'Apple watch', 'Samsung headphones', 'Zara jacket', 'Rolex watch', 'Beauty kit', 'Home decor', 'Gaming laptop'];
if (searchInput && suggestions) {
  searchInput.addEventListener('input', () => {
    const value = searchInput.value.trim().toLowerCase();
    const matches = terms.filter((term) => term.toLowerCase().includes(value)).slice(0, 5);
    suggestions.innerHTML = matches.map((term) => `<a href="/shop/?q=${encodeURIComponent(term)}"><i class="bi bi-search me-2"></i>${term}</a>`).join('');
    suggestions.classList.toggle('active', value.length > 0 && matches.length > 0);
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.search-shell')) suggestions.classList.remove('active');
  });
}

const themeToggle = document.querySelector('#theme-toggle');
const savedTheme = localStorage.getItem('commerce-theme');
if (savedTheme === 'dark') document.body.classList.add('dark-mode');
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('commerce-theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
  });
}
