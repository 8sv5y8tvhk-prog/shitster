import * as G from './game.js';
import * as audio from './audio.js';
import { getTrack } from './deezer.js';
import * as store from './store.js';

const app = document.getElementById('app');
let categories = [];
let game = store.loadGame();
let screen = null;
let prefs = store.loadPrefs();

// UI-Zustand, der nicht ins Spiel gehört
const ui = { preparedId: null, loading: false, track: null, wantPlay: false, pendingChallenger: null, tlScroll: 0, failCount: 0 };

/* ───────────────────────── Icons (SF-Symbols-Stil) ───────────────────────── */
const S = 'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"';
const ICONS = {
  play: '<path d="M7 4.8v14.4c0 .8.9 1.3 1.6.9l11.3-7.2c.6-.4.6-1.4 0-1.8L8.6 3.9C7.9 3.5 7 4 7 4.8z" fill="currentColor"/>',
  pause: '<rect x="6" y="4" width="4.2" height="16" rx="1.4" fill="currentColor"/><rect x="13.8" y="4" width="4.2" height="16" rx="1.4" fill="currentColor"/>',
  back: `<path d="M15 4l-8 8 8 8" ${S} stroke-width="2.6"/>`,
  chev: `<path d="M9 5l7 7-7 7" ${S} stroke-width="2.6"/>`,
  x: `<path d="M6 6l12 12M18 6L6 18" ${S} stroke-width="2.6"/>`,
  plus: `<path d="M12 5v14M5 12h14" ${S} stroke-width="2.8"/>`,
  minus: `<path d="M5 12h14" ${S} stroke-width="2.8"/>`,
  check: `<path d="M5 12.5l4.5 4.5L19 7.5" ${S} stroke-width="2.6"/>`,
  forward: '<path d="M3 6.3v11.4c0 .7.8 1.1 1.4.7L12 13v4.7c0 .7.8 1.1 1.4.7l8.2-5.7c.5-.3.5-1.1 0-1.4l-8.2-5.7c-.6-.4-1.4 0-1.4.7V11L4.4 5.6C3.8 5.2 3 5.6 3 6.3z" fill="currentColor"/>',
  replay: `<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3" ${S} stroke-width="2.3"/><path d="M4 3.5V8h4.5" ${S} stroke-width="2.3"/>`,
  people: '<circle cx="9" cy="8" r="3.6" fill="currentColor"/><path d="M2 19.2C2 15.6 5.1 13 9 13s7 2.6 7 6.2c0 .5-.4.8-.9.8H2.9c-.5 0-.9-.3-.9-.8z" fill="currentColor"/><circle cx="17.2" cy="9" r="2.8" fill="currentColor"/><path d="M17.6 13.3c2.7.3 4.4 2.3 4.4 4.9 0 .5-.4.8-.9.8h-3.4c.2-2.2-.1-4-.1-5.7z" fill="currentColor"/>',
  mic: `<rect x="9" y="2.5" width="6" height="11.5" rx="3" fill="currentColor"/><path d="M5.5 11.2a6.5 6.5 0 0 0 13 0M12 17.8v3.7" ${S} stroke-width="2"/>`,
  book: '<path d="M3.5 5.2c0-.9.7-1.5 1.6-1.4 2.4.2 4.3.9 5.9 2.1v14.2c-1.6-1.1-3.5-1.8-5.9-2-.9-.1-1.6-.8-1.6-1.6zM20.5 5.2c0-.9-.7-1.5-1.6-1.4-2.4.2-4.3.9-5.9 2.1v14.2c1.6-1.1 3.5-1.8 5.9-2 .9-.1 1.6-.8 1.6-1.6z" fill="currentColor"/>',
  trophy: '<path d="M7 3h10v1.8h3.2v2.4a4.2 4.2 0 0 1-4.1 4.2 5 5 0 0 1-3.1 2.8V17h3v3.5H8V17h3v-2.8a5 5 0 0 1-3.1-2.8 4.2 4.2 0 0 1-4.1-4.2V4.8H7zM5.8 6.8v.4a2.2 2.2 0 0 0 1.3 2V6.8zm12.4 0h-1.3v2.4a2.2 2.2 0 0 0 1.3-2z" fill="currentColor"/>',
  sparkle: '<path d="M12 2.5l2 6 6 2-6 2-2 6-2-6-6-2 6-2zM19 15.5l.9 2.6 2.6.9-2.6.9-.9 2.6-.9-2.6-2.6-.9 2.6-.9z" fill="currentColor"/>',
  bolt: '<path d="M13.5 2L4.5 13.5h6.5L10 22l9-11.5h-6.5z" fill="currentColor"/>',
  list: `<path d="M9 6h11M9 12h11M9 18h11" ${S} stroke-width="2.2"/><circle cx="4.5" cy="6" r="1.5" fill="currentColor"/><circle cx="4.5" cy="12" r="1.5" fill="currentColor"/><circle cx="4.5" cy="18" r="1.5" fill="currentColor"/>`,
  music: `<path d="M9 17.5V6l11-2.5v11.5" ${S} stroke-width="2.2"/><circle cx="6.3" cy="17.5" r="2.8" fill="currentColor"/><circle cx="17.3" cy="15" r="2.8" fill="currentColor"/>`,
  shuffle: `<path d="M3 7h3.5c5 0 6 10 11 10H21M3 17h3.5c1.8 0 3-1.3 4-3M13.5 10c1-1.7 2.2-3 4-3H21M18 4l3 3-3 3M18 14l3 3-3 3" ${S} stroke-width="2"/>`,
  xmarkBad: `<circle cx="12" cy="12" r="10" fill="currentColor" opacity=".25"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7" ${S} stroke-width="2.4"/>`,
  checkOk: `<circle cx="12" cy="12" r="10" fill="currentColor" opacity=".25"/><path d="M7.5 12.5l3 3 6-6.5" ${S} stroke-width="2.4"/>`,
};
const icon = n => `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${ICONS[n]}</svg>`;

