// Reine Spiellogik – ein serialisierbares State-Objekt, keine DOM-Zugriffe.
// So lässt sich der State später 1:1 über einen Echtzeit-Dienst (Option B) synchronisieren.

export const START_TOKENS = 2;
export const MAX_TOKENS = 5;
export const BUY_COST = 3;

// Trinkspiel: Basis-Schlücke (Stufe „Normal“), werden mit der Intensität skaliert
export const SIPS = { wrong: 2, right: 1, title: 2, year: 1, stolen: 1, counterWrong: 2, skip: 1, duel: 3, duelTie: 1 };
export const INTENSITY = { chill: 'Chillig', normal: 'Normal', hard: 'Eskalation' };
const DUEL_CHANCE = 0.22;
const DUEL_MIN_GAP = 3;

const PLAYER_COLORS = ['#FF375F', '#0A84FF', '#30D158', '#FF9F0A', '#BF5AF2', '#64D2FF', '#FFD60A', '#FF6482', '#5E5CE6', '#AC8E68'];

export function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Gleicher Song in mehreren Kategorien (auch mit anderer Deezer-ID) → nur einmal ins Spiel
export function songKey(s) {
  const n = x => x.toLowerCase().normalize('NFKD').replace(/\(.*?\)|\[.*?\]/g, '').replace(/[^a-z0-9]/g, '');
  const mainArtist = s.artist.split(/ feat\. | & |, /)[0];
  return `${n(mainArtist)}|${n(s.title)}`;
}

export function createGame({ names, songs, target, categories, mode = 'classic', drink = null }) {
  const seen = new Set();
  const unique = songs.filter(s => {
    const keys = [String(s.id), songKey(s)];
    if (keys.some(k => seen.has(k))) return false;
    keys.forEach(k => seen.add(k));
    return true;
  });
  const isDrink = mode === 'drink';
  const state = {
    version: 1,
    createdAt: Date.now(),
    settings: { target, categories, mode, drink: isDrink ? drink : null },
    players: names.map((name, i) => ({
      id: 'p' + i,
      name,
      color: PLAYER_COLORS[i % PLAYER_COLORS.length],
      tokens: isDrink ? 0 : START_TOKENS,
      // null = unbegrenzt
      counters: isDrink && drink.counter === 'limited' ? drink.counterLimit : null,
      timeline: [],
    })),
    deck: shuffle(unique),
    discard: [],
    current: 0,
    phase: 'listen',
    turn: null,
    duel: null,
    turnsSinceDuel: 0,
    lastResult: null,
    winner: null,
    endgame: null,
  };
  for (const p of state.players) p.timeline.push(draw(state));
  startTurn(state);
  return state;
}

export const isDrink = s => s.settings.mode === 'drink';

// Schluckzahl nach Intensität
export function sips(s, base) {
  const i = s.settings.drink?.intensity || 'normal';
  if (i === 'chill') return Math.max(1, Math.round(base / 2));
  if (i === 'hard') return base * 2;
  return base;
}

function draw(state) {
  if (!state.deck.length) {
    state.deck = shuffle(state.discard);
    state.discard = [];
  }
  return state.deck.pop() || null;
}

function startTurn(state) {
  state.phase = 'listen';
  state.turn = { card: draw(state), gap: null, challenges: [], bonus: false, title: false, year: false };
  state.lastResult = null;
  state.duel = null;
}

export const activePlayer = s => s.players[s.current];
export const playerById = (s, id) => s.players.find(p => p.id === id);
export const currentCard = s => (s.phase === 'duel' ? s.duel?.card : s.turn?.card);

export function fits(timeline, gap, year) {
  const left = gap > 0 ? timeline[gap - 1].year : -Infinity;
  const right = gap < timeline.length ? timeline[gap].year : Infinity;
  return left <= year && year <= right;
}

function insertSorted(timeline, card) {
  let i = 0;
  while (i < timeline.length && timeline[i].year <= card.year) i++;
  timeline.splice(i, 0, card);
  return i;
}

export function selectGap(s, gap) {
  if (s.phase !== 'listen') return;
  s.turn.gap = gap;
}

export function canSkip(s) {
  return s.phase === 'listen' && (isDrink(s) || activePlayer(s).tokens >= 1);
}

export function skip(s) {
  if (!canSkip(s)) return false;
  if (!isDrink(s)) activePlayer(s).tokens -= 1;
  s.discard.push(s.turn.card);
  s.turn = { card: draw(s), gap: null, challenges: [], bonus: false, title: false, year: false };
  return true;
}

// Song nicht abspielbar → ohne Kosten austauschen
export function replaceUnplayable(s) {
  if (s.phase === 'duel') {
    s.duel.card = draw(s);
    return;
  }
  s.turn.card = draw(s);
  s.turn.gap = null;
}

export function confirmPlacement(s) {
  if (s.phase !== 'listen' || s.turn.gap == null) return;
  s.phase = 'challenge';
}

