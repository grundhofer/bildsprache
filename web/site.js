/* Bildsprache – Seitenverhalten. Ohne Abhängigkeiten; jede Funktion prüft, ob ihre Elemente existieren. */
(function () {
  'use strict';
  var T = {};
  try { T = JSON.parse(document.getElementById('i18n').textContent); } catch (e) { /* Seiten ohne Texte */ }
  function t(key) { return T[key] || key; }
  var status = document.getElementById('status');
  function announce(text) {
    if (!status) return;
    status.textContent = '';
    setTimeout(function () { status.textContent = text; }, 30);
  }

  /* ---------- Kopieren ---------- */
  function copyText(text, button) {
    function done(ok) {
      announce(ok ? t('copied') : t('copyFailed'));
      if (!button) return;
      var old = button.dataset.label || button.textContent;
      button.dataset.label = old;
      button.textContent = ok ? t('copied') : t('copyFailed');
      button.setAttribute('data-copied', '');
      setTimeout(function () { button.textContent = old; button.removeAttribute('data-copied'); }, 1600);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(fallback(text, button)); });
    } else { done(fallback(text, button)); }
  }
  function fallback(text, button) {
    // Im offenen Dialog ist alles außerhalb inert; das Textfeld muss deshalb im Dialog liegen.
    var host = (button && button.closest('dialog')) || document.body;
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0'; ta.style.top = '0';
    host.appendChild(ta);
    ta.focus(); ta.select();
    var ok = false;
    try { ok = document.activeElement === ta && document.execCommand('copy'); } catch (e) { ok = false; }
    host.removeChild(ta);
    if (button) button.focus({ preventScroll: true });
    return ok;
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-copy]');
    if (!b) return;
    var src = b.getAttribute('data-copy');
    var text = src.charAt(0) === '#' ? (document.querySelector(src) || {}).textContent : src;
    if (text) copyText(text.trim(), b);
  });

  /* ---------- Vergleichsregler ---------- */
  function bindCompare(root) {
    (root || document).querySelectorAll('.cmp input[type="range"]').forEach(function (r) {
      if (r.dataset.bound) return;
      r.dataset.bound = '1';
      var box = r.closest('.cmp');
      function set() {
        box.style.setProperty('--pos', r.value + '%');
        r.setAttribute('aria-valuetext', r.value + ' %');
      }
      r.addEventListener('input', set); set();
    });
  }
  bindCompare();

  /* Startseite: Stil im Vergleichsregler wechseln */
  document.querySelectorAll('[data-hero-pick]').forEach(function (chip) {
    chip.addEventListener('click', function () {
      var box = document.getElementById(chip.dataset.heroPick);
      if (!box) return;
      var img = box.querySelector('.cmp-top img');
      img.src = chip.dataset.src; img.alt = chip.dataset.alt;
      box.querySelector('.cmp-lab.l').textContent = chip.dataset.label;
      var link = document.getElementById(chip.dataset.heroPick + '-link');
      if (link) { link.href = chip.dataset.href; link.textContent = chip.dataset.label; }
      document.querySelectorAll('[data-hero-pick="' + chip.dataset.heroPick + '"]').forEach(function (c) {
        c.setAttribute('aria-pressed', String(c === chip));
      });
    });
  });

  /* ---------- Filter im Bildraster ---------- */
  document.querySelectorAll('[data-filter-for]').forEach(function (group) {
    var grid = document.getElementById(group.dataset.filterFor);
    var tally = document.getElementById(group.dataset.filterFor + '-tally');
    group.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-filter]');
      if (!chip) return;
      var value = chip.dataset.filter;
      group.querySelectorAll('[data-filter]').forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      var shown = 0;
      // data-cat kann mehrere Werte tragen (Stilübersicht: alle Anwendungen eines Stils)
      grid.querySelectorAll('[data-cat]').forEach(function (card) {
        var on = value === '*' || card.dataset.cat.split(' ').indexOf(value) >= 0;
        card.hidden = !on; if (on) shown++;
        if (on && card.dataset.srcs) {
          var srcs = JSON.parse(card.dataset.srcs), img = card.querySelector('img');
          if (!img.dataset.src0) { img.dataset.src0 = img.getAttribute('src'); img.dataset.alt0 = img.alt; }
          var pick = srcs[value] || [img.dataset.src0, img.dataset.alt0];
          img.src = pick[0]; img.alt = pick[1];
        }
      });
      // Abschnitte ohne sichtbare Karte ausblenden
      grid.querySelectorAll('[data-group]').forEach(function (sec) {
        sec.hidden = !sec.querySelector('[data-cat]:not([hidden])');
      });
      var unit = group.dataset.unit || 'image';
      if (tally) tally.textContent = shown + ' ' + t(shown === 1 ? unit : unit + 's');
    });
  });

  /* Klebende Leiste: Höhe als Abstand für Sprungziele und Fokus (scroll-padding) */
  var bar = document.querySelector('.bar');
  function barHeight() { if (bar) document.documentElement.style.setProperty('--bar-h', bar.offsetHeight + 'px'); }
  barHeight();
  window.addEventListener('resize', barHeight);

  /* ---------- Lightbox ---------- */
  var dataEl = document.getElementById('cells-data');
  var dlg = document.getElementById('lb');
  if (dataEl && dlg) {
    var cells = JSON.parse(dataEl.textContent);
    var current = -1, opener = null, downOnBackdrop = false;
    var $ = function (sel) { return dlg.querySelector(sel); };
    var live = $('.lb-live');
    function visibleIndexes() {
      var out = [];
      document.querySelectorAll('[data-cell]').forEach(function (b) {
        var card = b.closest('[data-cat]') || b.closest('.card');
        if (!card || !card.hidden) out.push(Number(b.dataset.cell));
      });
      return out;
    }
    function seg(kind, label, text) {
      var d = document.createElement('div');
      d.className = 'seg seg-' + kind;
      var i = document.createElement('i'); i.textContent = label; d.appendChild(i);
      var s = document.createElement('span'); s.lang = 'en'; s.textContent = text; d.appendChild(s);
      return d;
    }
    function keepFocus(el, fallbackEl, had) {
      // Ein Bedienelement, das deaktiviert oder versteckt wird, darf den Fokus nicht verlieren. Geprüft wird der Fokus
      // von vor dem Umbau (had): Sobald ein Knopf deaktiviert ist, steht document.activeElement schon auf <body>.
      if (had === el && (el.disabled || el.hidden)) fallbackEl.focus();
    }
    function render(i, announceIt) {
      var c = cells[i]; current = i;
      var had = document.activeElement;
      var fig = $('.lb-fig'); fig.innerHTML = '';
      fig.className = 'lb-fig ' + c.ar;
      if (c.base && $('[data-lb-compare]').getAttribute('aria-pressed') === 'true') {
        fig.innerHTML = '<div class="cmp ' + c.ar + '"><img alt=""><div class="cmp-top"><img alt=""></div>' +
          '<input type="range" min="0" max="100" value="50"><span class="cmp-line"></span>' +
          '<span class="cmp-lab l"></span><span class="cmp-lab r"></span></div>';
        var imgs = fig.querySelectorAll('img');
        imgs[0].src = c.base; imgs[0].alt = c.baseAlt;
        imgs[1].src = c.src; imgs[1].alt = c.alt;
        fig.querySelector('input').setAttribute('aria-label', t('compareSlider') + ': ' + c.title);
        fig.querySelector('.cmp-lab.l').textContent = c.title;
        fig.querySelector('.cmp-lab.r').textContent = t('baseline');
        bindCompare(fig);
      } else {
        var img = document.createElement('img');
        img.src = c.src; img.alt = c.alt; img.width = c.w; img.height = c.h;
        fig.appendChild(img);
      }
      var cmpBtn = $('[data-lb-compare]');
      cmpBtn.hidden = !c.base;
      $('.lb-eyebrow').textContent = c.eyebrow;
      var h = $('.lb-title'); h.textContent = '';
      if (c.href) { var a = document.createElement('a'); a.href = c.href; a.textContent = c.title; h.appendChild(a); }
      else h.textContent = c.title;
      $('.lb-sub').textContent = c.sub || '';
      var an = $('.anat'); an.innerHTML = '';
      c.parts.forEach(function (p) { an.appendChild(seg(p[0], t('part_' + p[0]), p[1])); });
      $('[data-lb-copy-all]').dataset.text = c.prompt;
      var cs = $('[data-lb-copy-style]');
      cs.hidden = !c.styleBlock; cs.dataset.text = c.styleBlock || '';
      var ct = $('[data-lb-copy-tpl]');
      ct.hidden = !c.tpl; ct.dataset.text = c.tpl || '';
      var meta = $('.lb-meta'); meta.innerHTML = '';
      c.meta.forEach(function (m) {
        var dt = document.createElement('dt'); dt.textContent = m[0];
        var dd = document.createElement('dd'); dd.textContent = m[1];
        meta.appendChild(dt); meta.appendChild(dd);
      });
      var note = $('.lb-note'); note.hidden = !c.note; note.textContent = c.note || '';
      $('[data-lb-download]').href = c.src;
      var vis = visibleIndexes(), pos = vis.indexOf(i);
      var prev = $('[data-lb-prev]'), next = $('[data-lb-next]'), close = $('[data-lb-close]');
      prev.disabled = pos <= 0;
      next.disabled = pos < 0 || pos >= vis.length - 1;
      keepFocus(prev, next.disabled ? close : next, had);
      keepFocus(next, prev.disabled ? close : prev, had);
      keepFocus(cmpBtn, close, had);
      keepFocus(cs, close, had);
      keepFocus(ct, close, had);
      var side = $('.lb-side'); if (side) side.scrollTop = 0;
      dlg.scrollTop = 0;
      if (announceIt && live) live.textContent = c.title + ' – ' + (pos + 1) + ' / ' + vis.length;
      // Beim Schließen soll der Fokus auf die Karte des zuletzt gezeigten Bildes zurück.
      var card = document.querySelector('[data-cell="' + i + '"]');
      if (card) opener = card;
    }
    function step(d) {
      var vis = visibleIndexes(), pos = vis.indexOf(current);
      var nxt = vis[pos + d];
      if (nxt !== undefined) render(nxt, true);
    }
    document.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-cell]');
      if (!b) return;
      ev.preventDefault();
      opener = b;
      render(Number(b.dataset.cell), false);
      if (!dlg.open) dlg.showModal();
      $('[data-lb-close]').focus({ preventScroll: true });
    });
    $('[data-lb-close]').addEventListener('click', function () { dlg.close(); });
    $('[data-lb-prev]').addEventListener('click', function () { step(-1); });
    $('[data-lb-next]').addEventListener('click', function () { step(1); });
    $('[data-lb-compare]').addEventListener('click', function (ev) {
      var on = ev.currentTarget.getAttribute('aria-pressed') !== 'true';
      ev.currentTarget.setAttribute('aria-pressed', String(on));
      render(current, false);
    });
    $('[data-lb-copy-all]').addEventListener('click', function (ev) { copyText(ev.currentTarget.dataset.text, ev.currentTarget); });
    $('[data-lb-copy-style]').addEventListener('click', function (ev) { copyText(ev.currentTarget.dataset.text, ev.currentTarget); });
    $('[data-lb-copy-tpl]').addEventListener('click', function (ev) { copyText(ev.currentTarget.dataset.text, ev.currentTarget); });
    document.addEventListener('keydown', function (ev) {
      if (!dlg.open || ev.target.matches('input[type="range"]')) return;
      if (ev.key === 'ArrowRight') { step(1); ev.preventDefault(); }
      if (ev.key === 'ArrowLeft') { step(-1); ev.preventDefault(); }
    });
    // Nur ein Klick, der auf dem Hintergrund beginnt und endet, schließt den Dialog (nicht das Markieren von Text).
    dlg.addEventListener('pointerdown', function (ev) { downOnBackdrop = ev.target === dlg; });
    dlg.addEventListener('click', function (ev) { if (ev.target === dlg && downOnBackdrop) dlg.close(); });
    dlg.addEventListener('close', function () { if (opener) opener.focus(); });
  }

  /* ---------- Vorlage (Anwendungsseite) ---------- */
  var bData = document.getElementById('builder-data');
  if (bData) {
    var B = JSON.parse(bData.textContent);
    var bStyle = document.getElementById('b-style'), bSubject = document.getElementById('b-subject');
    var bText = document.getElementById('b-text'), bFormat = document.getElementById('b-format');
    var bOut = document.getElementById('b-out');
    function quoteLines(text) {
      return text.split('\n').map(function (l) { return l.trim(); }).filter(Boolean)
        .map(function (l) { return "'" + l.replace(/'/g, '’') + "'"; }).join(', ');
    }
    function buildPrompt() {
      var style = B.styles[bStyle.value] || '';
      var subject = bSubject.value.trim() || B.subject;
      var guards = B.guards[bFormat.value] || '';
      if (bText && bText.value.trim()) guards = guards.replace(B.slot, quoteLines(bText.value));
      var parts = [['style', 'Style: ' + style.trim()], ['motif', 'Subject: ' + subject], ['guards', 'Constraints: ' + guards]];
      bOut.innerHTML = '';
      parts.forEach(function (p) {
        var d = document.createElement('div'); d.className = 'seg seg-' + p[0];
        var i = document.createElement('i'); i.textContent = t('part_' + p[0]); d.appendChild(i);
        var sp = document.createElement('span'); sp.lang = 'en'; sp.textContent = p[1]; d.appendChild(sp);
        bOut.appendChild(d);
      });
      document.getElementById('b-text-all').textContent = parts.map(function (p) { return p[1]; }).join('\n\n');
      document.getElementById('b-style-only').textContent = style;
    }
    [bStyle, bSubject, bText, bFormat].forEach(function (x) { if (x) x.addEventListener('input', buildPrompt); });
    bStyle.addEventListener('change', buildPrompt);
    bFormat.addEventListener('change', buildPrompt);
    // „Vorlage ↓“ unter einem Bild: Stil übernehmen und zur Vorlage springen
    document.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-use-style]');
      if (!b || !B.styles[b.dataset.useStyle]) return;
      bStyle.value = b.dataset.useStyle;
      buildPrompt();
      document.getElementById('vorlage').scrollIntoView();
      bSubject.focus({ preventScroll: true });
    });
    buildPrompt();
  }

  /* ---------- Lexikon ---------- */
  var lex = document.getElementById('lexicon');
  if (lex) {
    var list = document.getElementById('lex-list');
    var q = document.getElementById('lex-q');
    var tally = document.getElementById('lex-tally');
    var moreBtn = document.getElementById('lex-more');
    var onlyLead = document.getElementById('lex-lead');
    var cats = Array.prototype.map.call(document.querySelectorAll('[data-lex-cat]'), function (c) { return c.dataset.lexCat; });
    var cat = '*', data = [], filtered = [], shown = 0, PAGE = 80;
    var lexMotifs = {};
    try { lexMotifs = JSON.parse(document.getElementById('lex-motifs').textContent); } catch (e) { /* ohne Beispielbilder */ }
    // Beispielbild als Lightbox-Eintrag; den Prompt bilden Baustein, Motiv und Leitplanken wie beim Erzeugen.
    function lexCell(s) {
      var m = lexMotifs[s.ex.m] || {};
      var parts = [['style', 'Style: ' + s.frag.trim()], ['motif', m.motif], ['guards', m.guards]];
      return {
        src: s.ex.src, alt: s.ex.alt, w: s.ex.w, h: s.ex.h, ar: s.ex.ar, title: s.name, href: s.page,
        eyebrow: s.cat + ' · ' + s.fam, sub: s.ex.sub, parts: parts,
        prompt: parts.map(function (p) { return p[1]; }).join('\n\n'), styleBlock: s.frag,
        meta: s.ex.meta, note: s.ex.note, base: null
      };
    }
    var params = new URLSearchParams(location.search);
    if (params.get('q')) q.value = params.get('q');
    if (params.get('cat') && cats.indexOf(params.get('cat')) >= 0) cat = params.get('cat');
    function pressChips() {
      document.querySelectorAll('[data-lex-cat]').forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.lexCat === cat)); });
    }
    pressChips();
    function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
    function item(s) {
      var li = el('li', 'lx'); li.id = s.slug; li.tabIndex = -1;
      var a = el('div');
      var h3 = el('h3');
      if (s.page) { var link = el('a', null, s.name); link.href = s.page; h3.appendChild(link); } else h3.textContent = s.name;
      a.appendChild(h3);
      a.appendChild(el('div', 'alt', s.alt));
      a.appendChild(el('div', 'fam', s.cat + ' · ' + s.fam));
      if (s.era) a.appendChild(el('div', 'dots', s.era));
      if (s._cell != null) {
        var ex = el('button', 'lx-ex'); ex.type = 'button'; ex.setAttribute('data-cell', s._cell);
        ex.setAttribute('aria-label', t('showExample') + ': ' + s.name);
        var im = el('img'); im.src = s.ex.thumb; im.alt = s.ex.alt; im.loading = 'lazy'; im.decoding = 'async';
        im.width = 320; im.height = 320;
        ex.appendChild(im);
        a.appendChild(ex);
      }
      var b = el('div');
      if (s.desc) b.appendChild(el('p', 'desc', s.desc));
      if (s.markers && s.markers.length) b.appendChild(el('p', 'dots', s.markers.join(' · ')));
      var r = el('div', 'row2');
      if (s.frag) {
        var frag = el('div', 'frag', s.frag); frag.lang = 'en'; b.appendChild(frag);
        var copy = el('button', 'btn', t('copyFragment')); copy.type = 'button'; copy.setAttribute('data-copy', s.frag);
        r.appendChild(copy);
      } else {
        b.appendChild(el('p', 'warn', t('noFragment')));
      }
      r.appendChild(el('span', 'dots', t('feasibility') + ': ' + t('feas_' + s.feas) + ' · ' + t('distinct') + ': ' + s.dist + '/5'));
      if (s.page) { var lead = el('a', 'tag', t('withImages')); lead.href = s.page; r.appendChild(lead); }
      b.appendChild(r);
      if (s.sens) b.appendChild(el('p', 'warn', s.sens));
      li.appendChild(a); li.appendChild(b);
      return li;
    }
    function syncLangLink(hash) {
      // Kategorie, Suche und Sprungziel gelten in beiden Sprachen und gehen beim Umschalten mit.
      var link = document.querySelector('.tb-lang a');
      if (!link) return;
      var u = new URL(link.getAttribute('href'), location.href);
      u.search = ''; u.hash = '';
      if (cat !== '*') u.searchParams.set('cat', cat);
      if (q.value) u.searchParams.set('q', q.value);
      if (hash) u.hash = hash;
      link.href = u.href;
    }
    function apply(reset) {
      var words = norm(q.value).split(/\s+/).filter(Boolean);
      filtered = data.filter(function (s) {
        if (cat !== '*' && s.catId !== cat) return false;
        if (onlyLead && onlyLead.checked && !s.page) return false;
        return words.every(function (w) { return s._idx.indexOf(w) >= 0; });
      });
      if (reset) { list.innerHTML = ''; shown = 0; }
      more(false);
      tally.textContent = filtered.length + ' ' + t(filtered.length === 1 ? 'style' : 'styles');
      pressChips();
      var u = new URL(location.href);
      if (q.value) u.searchParams.set('q', q.value); else u.searchParams.delete('q');
      if (cat !== '*') u.searchParams.set('cat', cat); else u.searchParams.delete('cat');
      try { history.replaceState(null, '', u.href); } catch (e) { /* lokale Vorschau */ }
      syncLangLink('');
    }
    function more(focusNew) {
      var firstNew = null;
      var frag = document.createDocumentFragment();
      filtered.slice(shown, shown + PAGE).forEach(function (s) { var li = item(s); if (!firstNew) firstNew = li; frag.appendChild(li); });
      list.appendChild(frag);
      shown = Math.min(filtered.length, shown + PAGE);
      moreBtn.hidden = shown >= filtered.length;
      moreBtn.textContent = t('showMore').replace('{n}', Math.min(PAGE, filtered.length - shown));
      if (focusNew && firstNew) firstNew.focus();
    }
    var timer;
    q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(function () { apply(true); }, 120); });
    if (onlyLead) onlyLead.addEventListener('change', function () { apply(true); });
    moreBtn.addEventListener('click', function () { more(true); });
    document.querySelectorAll('[data-lex-cat]').forEach(function (c) {
      c.addEventListener('click', function () { cat = c.dataset.lexCat; apply(true); });
    });
    fetch(lex.dataset.src).then(function (r) { return r.json(); }).then(function (rows) {
      data = rows;
      data.forEach(function (s) { s._idx = norm([s.name, s.alt, s.aka, s.cat, s.fam, s.desc, s.era, (s.markers || []).join(' '), s.frag].join(' ')); });
      // cells gehört zur Lightbox oben; die Lexikonseite liefert dafür eine leere Liste mit.
      if (typeof cells !== 'undefined' && cells) {
        data.forEach(function (s) { if (s.ex && s.frag) { s._cell = cells.length; cells.push(lexCell(s)); } });
      }
      return true;
    }, function () { tally.textContent = t('loadFailed'); return false; }).then(function (ok) {
      if (!ok) return;
      var id = '';
      if (location.hash) { try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) { id = location.hash.slice(1); } }
      // Liegt das Sprungziel außerhalb des Filters aus der URL, wird der Filter zurückgesetzt.
      if (id && data.some(function (s) { return s.slug === id; })) {
        apply(true);
        if (!filtered.some(function (s) { return s.slug === id; })) { cat = '*'; q.value = ''; if (onlyLead) onlyLead.checked = false; }
      }
      apply(true);
      if (id) {
        var pos = filtered.findIndex(function (s) { return s.slug === id; });
        while (pos >= shown && shown < filtered.length) more(false);
        var target = document.getElementById(id);
        if (target) { barHeight(); target.scrollIntoView(); target.classList.add('hit'); syncLangLink('#' + id); }
      }
    });
  }
})();