/* ───────────────────────── Helpers ───────────────────────── */
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const hue = y => (((y - 1988) * 13) % 360 + 360) % 360;
const initial = n => (n.trim()[0] || '?').toUpperCase();
const avatar = p => `<span class="avatar" style="--c:${p.color}">${esc(initial(p.name))}</span>`;
const haptic = (p = 10) => { try { navigator.vibrate?.(p); } catch {} };
const fmtTime = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
const save = () => store.saveGame(game);

function toast(msg, ms = 2200) {
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const el = document.createElement('div');
  el.className = 'toast';
  el.innerHTML = msg;
  document.body.appendChild(el);
  setTimeout(() => { el.classList.add('out'); setTimeout(() => el.remove(), 300); }, ms);
}

function alertBox({ title, message, actions, icon: ic, tone = 'accent' }) {
  return new Promise(resolve => {
    const bd = document.createElement('div');
    bd.className = 'alert-backdrop';
    bd.innerHTML = `
      <div class="alert" role="alertdialog" aria-labelledby="alert-title">
        ${ic ? `<div class="alert-icon ${tone}">${icon(ic)}</div>` : ''}
        <h4 id="alert-title">${title}</h4>
        ${message ? `<p>${message}</p>` : ''}
        <div class="actions">${actions.map((a, i) => `<button data-i="${i}" class="${a.style || 'cancel'}">${a.label}</button>`).join('')}</div>
      </div>`;
    const close = value => {
      bd.classList.add('closing');
      setTimeout(() => bd.remove(), 200);
      resolve(value);
    };
    bd.addEventListener('click', e => {
      const b = e.target.closest('button[data-i]');
      if (b) { haptic(6); close(actions[+b.dataset.i].value); }
      else if (e.target === bd) close(actions.find(a => a.style === 'cancel' || !a.style)?.value ?? null);
    });
    document.body.appendChild(bd);
  });
}

function sheet(renderBody, { title, dark } = {}) {
  const bd = document.createElement('div');
  bd.className = 'sheet-backdrop';
  const sh = document.createElement('div');
  sh.className = 'sheet';
  if (dark) sh.style.colorScheme = 'dark';
  const close = () => {
    bd.classList.add('closing');
    sh.classList.add('closing');
    setTimeout(() => { bd.remove(); sh.remove(); }, 350);
  };
  const paint = () => {
    sh.innerHTML = `<div class="grabber"></div><div class="sheet-head"><h3>${title}</h3><button class="sheet-close" data-close aria-label="Schließen">${icon('x')}</button></div>${renderBody()}`;
  };
  paint();
  bd.addEventListener('click', close);
  sh.addEventListener('click', e => { if (e.target.closest('[data-close]')) close(); });
  // Wischen nach unten schließt das Sheet
  let y0 = null;
  sh.addEventListener('touchstart', e => { y0 = sh.scrollTop <= 0 ? e.touches[0].clientY : null; }, { passive: true });
  sh.addEventListener('touchmove', e => {
    if (y0 == null) return;
    const dy = e.touches[0].clientY - y0;
    if (dy > 0) sh.style.transform = `translateY(${dy}px)`;
  }, { passive: true });
  sh.addEventListener('touchend', e => {
    if (y0 == null) return;
    const dy = e.changedTouches[0].clientY - y0;
    sh.style.transition = 'transform .3s var(--ease)';
    sh.style.transform = '';
    setTimeout(() => (sh.style.transition = ''), 300);
    if (dy > 110) close();
    y0 = null;
  });
  document.body.append(bd, sh);
  return { el: sh, close, paint };
}

function confetti(ms = 2600) {
  const c = document.createElement('canvas');
  c.className = 'confetti';
  const dpr = devicePixelRatio || 1;
  c.width = innerWidth * dpr;
  c.height = innerHeight * dpr;
  document.body.appendChild(c);
  const ctx = c.getContext('2d');
  ctx.scale(dpr, dpr);
  const colors = ['#ff375f', '#ffd60a', '#30d158', '#0a84ff', '#bf5af2', '#ff9f0a', '#fff'];
  const parts = Array.from({ length: 140 }, () => ({
    x: innerWidth / 2 + (Math.random() - 0.5) * 80,
    y: innerHeight * 0.35,
    vx: (Math.random() - 0.5) * 16,
    vy: -Math.random() * 16 - 4,
    r: Math.random() * 360,
    vr: (Math.random() - 0.5) * 20,
    w: 6 + Math.random() * 6,
    h: 8 + Math.random() * 10,
    c: colors[(Math.random() * colors.length) | 0],
  }));
  const t0 = performance.now();
  (function frame(t) {
    const k = (t - t0) / ms;
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    for (const p of parts) {
      p.vy += 0.42; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.r += p.vr;
      ctx.save();
      ctx.globalAlpha = Math.max(0, 1 - k * k);
      ctx.translate(p.x, p.y);
      ctx.rotate((p.r * Math.PI) / 180);
      ctx.fillStyle = p.c;
      ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * Math.abs(Math.cos(p.r / 20)));
      ctx.restore();
    }
    k < 1 ? requestAnimationFrame(frame) : c.remove();
  })(t0);
}

/* ───────────────────────── Screen-Handling ───────────────────────── */
function mount(html, { cls = '', transition = 'push' } = {}) {
  const el = document.createElement('div');
  el.className = `screen ${cls}`;
  el.innerHTML = html;
  const old = screen;
  app.appendChild(el);
  if (old) {
    old.classList.add(`leave-${transition}`);
    el.classList.add(`enter-${transition}`);
    setTimeout(() => old.remove(), 500);
  }
  screen = el;
  const nav = el.querySelector('.navbar');
  if (nav) el.addEventListener('scroll', () => nav.classList.toggle('scrolled', el.scrollTop > 36), { passive: true });
  return el;
}

