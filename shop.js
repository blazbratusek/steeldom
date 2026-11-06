(function () {
  var all = window.STEELDOM_PRODUCTS || [];
  var preview = /[?&]predogled\b/.test(location.search);
  var eur = function (n) { var p = (Math.round(n * 100) / 100).toFixed(n % 1 ? 2 : 0).split('.'); return p[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (p[1] ? ',' + p[1] : '') + ' €'; };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  function img(p, i, cls) {
    var src = p.images && p.images[i];
    return src ? '<img class="' + (cls || '') + '" src="img/izdelki/' + esc(src) + '" alt="' + esc(p.name) + '" loading="lazy">'
               : '<div class="noimg-ph ' + (cls || '') + '"><span>Slika izdelka</span></div>';
  }
  function priceHtml(p) {
    return (p.oldPrice ? '<s>' + eur(p.oldPrice) + '</s> ' : '') + '<b>' + eur(p.price) + '</b>';
  }

  // ---------- Listing ----------
  var grid = document.getElementById('shop-grid');
  if (grid) {
    var list = all.filter(function (p) { return preview || !p.draft; });
    if (!list.length) {
      grid.innerHTML = '<p class="shop-empty">Izdelke pripravljamo. Za povpraševanje nas <a href="index.html#kontakt">kontaktirajte</a>.</p>';
    } else {
      grid.innerHTML = list.map(function (p) {
        return '<a class="pcard" href="izdelek.html?p=' + encodeURIComponent(p.id) + (preview ? '&predogled' : '') + '">' +
          '<div class="pcard-img">' + img(p, 0) + (p.badge ? '<span class="pbadge">' + esc(p.badge) + '</span>' : '') + '</div>' +
          '<div class="pcard-txt"><div class="pcat">' + esc(p.category || '') + '</div><h3>' + esc(p.name) + '</h3>' +
          '<p>' + esc(p.short || '') + '</p><div class="pprice">' + priceHtml(p) + '</div></div></a>';
      }).join('');
    }
  }

  // ---------- Product page ----------
  var root = document.getElementById('product');
  if (!root) return;
  var m = location.search.match(/[?&]p=([^&]+)/);
  var p = m && all.filter(function (x) { return x.id === decodeURIComponent(m[1]); })[0];
  if (!p) {
    root.innerHTML = '<div class="shop-empty"><h1>Izdelek ni najden</h1><p><a href="vrtno-pohistvo.html">Nazaj na vse izdelke</a></p></div>';
    return;
  }
  document.title = p.name + ' – STEELDOM';
  var color = (p.colors && p.colors[0]) || '';
  var thumbs = (p.images || []).length > 1 ? '<div class="thumbs">' + p.images.map(function (s, i) {
    return '<button type="button" data-i="' + i + '"' + (i === 0 ? ' class="on"' : '') + '><img src="img/izdelki/' + esc(s) + '" alt=""></button>';
  }).join('') + '</div>' : '';
  var colorsHtml = (p.colors && p.colors.length) ? '<div class="opt"><div class="opt-l">Barva: <span id="color-name">' + esc(color) + '</span></div><div class="pills">' +
    p.colors.map(function (c, i) { return '<button type="button" class="pill' + (i === 0 ? ' on' : '') + '" data-c="' + esc(c) + '">' + esc(c) + '</button>'; }).join('') + '</div></div>' : '';
  var saving = p.oldPrice ? '<span class="save">Prihranek ' + eur(p.oldPrice - p.price) + '</span>' : '';

  root.innerHTML =
    '<nav class="crumbs"><a href="vrtno-pohistvo.html' + (preview ? '?predogled' : '') + '">Vrtno pohištvo</a> / <span>' + esc(p.name) + '</span></nav>' +
    '<div class="pgrid">' +
      '<div class="gallery"><div class="main-img">' + img(p, 0, 'main') + (p.badge ? '<span class="pbadge">' + esc(p.badge) + '</span>' : '') + '</div>' + thumbs + '</div>' +
      '<div class="pinfo">' +
        '<div class="pcat">' + esc(p.category || '') + '</div><h1>' + esc(p.name) + '</h1>' +
        '<div class="pprice big">' + priceHtml(p) + saving + '</div><div class="vat">Cena vključuje DDV.</div>' +
        colorsHtml +
        '<div class="buy">' +
          (p.stripeLink ? '<a class="btn" id="buy-card" href="#">Kupi s kartico</a>' : '') +
          '<button type="button" class="btn ' + (p.stripeLink ? 'outline' : '') + '" id="buy-invoice">Naroči po predračunu</button>' +
        '</div>' +
        '<ul class="perks"><li><b>Dobavni rok:</b> ' + esc(p.delivery || 'po dogovoru') + '</li>' +
          '<li><b>Dostava:</b> ' + esc(p.shipping || 'po dogovoru') + '</li>' +
          '<li><b>Plačilo:</b> ' + (p.stripeLink ? 'kartica, Apple Pay, Google Pay ali predračun' : 'po predračunu (TRR)') + '</li>' +
          '<li><b>Vračilo:</b> 14 dni za odstop od pogodbe</li></ul>' +
      '</div>' +
    '</div>' +
    '<div class="pdetails"><div><h2>Opis</h2>' + (p.description || []).map(function (t) { return '<p>' + esc(t) + '</p>'; }).join('') + '</div>' +
    '<div><h2>Lastnosti</h2><table class="specs">' + (p.specs || []).map(function (r) { return '<tr><th>' + esc(r[0]) + '</th><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</table></div></div>';

  // gallery
  root.querySelectorAll('.thumbs button').forEach(function (b) {
    b.addEventListener('click', function () {
      root.querySelectorAll('.thumbs button').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var mi = root.querySelector('.main-img img'); if (mi) mi.src = 'img/izdelki/' + p.images[+b.dataset.i];
    });
  });
  // colours
  root.querySelectorAll('.pill').forEach(function (b) {
    b.addEventListener('click', function () {
      root.querySelectorAll('.pill').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on'); color = b.dataset.c;
      document.getElementById('color-name').textContent = color;
    });
  });
  // card (Stripe Payment Link) – colour passed as client_reference_id
  var card = document.getElementById('buy-card');
  if (card) card.addEventListener('click', function (e) {
    e.preventDefault();
    var ref = (p.id + (color ? '__' + color : '')).normalize('NFD').replace(/[^\w-]/g, '_').slice(0, 200);
    location.href = p.stripeLink + (p.stripeLink.indexOf('?') > -1 ? '&' : '?') + 'client_reference_id=' + encodeURIComponent(ref);
  });

  // order by pro-forma invoice (Web3Forms -> info@steeldom.si)
  var dlg = document.getElementById('order-dlg');
  var form = document.getElementById('order-form');
  document.getElementById('buy-invoice').addEventListener('click', function () {
    form.product.value = p.name; form.color.value = color; form.price.value = eur(p.price);
    document.getElementById('order-sum').textContent = p.name + (color ? ' – ' + color : '') + ' · ' + eur(p.price);
    dlg.classList.add('open'); document.body.style.overflow = 'hidden';
  });
  function close() { dlg.classList.remove('open'); document.body.style.overflow = ''; }
  dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.hasAttribute('data-close')) close(); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var out = document.getElementById('order-msg'), btn = form.querySelector('button[type=submit]');
    out.className = 'form-msg'; btn.disabled = true; btn.textContent = 'Pošiljam …';
    form.subject.value = 'NAROČILO: ' + p.name + (color ? ' (' + color + ')' : '') + ' – steeldom.si';
    fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.success) throw new Error();
        out.className = 'form-msg ok';
        out.textContent = 'Hvala! Naročilo smo prejeli. Predračun vam pošljemo na e-pošto v najkrajšem času.';
        form.reset();
      })
      .catch(function () {
        out.className = 'form-msg err';
        out.textContent = 'Naročila ni bilo mogoče poslati. Pišite nam na info@steeldom.si ali pokličite +386 70 557 514.';
      })
      .finally(function () { btn.disabled = false; btn.textContent = 'Oddaj naročilo'; });
  });
})();