export function takenGaps(s) {
  return new Set([s.turn.gap, ...s.turn.challenges.map(c => c.gap)]);
}

// Darf diese Person grundsätzlich kontern (Tokens bzw. Konter übrig)?
export function canChallenge(s, p) {
  if (isDrink(s)) {
    if (s.settings.drink.counter === 'off') return false;
    return p.counters == null || p.counters > 0;
  }
  return p.tokens >= 1;
}

export function challengers(s) {
  const done = new Set(s.turn.challenges.map(c => c.playerId));
  return s.players.filter((p, i) => i !== s.current && canChallenge(s, p) && !done.has(p.id));
}

export function addChallenge(s, playerId, gap) {
  const p = playerById(s, playerId);
  if (s.phase !== 'challenge' || !p || !canChallenge(s, p) || takenGaps(s).has(gap)) return;
  if (isDrink(s)) {
    if (p.counters != null) p.counters -= 1;
  } else {
    p.tokens -= 1;
  }
  s.turn.challenges.push({ playerId, gap });
}

// Bereits gesetzten Konter auf eine andere freie Lücke verschieben (kostet nichts extra)
export function moveChallenge(s, playerId, gap) {
  const c = s.turn.challenges.find(x => x.playerId === playerId);
  if (s.phase !== 'challenge' || !c || takenGaps(s).has(gap)) return;
  c.gap = gap;
}

export const challengeOf = (s, playerId) => s.turn?.challenges.find(c => c.playerId === playerId) || null;

export function removeChallenge(s, playerId) {
  const idx = s.turn.challenges.findIndex(c => c.playerId === playerId);
  if (idx < 0) return;
  const p = playerById(s, playerId);
  if (isDrink(s)) {
    if (p.counters != null) p.counters += 1;
  } else {
    p.tokens += 1;
  }
  s.turn.challenges.splice(idx, 1);
}

export function reveal(s) {
  if (s.phase !== 'challenge') return;
  const me = activePlayer(s);
  const card = s.turn.card;
  const correct = fits(me.timeline, s.turn.gap, card.year);
  // Konter vor dem Einsortieren auswerten (Lücken-Indizes beziehen sich auf die alte Zeitleiste)
  const challengeResults = s.turn.challenges.map(c => ({ playerId: c.playerId, correct: fits(me.timeline, c.gap, card.year) }));
  let winnerId = null;
  if (correct) {
    me.timeline.splice(s.turn.gap, 0, card);
    winnerId = me.id;
  } else {
    const hit = s.turn.challenges.find(c => fits(me.timeline, c.gap, card.year));
    if (hit) {
      insertSorted(playerById(s, hit.playerId).timeline, card);
      winnerId = hit.playerId;
    } else {
      s.discard.push(card);
    }
  }
  s.lastResult = { correct, winnerId, gap: s.turn.gap, challenges: challengeResults };
  s.phase = 'reveal';
  checkWinner(s);
}

export function toggleBonus(s) {
  if (s.phase !== 'reveal') return;
  const me = activePlayer(s);
  if (s.turn.bonus) {
    s.turn.bonus = false;
    if (s.turn.bonusApplied) me.tokens -= 1;
    s.turn.bonusApplied = false;
  } else {
    s.turn.bonus = true;
    s.turn.bonusApplied = me.tokens < MAX_TOKENS;
    if (s.turn.bonusApplied) me.tokens += 1;
  }
}

// Trinkspiel: „Titel & Interpret“ bzw. „Genaues Jahr“ umschalten
export function toggleFlag(s, flag) {
  if (s.phase !== 'reveal' || !isDrink(s)) return;
  s.turn[flag] = !s.turn[flag];
}

// Trinkbilanz des aktuellen Zugs – rein angesagt, nichts wird gespeichert
export function drinkTally(s) {
  const me = activePlayer(s);
  const r = s.lastResult;
  const rows = new Map(s.players.map(p => [p.id, { player: p, drink: 0, give: 0 }]));
  const add = (id, key, base) => (rows.get(id)[key] += sips(s, base));
  if (r.correct) add(me.id, 'give', SIPS.right);
  else add(me.id, 'drink', SIPS.wrong);
  if (r.winnerId && r.winnerId !== me.id) add(me.id, 'drink', SIPS.stolen);
  if (s.turn.title) add(me.id, 'give', SIPS.title);
  if (s.turn.year) for (const p of s.players) if (p.id !== me.id) add(p.id, 'drink', SIPS.year);
  for (const c of r.challenges || []) if (!c.correct) add(c.playerId, 'drink', SIPS.counterWrong);
  const exCard = r.correct && s.turn.title && s.turn.year && s.settings.drink.intensity !== 'chill';
  return {
    rows: [...rows.values()].filter(x => x.drink || x.give).sort((a, b) => b.drink - a.drink || b.give - a.give),
    exCard,
  };
}

export function canBuy(s, playerId) {
  const p = playerById(s, playerId);
  return !isDrink(s) && p && p.tokens >= BUY_COST && s.phase !== 'over';
}