const navbar = (title, { back, right = '' } = {}) => `
  <div class="navbar">
    <div>${back ? `<button class="nav-btn" data-a="back">${icon('back')}${esc(back)}</button>` : ''}</div>
    <div class="small-title">${esc(title)}</div>
    <div class="right">${right}</div>
  </div>`;

/* ───────────────────────── Home ───────────────────────── */
function renderHome(transition = 'fade') {
  audio.clear();
  const canResume = game && game.phase !== 'over';
  const el = mount(`
    ${navbar('Shitster')}
    <div class="large-title brand"><img class="brand-logo" src="assets/icon.svg" alt="">Shitster</div>
    <div class="hero">
      <div class="hero-vinyl"><div class="vinyl" style="--tint:#ff9f0a;animation:none"><div class="label"></div></div></div>
      <h2>Wer kennt das Jahr?</h2>
      <p>Hör rein, ordne ein, klau Karten. Das Timeline-Musikspiel für eure Runde.</p>
      <button class="btn white" data-a="new">${icon('play')}Neues Spiel</button>
    </div>
    ${canResume ? `
      <div class="section">
        <div class="section-header">Laufendes Spiel</div>
        <button class="resume-card" data-a="resume">
          <div class="avatar-stack">${game.players.slice(0, 4).map(avatar).join('')}</div>
          <div style="flex:1;min-width:0">
            <div class="title" style="font-weight:600">Spiel fortsetzen</div>
            <div class="detail" style="font-size:15px;color:var(--label-2)">${esc(G.activePlayer(game).name)} ist dran · Ziel ${game.settings.target} Karten</div>
          </div>
          <span class="chev" style="color:var(--label-3)">${icon('chev')}</span>
        </button>
      </div>` : ''}
    <div class="section">
      <div class="section-header big">Kategorien</div>
      <div class="list">
        ${categories.map(c => `
          <button class="row has-icon" data-a="cat" data-id="${c.id}">
            <span class="icon-tile" style="background:linear-gradient(135deg,${c.colors[0]},${c.colors[1]})">${icon(c.icon || 'mic')}</span>
            <div class="body"><div class="title">${esc(c.name)}</div><div class="detail">${c.count} Songs · ${c.from}–${c.to}</div></div>
            <span class="chev">${icon('chev')}</span>
          </button>`).join('') || '<div class="row"><div class="body detail">Keine Kategorien gefunden</div></div>'}
      </div>
      <div class="section-footer">Weitere Kategorien folgen – eigene Listen kommen in einer späteren Version.</div>
    </div>
    <div class="section">
      <div class="list">
        <button class="row has-icon" data-a="rules">
          <span class="icon-tile" style="background:#ff9500">${icon('book')}</span>
          <div class="body"><div class="title">Spielregeln</div></div>
          <span class="chev">${icon('chev')}</span>
        </button>
      </div>
    </div>
  `, { transition });
  el.addEventListener('click', e => {
    const b = e.target.closest('[data-a]');
    if (!b) return;
    haptic(6);
    const a = b.dataset.a;
    if (a === 'new') renderSetup();
    if (a === 'resume') renderGame('fade');
    if (a === 'rules') renderRules();
    if (a === 'cat') renderCategory(categories.find(c => c.id === b.dataset.id));
  });
}

/* ───────────────────────── Kategorie ───────────────────────── */
async function renderCategory(cat) {
  const el = mount(`${navbar(cat.name, { back: 'Start' })}<div class="large-title">${esc(cat.name)}</div><div class="subtitle">${esc(cat.description)}</div><div class="section"><div class="list" id="songs"><div class="row"><div class="body detail">Lade …</div></div></div></div>`);
  el.addEventListener('click', e => { if (e.target.closest('[data-a="back"]')) renderHome('pop'); });
  const data = await store.loadCategory(cat.file);
  const songs = data.songs.slice().sort((a, b) => a.year - b.year || a.artist.localeCompare(b.artist));
  el.querySelector('#songs').innerHTML = songs.map(s => `
    <div class="row">
      <span class="year-pill" style="--h:${hue(s.year)}">${s.year}</span>
      <div class="body"><div class="title">${esc(s.title)}</div><div class="detail">${esc(s.artist)}</div></div>
    </div>`).join('');
}

/* ───────────────────────── Regeln ───────────────────────── */
function renderRules() {
  const el = mount(`
    ${navbar('Spielregeln', { back: 'Start' })}
    <div class="large-title">Spielregeln</div>
    <div class="section"><div class="section-header">Ziel</div><div class="list"><div class="prose" style="padding-top:12px">
      <p>Baue als Erste:r eine Zeitleiste aus <b>10 Songs</b> (einstellbar) – sortiert nach Erscheinungsjahr.</p>
    </div></div></div>
    <div class="section"><div class="section-header">Ein Zug</div><div class="list"><div class="prose" style="padding-top:12px">
      <p><b>1.</b> Jede:r startet mit einer aufgedeckten Karte und 2 Tokens.</p>
      <p><b>2.</b> Wer dran ist, spielt den Song ab und tippt auf die Lücke in der eigenen Zeitleiste, wo er zeitlich hingehört.</p>
      <p><b>3.</b> Die anderen können <b>HITSTER!</b> rufen (siehe unten).</p>
      <p><b>4.</b> Aufdecken: Liegt die Karte richtig, bleibt sie in der Zeitleiste. Sonst fliegt sie raus. Gleiche Jahre dürfen vor oder hinter der Karte liegen.</p>
    </div></div></div>
    <div class="section"><div class="section-header">Tokens</div><div class="list"><div class="prose" style="padding-top:12px">
      <p><b>+1 Token</b>: Wer dran ist und Titel <i>und</i> Interpret richtig nennt (max. 5 Tokens).</p>
      <p><b>Überspringen</b> (1 Token): Neuer Song, wenn du keinen Plan hast.</p>
      <p><b>HITSTER!</b> (1 Token): Glaubst du, die Person am Zug liegt falsch? Setz einen Token auf eine andere Lücke. Liegst du richtig, klaust du die Karte für deine eigene Zeitleiste.</p>
      <p><b>Karte kaufen</b> (3 Tokens): Jederzeit über die Spielerübersicht – die Karte wandert direkt richtig einsortiert in deine Zeitleiste.</p>
    </div></div></div>
  `);
  el.addEventListener('click', e => { if (e.target.closest('[data-a="back"]')) renderHome('pop'); });
}

