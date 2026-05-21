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

const chatAssistant = document.querySelector('#chat-assistant');
const chatToggle = document.querySelector('#chat-toggle');
const chatClose = document.querySelector('#chat-close');
const chatPanel = document.querySelector('#chat-panel');
const chatMessages = document.querySelector('#chat-messages');
const chatForm = document.querySelector('#chat-form');
const chatInput = document.querySelector('#chat-input');

const chatAnswers = [
  {
    keywords: ['order', 'track', 'tracking', 'delivery status', 'where is'],
    answer: 'You can track your order from the Orders page after logging in. Open <a href="/orders/">Track order</a> to see your latest order status.'
  },
  {
    keywords: ['shipping', 'delivery', 'ship', 'days', 'free shipping'],
    answer: 'Standard delivery usually takes 3-5 business days. Orders above Rs. 999 qualify for free shipping.'
  },
  {
    keywords: ['return', 'refund', 'exchange', 'replace'],
    answer: 'Returns and exchanges are accepted for eligible items in unused condition. Visit the FAQ page for the full return steps.'
  },
  {
    keywords: ['payment', 'pay', 'card', 'upi', 'cash', 'cod', 'paypal'],
    answer: 'CommercePro supports secure checkout with cards, wallets, PayPal-style payments, and phone payments shown in the footer.'
  },
  {
    keywords: ['cart', 'bag', 'checkout', 'buy'],
    answer: 'Open your <a href="/cart/">cart</a> to review items, update quantities, and continue to checkout.'
  },
  {
    keywords: ['wishlist', 'favorite', 'heart', 'save'],
    answer: 'Use the heart icon on products to save favorites. Logged-in users can open their wishlist from the header.'
  },
  {
    keywords: ['login', 'account', 'register', 'profile', 'password'],
    answer: 'For account help, use the Login page to sign in, create an account, or reset your password.'
  },
  {
    keywords: ['contact', 'support', 'email', 'phone', 'human', 'agent'],
    answer: 'This chatbot works offline. For direct support, send your details from the <a href="/contact/">Contact</a> page.'
  },
  {
    keywords: ['sale', 'discount', 'coupon', 'offer'],
    answer: 'Flash sale offers are shown at the top of the site. You can also join the newsletter for new drops and coupons.'
  }
];

const addChatMessage = (message, type = 'bot') => {
  if (!chatMessages) return;
  const item = document.createElement('div');
  item.className = `chat-message ${type}`;
  if (type === 'user') item.textContent = message;
  else item.innerHTML = message;
  chatMessages.appendChild(item);
  chatMessages.scrollTop = chatMessages.scrollHeight;
};

const getChatAnswer = (message) => {
  const normalized = message.toLowerCase();
  const match = chatAnswers.find((item) => item.keywords.some((keyword) => normalized.includes(keyword)));
  if (match) return match.answer;
  return 'I can help with orders, shipping, returns, payment, cart, wishlist, account, and contact questions. Try asking "track my order" or "return policy".';
};

const openChat = () => {
  if (!chatAssistant || !chatToggle || !chatPanel) return;
  chatAssistant.classList.add('open');
  chatToggle.setAttribute('aria-expanded', 'true');
  chatPanel.setAttribute('aria-hidden', 'false');
  if (chatMessages && !chatMessages.dataset.started) {
    chatMessages.dataset.started = '1';
    addChatMessage('Hi! I am your offline CommercePro assistant. Ask me about orders, delivery, returns, payments, cart, or account help.');
  }
  setTimeout(() => chatInput?.focus(), 80);
};

const closeChat = () => {
  if (!chatAssistant || !chatToggle || !chatPanel) return;
  chatAssistant.classList.remove('open');
  chatToggle.setAttribute('aria-expanded', 'false');
  chatPanel.setAttribute('aria-hidden', 'true');
};

if (chatAssistant && chatToggle) {
  chatToggle.addEventListener('click', () => {
    if (chatAssistant.classList.contains('open')) closeChat();
    else openChat();
  });
  chatClose?.addEventListener('click', closeChat);
  chatForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;
    addChatMessage(message, 'user');
    chatInput.value = '';
    setTimeout(() => addChatMessage(getChatAnswer(message)), 260);
  });
  document.querySelectorAll('[data-chat-prompt]').forEach((button) => {
    button.addEventListener('click', () => {
      const prompt = button.dataset.chatPrompt;
      addChatMessage(prompt, 'user');
      setTimeout(() => addChatMessage(getChatAnswer(prompt)), 220);
    });
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeChat();
  });
  document.addEventListener('click', (event) => {
    if (!chatAssistant.contains(event.target)) closeChat();
  });
}
