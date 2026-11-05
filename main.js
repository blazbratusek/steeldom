(function () {
  // Header background on scroll
  var top = document.querySelector('.top');
  function onScroll() { if (top && !document.body.classList.contains('legal-page')) top.classList.toggle('solid', window.scrollY > 40); }
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

  // Contact form -> Web3Forms, sends to info@steeldom.si
  var form = document.getElementById('contact-form');
  if (form) {
    var out = document.getElementById('form-msg');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      out.className = 'form-msg';
      btn.disabled = true;
      btn.textContent = 'Pošiljam …';
      fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
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

  // ---------- Hero: interactive 3D wireframe of a steel structure ----------
  var cv = document.getElementById('hero-3d');
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Model (units ~ metres, y up)
  var W2 = 2, D2 = 1.5, H = 2.6;
  var edges = [];   // structural edges [a, b]
  var grid = [];    // ground grid edges
  function P(x, y, z) { return [x, y, z]; }
  var posts = [[-W2, -D2], [W2, -D2], [W2, D2], [-W2, D2]];
  posts.forEach(function (p) { edges.push([P(p[0], 0, p[1]), P(p[0], H, p[1])]); });
  for (var i = 0; i < 4; i++) {
    var a = posts[i], b = posts[(i + 1) % 4];
    edges.push([P(a[0], H, a[1]), P(b[0], H, b[1])]);
    edges.push([P(a[0], H - 0.18, a[1]), P(b[0], H - 0.18, b[1])]); // beam depth
  }
  for (var x = -1.5; x <= 1.51; x += 0.5) edges.push([P(x, H, -D2), P(x, H, D2)]);           // roof joists
  for (var s = 0.25; s <= 2.1; s += 0.3) edges.push([P(-W2, s, -D2), P(W2, s, -D2)]);       // slatted back panel
  [[-W2, -D2, 1], [W2, -D2, -1], [W2, D2, -1], [-W2, D2, 1]].forEach(function (p) {          // braces
    edges.push([P(p[0], H - 0.7, p[1]), P(p[0] + 0.7 * p[2], H - 0.18, p[1])]);
  });
  for (var g = -3; g <= 3.01; g += 0.5) {
    grid.push([P(g, 0, -2.5), P(g, 0, 2.5)]);
    if (Math.abs(g) <= 2.51) grid.push([P(-3, 0, g), P(3, 0, g)]);
  }
  var nodes = [];
  posts.forEach(function (p) { nodes.push(P(p[0], 0, p[1]), P(p[0], H, p[1])); });

  var dpr = 1, Wc = 0, Hc = 0, cx = 0, cy = 0, f = 0, alphaMul = 1;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = cv.getBoundingClientRect();
    Wc = r.width; Hc = r.height;
    cv.width = Math.round(Wc * dpr); cv.height = Math.round(Hc * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (Wc <= 620) { cx = Wc * 0.5; cy = Hc * 0.47; f = Math.min(Wc * 0.95, Hc * 1.9); alphaMul = 0.85; }
    else if (Wc < 960) { cx = Wc * 0.72; cy = Hc * 0.36; f = Math.min(Wc * 0.8, Hc * 0.9); alphaMul = 0.45; }
    else { cx = Wc * 0.74; cy = Hc * 0.47; f = Math.min(Wc * 0.62, Hc * 1.1); alphaMul = 1; }
  }

  var yaw = 0.7, pitch = -0.38, tx = 0, ty = 0, mx = 0, my = 0, cam = 9;
  function proj(p) {
    var X = p[0], Y = p[1] - H / 2, Z = p[2];
    var c = Math.cos(yaw), s = Math.sin(yaw);
    var x1 = X * c - Z * s, z1 = X * s + Z * c;
    var cp = Math.cos(pitch), sp = Math.sin(pitch);
    var y2 = Y * cp - z1 * sp, z2 = Y * sp + z1 * cp;
    var k = f / (z2 + cam);
    return [cx + x1 * k, cy - y2 * k, z2];
  }
  function depthA(z) { return Math.max(0.15, Math.min(1, 0.95 - (z + 2.5) / 7)); }
  function line(a, b, col, al, w) {
    ctx.strokeStyle = 'rgba(' + col + ',' + (al * alphaMul).toFixed(3) + ')';
    ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  }

  // Weld spark travelling along structure
  var spark = { e: 0, t: 0, dur: 1.4 };
  function newSpark() { spark.e = Math.floor(Math.random() * edges.length); spark.t = 0; spark.dur = 1.1 + Math.random() * 0.8; }
  newSpark();

  function dim(a, b, label, off) {
    var A = proj(a), B = proj(b);
    var dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy) || 1;
    var nx = -dy / L * off, ny = dx / L * off;
    var a2 = [A[0] + nx, A[1] + ny], b2 = [B[0] + nx, B[1] + ny];
    line(a2, b2, '215,20,30', 0.55, 1);
    line([A[0] + nx * 0.3, A[1] + ny * 0.3], [A[0] + nx * 1.3, A[1] + ny * 1.3], '215,20,30', 0.55, 1);
    line([B[0] + nx * 0.3, B[1] + ny * 0.3], [B[0] + nx * 1.3, B[1] + ny * 1.3], '215,20,30', 0.55, 1);
    ctx.fillStyle = 'rgba(232,90,96,' + (0.85 * alphaMul).toFixed(3) + ')';
    ctx.font = '600 11px Inter, Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(label, (a2[0] + b2[0]) / 2 + nx * 0.9, (a2[1] + b2[1]) / 2 + ny * 0.9 + 4);
  }

  var last = 0, time = 0, running = true;
  function frame(ts) {
    var dt = Math.min(0.05, (ts - last) / 1000 || 0); last = ts; time += dt;
    tx += (mx - tx) * 0.05; ty += (my - ty) * 0.05;
    yaw = 0.72 + Math.sin(time * 0.18) * 0.38 + tx * 0.45;
    pitch = -0.38 - ty * 0.12;
    ctx.clearRect(0, 0, Wc, Hc);

    // blueprint ground grid
    grid.forEach(function (e) {
      var a = proj(e[0]), b = proj(e[1]);
      line(a, b, '150,160,172', 0.07 * depthA((a[2] + b[2]) / 2), 1);
    });
    // structure
    edges.forEach(function (e) {
      var a = proj(e[0]), b = proj(e[1]);
      line(a, b, '206,212,220', 0.62 * depthA((a[2] + b[2]) / 2), 1.25);
    });
    // nodes
    nodes.forEach(function (n) {
      var p = proj(n), al = depthA(p[2]) * alphaMul;
      ctx.fillStyle = 'rgba(230,234,238,' + (0.8 * al).toFixed(3) + ')';
      ctx.fillRect(p[0] - 2.5, p[1] - 2.5, 5, 5);
    });
    // dimensions (CAD look)
    dim(P(-W2, 0, D2), P(W2, 0, D2), '4000', 26);
    dim(P(W2, 0, D2), P(W2, H, D2), '2600', -26);

    // spark
    if (!reduce) {
      spark.t += dt / spark.dur;
      if (spark.t >= 1) newSpark();
      var e = edges[spark.e], a = proj(e[0]), b = proj(e[1]);
      var t = spark.t, px = a[0] + (b[0] - a[0]) * t, py = a[1] + (b[1] - a[1]) * t;
      var t0 = Math.max(0, t - 0.25);
      ctx.strokeStyle = 'rgba(255,90,70,' + (0.9 * alphaMul).toFixed(3) + ')';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0); ctx.lineTo(px, py); ctx.stroke();
      var gr = ctx.createRadialGradient(px, py, 0, px, py, 18);
      gr.addColorStop(0, 'rgba(255,200,150,' + (0.95 * alphaMul).toFixed(3) + ')');
      gr.addColorStop(0.25, 'rgba(255,70,50,' + (0.6 * alphaMul).toFixed(3) + ')');
      gr.addColorStop(1, 'rgba(215,20,30,0)');
      ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(px, py, 18, 0, Math.PI * 2); ctx.fill();
    }
    if (running && !reduce) requestAnimationFrame(frame);
  }

  window.addEventListener('mousemove', function (ev) {
    mx = (ev.clientX / window.innerWidth) * 2 - 1;
    my = (ev.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });
  window.addEventListener('touchmove', function (ev) {
    if (!ev.touches[0]) return;
    mx = (ev.touches[0].clientX / window.innerWidth) * 2 - 1;
  }, { passive: true });
  window.addEventListener('resize', function () { resize(); if (reduce) frame(0); });

  resize();
  if (reduce) { frame(0); return; }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) {
      var vis = en[0].isIntersecting;
      if (vis && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
      running = vis;
    }).observe(cv);
  }
  requestAnimationFrame(frame);
})();