/* ───────────────────────── Setup ───────────────────────── */
function renderSetup() {
  if (!prefs.categories) prefs.categories = categories.map(c => c.id);
  prefs.categories = prefs.categories.filter(id => categories.some(c => c.id === id));
  if (!prefs.categories.length && categories.length) prefs.categories = [categories[0].id];
  if (!prefs.names?.length) prefs.names = ['', ''];

  const el = mount(`
    ${navbar('Neues Spiel', { back: 'Start' })}
    <div class="large-title">Neues Spiel</div>
    <div class="section">
      <div class="section-header">Spieler</div>
      <div class="list" id="players"></div>
      <div class="section-footer">Ein Handy für alle – reicht es einfach weiter.</div>
    </div>
    <div class="section">
      <div class="section-header">Kategorien</div>
      <div class="list" id="cats"></div>
    </div>
    <div class="section">
      <div class="section-header">Regeln</div>
      <div class="list">
        <div class="row"><div class="body"><div class="title">Karten zum Sieg</div></div>
          <span class="value" id="target" style="font-family:var(--font-rounded);font-weight:600;min-width:24px;text-align:right">${prefs.target}</span>
          <div class="stepper"><button data-a="tminus" aria-label="Weniger">${icon('minus')}</button><span class="sep"></span><button data-a="tplus" aria-label="Mehr">${icon('plus')}</button></div>
        </div>
        <div class="row"><div class="body"><div class="title">Start-Tokens</div></div><span class="value">${G.START_TOKENS}</span></div>
      </div>
    </div>
    <div class="bottom-bar"><button class="btn" data-a="start">${icon('play')}Spiel starten</button></div>
  `, { cls: 'with-bar' });

  const paintPlayers = () => {
    el.querySelector('#players').innerHTML = prefs.names.map((n, i) => `
      <div class="row">
        <button class="minus-btn" data-a="del" data-i="${i}" ${prefs.names.length <= 1 ? 'disabled' : ''} aria-label="Entfernen">${icon('minus')}</button>
        <input type="text" data-i="${i}" value="${esc(n)}" placeholder="Spieler ${i + 1}" maxlength="16" autocomplete="off" autocapitalize="words" enterkeyhint="next">
      </div>`).join('') + (prefs.names.length < 10 ? `
      <button class="row tint" data-a="add"><span class="plus-btn">${icon('plus')}</span><div class="body">Spieler hinzufügen</div></button>` : '');
  };
  const paintCats = () => {
    el.querySelector('#cats').innerHTML = categories.map(c => `
      <button class="row has-icon ${prefs.categories.includes(c.id) ? 'checked' : ''}" data-a="togglecat" data-id="${c.id}">
        <span class="icon-tile" style="background:linear-gradient(135deg,${c.colors[0]},${c.colors[1]})">${icon(c.icon || 'mic')}</span>
        <div class="body"><div class="title">${esc(c.name)}</div><div class="detail">${c.count} Songs</div></div>
        <span class="check">${icon('check')}</span>
      </button>`).join('');
  };
  paintPlayers();
  paintCats();

  el.addEventListener('input', e => {
    if (e.target.matches('input[data-i]')) {
      prefs.names[+e.target.dataset.i] = e.target.value;
      store.savePrefs(prefs);
    }
  });
  el.addEventListener('keydown', e => {
    if (e.key === 'Enter' && e.target.matches('input[data-i]')) {
      const next = el.querySelector(`input[data-i="${+e.target.dataset.i + 1}"]`);
      next ? next.focus() : e.target.blur();
    }
  });
  el.addEventListener('click', async e => {
    const b = e.target.closest('[data-a]');
    if (!b) return;
    const a = b.dataset.a;
    haptic(6);
    if (a === 'back') return renderHome('pop');
    if (a === 'add') {
      prefs.names.push('');
      paintPlayers();
      el.querySelector(`input[data-i="${prefs.names.length - 1}"]`)?.focus();
    }
    if (a === 'del') { prefs.names.splice(+b.dataset.i, 1); paintPlayers(); }
    if (a === 'togglecat') {
      const id = b.dataset.id;
      const has = prefs.categories.includes(id);
      if (has && prefs.categories.length === 1) return toast('Mindestens eine Kategorie');
      prefs.categories = has ? prefs.categories.filter(x => x !== id) : [...prefs.categories, id];
      b.classList.toggle('checked', !has);
    }
    if (a === 'tminus' || a === 'tplus') {
      prefs.target = Math.max(3, Math.min(25, prefs.target + (a === 'tplus' ? 1 : -1)));
      el.querySelector('#target').textContent = prefs.target;
    }
    store.savePrefs(prefs);
    if (a === 'start') startNewGame();
  });
}

async function startNewGame() {
  const names = prefs.names.map((n, i) => n.trim() || `Spieler ${i + 1}`);
  const cats = categories.filter(c => prefs.categories.includes(c.id));
  const lists = await Promise.all(cats.map(c => store.loadCategory(c.file)));
  const songs = lists.flatMap(l => l.songs);
  if (songs.length < names.length * (prefs.target + 2)) toast('Wenig Songs für so viele Karten – es wird gemischt, wenn der Stapel leer ist.', 3000);
  game = G.createGame({ names, songs, target: prefs.target, categories: prefs.categories });
  save();
  Object.assign(ui, { preparedId: null, pendingChallenger: null, tlScroll: 0 });
  renderGame('fade');
}

