// Lokale Speicherung (localStorage) – robust gegen private Tabs & volle Speicher.

const KEY_GAME = 'shitster.game.v1';
const KEY_PREFS = 'shitster.prefs.v1';

function read(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function write(key, value) {
  try {
    value == null ? localStorage.removeItem(key) : localStorage.setItem(key, JSON.stringify(value));
  } catch {}
}

export const loadGame = () => read(KEY_GAME, null);
export const saveGame = g => write(KEY_GAME, g);
export const clearGame = () => write(KEY_GAME, null);

export const loadPrefs = () => read(KEY_PREFS, { names: ['', ''], target: 10, categories: null });
export const savePrefs = p => write(KEY_PREFS, p);

const catCache = new Map();

export async function loadCategoryIndex() {
  const res = await fetch('data/categories.json');
  return res.json();
}

export async function loadCategory(file) {
  if (catCache.has(file)) return catCache.get(file);
  const res = await fetch('data/' + file);
  const data = await res.json();
  catCache.set(file, data);
  return data;
}