export function buyCard(s, playerId) {
  if (!canBuy(s, playerId)) return null;
  const p = playerById(s, playerId);
  const card = draw(s);
  if (!card) return null;
  p.tokens -= BUY_COST;
  insertSorted(p.timeline, card);
  checkWinner(s);
  return card;
}

// Spielende mit „gleichen Zügen“:
// Erreicht jemand das Ziel, wird die Runde zu Ende gespielt (Runde = Sitzreihenfolge ab Spieler 1).
// Danach gewinnt, wer allein die meisten Karten hat. Bei Gleichstand: Stechen nur unter den Gleichstehenden,
// Runde für Runde, bis jemand allein vorne liegt.
// s.endgame = { type: 'final' | 'tiebreak', contenders: [ids] | null, queue: [Sitzindizes, die in dieser Runde noch dran sind] }
function checkWinner(s) {
  if (s.endgame || s.winner) return;
  if (!s.players.some(p => p.timeline.length >= s.settings.target)) return;
  const queue = [];
  for (let i = s.current + 1; i < s.players.length; i++) queue.push(i);
  s.endgame = { type: 'final', contenders: null, queue };
}

export const cardCount = p => p.timeline.length;

// Wer liegt vorne? Im Stechen zählen nur die Gleichstehenden.
export function leaders(s) {
  const pool = s.endgame?.contenders ? s.players.filter(p => s.endgame.contenders.includes(p.id)) : s.players;
  const max = Math.max(...pool.map(cardCount));
  return pool.filter(p => cardCount(p) === max);
}

// Bestmöglicher Kartengewinn eines Nachziehers bis Rundenende (obere Schranke):
// eigener Zug +1, Karten kaufen mit Tokens (inkl. möglichem Bonus-Token), je ein Konter/HITSTER! in den Zügen der anderen Nachzieher.
function maxGain(s, p) {
  const others = s.endgame.queue.filter(i => s.players[i].id !== p.id).length;
  const buys = isDrink(s) ? 0 : Math.floor((p.tokens + 1) / BUY_COST);
  const steals = isDrink(s) && s.settings.drink.counter === 'off' ? 0 : others;
  return 1 + buys + steals;
}

// Kann noch irgendein Nachzieher den Führenden einholen (Gleichstand reicht, dann gibt es ein Stechen)?
function anyoneCanCatchUp(s) {
  const top = cardCount(leaders(s)[0]);
  return s.endgame.queue.some(i => {
    const p = s.players[i];
    if (s.endgame.contenders && !s.endgame.contenders.includes(p.id)) return false;
    return cardCount(p) + maxGain(s, p) >= top;
  });
}

// Ist der laufende Zug der letzte vor der Auswertung?
// Auch dann, wenn die übrigen Nachzieher den Führenden rechnerisch nicht mehr einholen können.
export const isLastTurn = s => !!s.endgame && (s.endgame.queue.length === 0 || !anyoneCanCatchUp(s));

// Spieler, die in der laufenden Endrunde noch nachziehen
export const pendingPlayers = s => (s.endgame ? s.endgame.queue.map(i => s.players[i]) : []);

function shouldDuel(s) {
  return !s.endgame && isDrink(s) && s.settings.drink.duel && s.players.length >= 2 && s.turnsSinceDuel >= DUEL_MIN_GAP && Math.random() < DUEL_CHANCE;
}

export function nextTurn(s) {
  if (s.winner) {
    s.phase = 'over';
    return;
  }
  if (s.endgame) {
    if (isLastTurn(s)) {
      const top = leaders(s);
      if (top.length === 1) {
        s.winner = top[0].id;
        s.phase = 'over';
        return;
      }
      // Gleichstand → Stechen unter den Gleichstehenden, in Sitzreihenfolge
      const ids = top.map(p => p.id);
      s.endgame = { type: 'tiebreak', contenders: ids, queue: s.players.map((p, i) => (ids.includes(p.id) ? i : -1)).filter(i => i >= 0) };
    }
    s.current = s.endgame.queue.shift();
    startTurn(s);
    return;
  }
  s.current = (s.current + 1) % s.players.length;
  if (shouldDuel(s)) {
    const [a, b] = shuffle(s.players);
    s.turnsSinceDuel = 0;
    s.phase = 'duel';
    s.turn = null;
    s.lastResult = null;
    s.duel = { a: a.id, b: b.id, card: draw(s), revealed: false, loser: null };
    return;
  }
  s.turnsSinceDuel += 1;
  startTurn(s);
}

export function revealDuel(s) {
  if (s.phase === 'duel') s.duel.revealed = true;
}

// loser: Spieler-ID oder 'tie'
export function resolveDuel(s, loser) {
  if (s.phase === 'duel' && s.duel.revealed) s.duel.loser = loser;
}

export function finishDuel(s) {
  if (s.phase !== 'duel') return;
  s.discard.push(s.duel.card);
  startTurn(s);
}