/* ───────────────────────── Spiel ───────────────────────── */
let unsubAudio = null;

function renderGame(transition = 'fade') {
  if (game.phase === 'over') return renderWinner(transition);
  const el = mount(`
    <div class="game-bg"></div>
    <div class="game-top" id="g-top"></div>
    <div class="turn-head" id="g-head"></div>
    <div class="stage" id="g-stage"></div>
    <div class="hint" id="g-hint"></div>
    <div class="tl-wrap" id="g-tl"></div>
    <div class="game-bottom" id="g-bottom"></div>
  `, { cls: 'game', transition });
  el.addEventListener('click', onGameClick);
  unsubAudio?.();
  unsubAudio = audio.onChange(updatePlayerUI);
  paintGame();
}

function paintGame() {
  const s = game;
  if (!screen?.classList.contains('game')) return;
  const me = G.activePlayer(s);
  screen.style.setProperty('--tint', me.color);
  paintTop();
  paintHead();
  paintStage();
  paintTimeline();
  paintBottom();
  ensureTrack();
}

function paintTop() {
  const s = game;
  screen.querySelector('#g-top').innerHTML = `
    <button class="circle-btn" data-a="menu" aria-label="Pause">${icon('x')}</button>
    <div class="scoreboard">${s.players.map((p, i) => `
      <button class="score-chip ${i === s.current ? 'active' : ''}" style="--c:${p.color}" data-a="scores">
        ${avatar(p)}<span class="n">${p.timeline.length}/${s.settings.target}</span><span class="t"><span class="token"></span>${p.tokens}</span>
      </button>`).join('')}</div>
    <button class="circle-btn" data-a="scores" aria-label="Spielerübersicht">${icon('people')}</button>`;
}

function paintHead() {
  const s = game;
  const me = G.activePlayer(s);
  const kicker = { listen: 'Am Zug', challenge: 'Gleich wird aufgedeckt', reveal: 'Aufgedeckt' }[s.phase] || '';
  screen.querySelector('#g-head').innerHTML = `
    <div class="kicker">${kicker}</div>
    <h1><span class="name">${esc(me.name)}</span></h1>
    <div class="tokens">${Array.from({ length: G.MAX_TOKENS }, (_, i) => `<span class="token lg ${i < me.tokens ? '' : 'empty'}"></span>`).join('')}</div>`;
}

function playerHTML(big = true) {
  const st = audio.state();
  const C = 2 * Math.PI * 48;
  return `
    <div class="player ${st.playing ? 'playing' : ''}" id="player" ${big ? '' : 'style="width:120px"'}>
      <svg class="ring" viewBox="0 0 100 100"><circle class="track" cx="50" cy="50" r="48" fill="none" stroke-width="2.4"/>
        <circle class="bar" cx="50" cy="50" r="48" fill="none" stroke-width="2.6" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - st.progress)}"/></svg>
      <div class="vinyl"><div class="label"></div></div>
      <button class="play-btn" data-a="toggle" aria-label="Abspielen">${playIcon()}</button>
    </div>`;
}

function playIcon() {
  if (ui.loading && !ui.track) return '<span class="spinner"></span>';
  return audio.state().playing ? icon('pause') : icon('play');
}

function updatePlayerUI(st) {
  const p = screen?.querySelector('#player');
  if (!p) return;
  p.classList.toggle('playing', st.playing);
  const C = 2 * Math.PI * 48;
  p.querySelector('.bar')?.setAttribute('stroke-dashoffset', C * (1 - st.progress));
  const btn = p.querySelector('.play-btn');
  const want = playIcon();
  if (btn && btn.dataset.icon !== want) { btn.innerHTML = want; btn.dataset.icon = want; }
  const t = screen.querySelector('#g-time');
  if (t) t.textContent = st.playing || st.time > 0 ? '-' + fmtTime(Math.max(0, st.duration - st.time)) : '0:30';
}

