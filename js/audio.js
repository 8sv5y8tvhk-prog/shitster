// Ein einziges Audio-Element für die ganze App – wichtig für iOS,
// weil Wiedergabe nur nach einer Nutzer-Geste erlaubt ist.

const el = new Audio();
el.preload = 'auto';
el.setAttribute('playsinline', '');

const listeners = new Set();
let fadeTimer = null;

function emit() {
  const st = state();
  listeners.forEach(fn => fn(st));
}

export function state() {
  const d = el.duration && isFinite(el.duration) ? el.duration : 30;
  return { playing: !el.paused && !el.ended, progress: Math.min(1, el.currentTime / d), time: el.currentTime, duration: d, src: el.src };
}

['play', 'pause', 'ended', 'timeupdate', 'loadedmetadata'].forEach(ev => el.addEventListener(ev, emit));

export function onChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

export const hasSource = () => !!el.getAttribute('src');

export function load(url) {
  if (el.src === url) return;
  stop();
  el.src = url;
  el.load();
}

export async function play() {
  if (!el.src) return false;
  if (el.ended) el.currentTime = 0;
  el.volume = 0;
  try {
    await el.play();
  } catch {
    el.volume = 1;
    return false;
  }
  clearInterval(fadeTimer);
  fadeTimer = setInterval(() => {
    el.volume = Math.min(1, el.volume + 0.08);
    if (el.volume >= 1) clearInterval(fadeTimer);
  }, 30);
  return true;
}

export function pause() {
  el.pause();
}

export function stop() {
  clearInterval(fadeTimer);
  el.pause();
  if (el.src) el.currentTime = 0;
}

export function restart() {
  el.currentTime = 0;
  return play();
}

export function clear() {
  stop();
  el.removeAttribute('src');
  el.load();
  emit();
}
