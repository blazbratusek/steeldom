(function () {
  // Header background on scroll
  var top = document.querySelector('.top');
  function onScroll() { if (top) top.classList.toggle('solid', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); burger.setAttribute('aria-expanded', false); });
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  // "Povpraševanje" on a model pre-fills the form
  document.querySelectorAll('[data-model]').forEach(function (b) {
    b.addEventListener('click', function () {
      var sel = document.getElementById('f-type');
      var msg = document.getElementById('f-msg');
      if (sel) sel.value = b.getAttribute('data-model');
      if (msg && !msg.value) msg.value = 'Zanima me model ' + b.getAttribute('data-model') + '. ';
    });
  });

  // Contact form -> Web3Forms (free), sends to info@steeldom.si
  var form = document.getElementById('contact-form');
  if (form) {
    var out = document.getElementById('form-msg');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      out.className = 'form-msg';
      btn.disabled = true;
      btn.textContent = 'Pošiljam …';
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.success) {
            out.className = 'form-msg ok';
            out.textContent = 'Hvala! Vaše sporočilo smo prejeli in se vam oglasimo v najkrajšem času.';
            form.reset();
          } else { throw new Error(); }
        })
        .catch(function () {
          out.className = 'form-msg err';
          out.textContent = 'Sporočila ni bilo mogoče poslati. Pišite nam na info@steeldom.si ali pokličite +386 70 557 514.';
        })
        .finally(function () { btn.disabled = false; btn.textContent = 'Pošlji povpraševanje'; });
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