function paintStage() {
  const s = game;
  const me = G.activePlayer(s);
  const st = screen.querySelector('#g-stage');
  if (s.phase === 'listen') {
    st.innerHTML = `
      ${playerHTML()}
      <div class="player-controls">
        <button class="pill-btn" data-a="replay">${icon('replay')}Neu</button>
        <span class="time" id="g-time">0:30</span>
        <button class="pill-btn" data-a="skip" ${G.canSkip(s) ? '' : 'disabled'}>${icon('forward')}Skip · 1<span class="token"></span></button>
      </div>`;
    updatePlayerUI(audio.state());
  } else if (s.phase === 'challenge') {
    const cands = s.players.filter((p, i) => i !== s.current);
    const done = new Map(s.turn.challenges.map(c => [c.playerId, c]));
    st.innerHTML = `
      <div class="challenge-box">
        <h2>HITSTER!</h2>
        <p>Liegt ${esc(me.name)} falsch? Tippe deinen Namen und dann eine freie Lücke. Kostet 1 Token – wer richtig liegt, klaut die Karte.</p>
        <div class="chips">
          ${cands.map(p => {
            const isDone = done.has(p.id);
            const on = ui.pendingChallenger === p.id;
            const dis = !isDone && p.tokens < 1;
            return `<button class="chip ${isDone ? 'done' : ''} ${on ? 'on' : ''}" style="--c:${p.color}" data-a="${isDone ? 'unchallenge' : 'pickchallenger'}" data-id="${p.id}" ${dis ? 'disabled' : ''}>
              ${avatar(p)}${esc(p.name)}${isDone ? `<span class="x">${icon('x')}</span>` : `<span class="t" style="display:inline-flex;align-items:center;gap:2px;font-size:13px;opacity:.8"><span class="token"></span>${p.tokens}</span>`}
            </button>`;
          }).join('')}
        </div>
      </div>
      <div class="player-controls" style="margin-top:16px">
        <button class="pill-btn" data-a="toggle" id="mini-toggle">${audio.state().playing ? icon('pause') + 'Pause' : icon('play') + 'Nochmal hören'}</button>
      </div>`;
  } else if (s.phase === 'reveal') {
    const card = s.turn.card;
    const r = s.lastResult;
    const winner = r.winnerId && G.playerById(s, r.winnerId);
    const res = r.correct
      ? `<div class="result ok">${icon('checkOk')}Richtig! Karte bleibt</div>`
      : winner
        ? `<div class="result steal">${icon('bolt')}${esc(winner.name)} klaut die Karte!</div>`
        : `<div class="result bad">${icon('xmarkBad')}Daneben – Karte ist weg</div>`;
    const cover = ui.track?.cover && ui.preparedId === card.id ? ui.track.cover : '';
    st.innerHTML = `
      <div class="flip"><div class="flip-inner">
        <div class="flip-face flip-front" style="${cover ? `background-image:url('${esc(cover)}')` : `background:linear-gradient(160deg,hsl(${hue(card.year)} 80% 55%),#1c1c1e)`}"><span class="year">${card.year}</span></div>
        <div class="flip-face flip-back">?</div>
      </div></div>
      <div class="song-meta"><div class="st">${esc(card.title)}</div><div class="sa">${esc(card.artist)}</div></div>
      ${res}`;
  }
}

function gapLabel(tl, g) {
  if (!tl.length) return '';
  if (g === 0) return `Vor ${tl[0].year}`;
  if (g === tl.length) return `Nach ${tl[tl.length - 1].year}`;
  return `Zwischen ${tl[g - 1].year} und ${tl[g].year}`;
}

function timelineHTML(tl, { selected = null, claims = new Map(), canTap = () => false, newId = null } = {}) {
  let h = '';
  for (let g = 0; g <= tl.length; g++) {
    const claim = claims.get(g);
    if (g === selected) h += `<div class="gap selected" data-gapi="${g}"><div class="slot">?</div></div>`;
    else if (claim) h += `<div class="gap claimed" style="--c:${claim.color}" data-gapi="${g}"><div class="slot">${esc(initial(claim.name))}</div></div>`;
    else if (canTap(g)) h += `<button class="gap interactive" data-a="gap" data-gap="${g}" aria-label="${gapLabel(tl, g)}"><div class="slot">${icon('plus')}</div></button>`;
    else h += `<div class="gap"><div class="slot"></div></div>`;
    if (g < tl.length) {
      const c = tl[g];
      h += `<div class="tl-card ${c.id === newId ? 'new' : ''}" style="--h:${hue(c.year)}"><div class="y">${c.year}</div><div><div class="t">${esc(c.title)}</div><div class="a">${esc(c.artist)}</div></div></div>`;
    }
  }
  return h;
}

function paintTimeline() {
  const s = game;
  const me = G.activePlayer(s);
  const wrap = screen.querySelector('#g-tl');
  const prev = wrap.querySelector('.timeline');
  if (prev) ui.tlScroll = prev.scrollLeft;
  let owner = me, html, hint = '';

  if (s.phase === 'listen') {
    html = timelineHTML(me.timeline, { selected: s.turn.gap, canTap: () => true });
    hint = s.turn.gap == null ? 'Tippe auf eine Lücke in deiner Zeitleiste' : gapLabel(me.timeline, s.turn.gap);
  } else if (s.phase === 'challenge') {
    const claims = new Map(s.turn.challenges.map(c => [c.gap, G.playerById(s, c.playerId)]));
    const taken = G.takenGaps(s);
    html = timelineHTML(me.timeline, { selected: s.turn.gap, claims, canTap: g => ui.pendingChallenger && !taken.has(g) });
    const pc = ui.pendingChallenger && G.playerById(s, ui.pendingChallenger);
    hint = pc ? `${esc(pc.name)}: Tippe auf eine freie Lücke` : s.turn.challenges.length ? 'Noch jemand? Sonst aufdecken!' : `${esc(me.name)} sagt: ${gapLabel(me.timeline, s.turn.gap)}`;
  } else if (s.phase === 'reveal') {
    const r = s.lastResult;
    owner = r.winnerId ? G.playerById(s, r.winnerId) : me;
    html = timelineHTML(owner.timeline, { newId: r.winnerId ? s.turn.card.id : null });
    hint = '';
  }
  wrap.innerHTML = `
    <div class="tl-label"><span>${owner === me ? 'Zeitleiste' : 'Zeitleiste von ' + esc(owner.name)}</span><span class="count">${owner.timeline.length} / ${s.settings.target}</span></div>
    <div class="timeline">${html}</div>`;
  screen.querySelector('#g-hint').innerHTML = hint;
  const tl = wrap.querySelector('.timeline');
  tl.scrollLeft = ui.tlScroll;
  const focus = tl.querySelector('.tl-card.new, .gap.selected');
  if (focus) {
    requestAnimationFrame(() => {
      const left = focus.offsetLeft - tl.clientWidth / 2 + focus.offsetWidth / 2;
      tl.scrollTo({ left, behavior: s.phase === 'reveal' ? 'auto' : 'smooth' });
    });
  } else if (!prev) {
    tl.scrollLeft = tl.scrollWidth;
  }
}

function paintBottom() {
  const s = game;
  const me = G.activePlayer(s);
  const b = screen.querySelector('#g-bottom');
  if (s.phase === 'listen') {
    b.innerHTML = `<button class="btn" data-a="place" ${s.turn.gap == null ? 'disabled' : ''}>${icon('check')}Hier einordnen</button>`;
  } else if (s.phase === 'challenge') {
    b.innerHTML = `<button class="btn white" data-a="reveal">${icon('sparkle')}Aufdecken</button>`;
  } else if (s.phase === 'reveal') {
    const full = me.tokens >= G.MAX_TOKENS && !s.turn.bonusApplied;
    b.innerHTML = `
      <label class="bonus-row">
        <div class="body"><div class="ttl">Titel &amp; Interpret gewusst?</div><div class="sub">${full ? 'Maximum von 5 Tokens erreicht' : `+1 Token für ${esc(me.name)}`}</div></div>
        <span class="switch ${full ? 'maxed' : ''}"><input type="checkbox" data-a="bonus" ${s.turn.bonus ? 'checked' : ''}><span></span></span>
      </label>
      <button class="btn" data-a="next">${s.winner ? icon('trophy') + 'Zur Siegerehrung' : 'Nächster Zug' + icon('chev')}</button>`;
  }
}

async function ensureTrack() {
  const s = game;
  if (s.phase === 'over' || !s.turn?.card) return;
  const card = s.turn.card;
  if (ui.preparedId === card.id) return;
  ui.preparedId = card.id;
  ui.track = null;
  ui.loading = true;
  audio.clear();
  updatePlayerUI(audio.state());
  try {
    const t = await getTrack(card.id);
    if (ui.preparedId !== card.id) return;
    if (!t.playable) throw new Error('unplayable');
    ui.track = t;
    ui.loading = false;
    ui.failCount = 0;
    audio.load(t.preview);
    if (t.cover) new Image().src = t.cover;
    const front = screen?.querySelector('.flip-front');
    if (front && t.cover) front.style.backgroundImage = `url('${t.cover}')`;
    if (ui.wantPlay) { ui.wantPlay = false; audio.play(); }
    updatePlayerUI(audio.state());
  } catch (err) {
    if (ui.preparedId !== card.id) return;
    ui.loading = false;
    ui.preparedId = null;
    if (s.phase === 'listen' && ++ui.failCount <= 5 && err.message === 'unplayable') {
      toast('Song nicht verfügbar – neuer Song');
      G.replaceUnplayable(s);
      save();
      paintGame();
    } else if (s.phase === 'listen') {
      toast(navigator.onLine ? 'Deezer antwortet nicht – tippe erneut auf Play' : 'Keine Internetverbindung');
      updatePlayerUI(audio.state());
    }
  }
}

async function onGameClick(e) {
  const el = e.target.closest('[data-a]');
  if (!el) return;
  const a = el.dataset.a;
  const s = game;

  if (a === 'toggle') {
    haptic(8);
    if (!ui.track) { ui.wantPlay = true; ui.preparedId = null; ensureTrack(); return; }
    if (audio.state().playing) audio.pause();
    else if (!(await audio.play())) toast('Tippe nochmal auf Play');
    if (s.phase === 'challenge') paintStage();
    return;
  }
  if (a === 'replay') { haptic(8); if (ui.track) audio.restart(); return; }
  if (a === 'skip') {
    if (!G.skip(s)) return;
    haptic([10, 40, 10]);
    save();
    toast(`Übersprungen · −1 <span class="token"></span>`);
    ui.wantPlay = true;
    paintGame();
    return;
  }
  if (a === 'gap') {
    haptic(8);
    const g = +el.dataset.gap;
    if (s.phase === 'listen') {
      G.selectGap(s, s.turn.gap === g ? null : g);
      save();
      paintTimeline();
      paintBottom();
    } else if (s.phase === 'challenge' && ui.pendingChallenger) {
      G.addChallenge(s, ui.pendingChallenger, g);
      ui.pendingChallenger = null;
      haptic([15, 30, 15]);
      save();
      paintTop();
      paintStage();
      paintTimeline();
    }
    return;
  }
  if (a === 'place') {
    haptic(12);
    G.confirmPlacement(s);
    ui.pendingChallenger = null;
    if (!G.challengers(s).length) G.reveal(s);
    save();
    afterPhaseChange();
    return;
  }
  if (a === 'pickchallenger') {
    haptic(6);
    ui.pendingChallenger = ui.pendingChallenger === el.dataset.id ? null : el.dataset.id;
    paintStage();
    paintTimeline();
    return;
  }
  if (a === 'unchallenge') {
    G.removeChallenge(s, el.dataset.id);
    save();
    paintTop();
    paintStage();
    paintTimeline();
    return;
  }
  if (a === 'reveal') {
    haptic([10, 60, 20]);
    ui.pendingChallenger = null;
    G.reveal(s);
    save();
    afterPhaseChange();
    return;
  }
  if (a === 'bonus') {
    const me = G.activePlayer(s);
    if (!s.turn.bonus && me.tokens >= G.MAX_TOKENS) {
      e.preventDefault();
      haptic([30, 50, 30]);
      alertBox({
        icon: 'sparkle', tone: 'gold',
        title: 'Token-Maximum erreicht',
        message: `${esc(me.name)} hat schon 5 Tokens – mehr passen nicht in die Tasche. Setz sie ein: <b>Skip</b> oder <b>HITSTER!</b> für 1 Token, oder <b>3 Tokens</b> gegen eine Karte (über die Spielerübersicht).`,
        actions: [{ label: 'Verstanden', value: true, style: 'primary' }],
      });
      return;
    }
    G.toggleBonus(s);
    haptic(10);
    save();
    paintTop();
    paintHead();
    return;
  }
  if (a === 'next') {
    haptic(8);
    audio.clear();
    ui.preparedId = null;
    ui.track = null;
    ui.tlScroll = 0;
    G.nextTurn(s);
    save();
    if (s.phase === 'over') return renderWinner('fade');
    screen.querySelector('#g-tl').innerHTML = '';
    screen.classList.remove('enter-fade');
    void screen.offsetWidth;
    screen.classList.add('enter-fade');
    paintGame();
    return;
  }
  if (a === 'scores') { haptic(6); return openScores(); }
  if (a === 'menu') {
    haptic(6);
    const v = await alertBox({
      icon: 'pause',
      title: 'Spiel pausieren?',
      message: 'Der Spielstand wird gespeichert – ihr könnt jederzeit genau hier weitermachen.',
      actions: [
        { label: 'Pausieren', value: 'pause', style: 'primary' },
        { label: 'Spiel beenden', value: 'end', style: 'destructive' },
        { label: 'Weiterspielen', value: null, style: 'cancel' },
      ],
    });
    if (v === 'pause') { unsubAudio?.(); renderHome('fade'); }
    if (v === 'end') {
      const sure = await alertBox({
        icon: 'x', tone: 'red',
        title: 'Spiel wirklich beenden?',
        message: 'Der Spielstand wird gelöscht und kann nicht wiederhergestellt werden.',
        actions: [
          { label: 'Beenden', value: true, style: 'destructive' },
          { label: 'Abbrechen', value: false, style: 'cancel' },
        ],
      });
      if (sure) { unsubAudio?.(); store.clearGame(); game = null; renderHome('fade'); }
    }
  }
}

function afterPhaseChange() {
  paintGame();
  if (game.phase === 'reveal' && game.lastResult.winnerId) setTimeout(() => confetti(), 1100);
}

function openScores() {
  const s = game;
  const sh = sheet(() => `
    <div class="section" style="margin-bottom:12px">
      <div class="list">
        ${s.players.map(p => `<div class="pgroup">
          <div class="row has-icon" style="--sep-inset:58px">
            ${avatar(p)}
            <div class="body"><div class="title" style="font-weight:600">${esc(p.name)}</div><div class="detail">${p.timeline.length} von ${s.settings.target} Karten</div></div>
            <span style="display:inline-flex;align-items:center;gap:4px;font-family:var(--font-rounded);font-weight:700"><span class="token lg"></span>${p.tokens}</span>
          </div>
          <div class="mini-tl" style="background:var(--cell)">${p.timeline.map(c => `<span style="--h:${hue(c.year)}">${c.year}</span>`).join('')}</div>
          ${G.canBuy(s, p.id) ? `<button class="row tint" data-buy="${p.id}" style="--sep-inset:58px;padding-left:58px">${icon('sparkle')} Karte kaufen · 3 Tokens</button>` : ''}
        </div>`).join('')}
      </div>
      <div class="section-footer">Mit 3 Tokens kannst du jederzeit eine Karte kaufen – sie wird automatisch richtig einsortiert.</div>
    </div>`, { title: 'Spieler' });
  sh.el.addEventListener('click', async e => {
    const b = e.target.closest('[data-buy]');
    if (!b) return;
    const p = G.playerById(s, b.dataset.buy);
    const ok = await alertBox({
      icon: 'sparkle', tone: 'gold',
      title: 'Karte kaufen?',
      message: `${esc(p.name)} tauscht 3 Tokens gegen eine Karte vom Stapel. Sie wird automatisch richtig einsortiert.`,
      actions: [{ label: 'Kaufen · 3 Tokens', value: true, style: 'primary' }, { label: 'Abbrechen', value: false, style: 'cancel' }],
    });
    if (!ok) return;
    const card = G.buyCard(s, p.id);
    if (!card) return;
    haptic([10, 40, 10]);
    save();
    toast(`${esc(p.name)} bekommt ${card.year}: ${esc(card.title)}`, 3000);
    sh.paint();
    paintTop();
    paintHead();
    if (s.phase === 'listen' && s.winner) {
      sh.close();
      G.nextTurn(s);
      save();
      setTimeout(() => renderWinner('fade'), 400);
    }
  });
}

/* ───────────────────────── Sieger ───────────────────────── */
function renderWinner(transition = 'fade') {
  audio.clear();
  unsubAudio?.();
  const s = game;
  const w = G.playerById(s, s.winner);
  const ranking = s.players.slice().sort((a, b) => (b.id === w.id) - (a.id === w.id) || b.timeline.length - a.timeline.length || b.tokens - a.tokens);
  const el = mount(`
    <div class="game-bg"></div>
    <div class="winner">
      <div class="trophy">${icon('trophy')}</div>
      <h1>${esc(w.name)} gewinnt!</h1>
      <p>mit ${w.timeline.length} Karten in der Zeitleiste</p>
    </div>
    <div class="ranking">${ranking.map((p, i) => `
      <div class="r"><span class="pos">${i + 1}</span>${avatar(p)}<span class="nm">${esc(p.name)}</span><span class="sc">${p.timeline.length}</span></div>`).join('')}
    </div>
    <div class="tl-wrap"><div class="tl-label"><span>Siegerzeitleiste</span></div><div class="timeline">${timelineHTML(w.timeline)}</div></div>
    <div class="game-bottom" style="display:grid;gap:10px;margin-top:auto">
      <button class="btn" data-a="again">${icon('shuffle')}Revanche</button>
      <button class="btn glass" data-a="home">Zum Start</button>
    </div>
  `, { cls: 'game', transition });
  el.style.setProperty('--tint', w.color);
  setTimeout(() => confetti(3200), 350);
  haptic([20, 60, 20, 60, 40]);
  el.addEventListener('click', async e => {
    const b = e.target.closest('[data-a]');
    if (!b) return;
    if (b.dataset.a === 'home') { store.clearGame(); game = null; renderHome('fade'); }
    if (b.dataset.a === 'again') {
      const names = s.players.map(p => p.name);
      const cats = categories.filter(c => s.settings.categories.includes(c.id));
      const lists = await Promise.all(cats.map(c => store.loadCategory(c.file)));
      game = G.createGame({ names, songs: lists.flatMap(l => l.songs), target: s.settings.target, categories: s.settings.categories });
      save();
      Object.assign(ui, { preparedId: null, pendingChallenger: null, tlScroll: 0 });
      renderGame('fade');
    }
  });
}

/* ───────────────────────── Start ───────────────────────── */
async function boot() {
  try {
    categories = await store.loadCategoryIndex();
  } catch {
    categories = [];
  }
  if (game && game.phase !== 'over') renderGame('fade');
  else renderHome('fade');
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
}

boot();
