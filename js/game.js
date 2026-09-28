// Reine Spiellogik – ein serialisierbares State-Objekt, keine DOM-Zugriffe.
// So lässt sich der State später 1:1 über einen Echtzeit-Dienst (Option B) synchronisieren.

export const START_TOKENS = 2;
export const MAX_TOKENS = 5;
export const BUY_COST = 3;

const PLAYER_COLORS = ['#FF375F', '#0A84FF', '#30D158', '#FF9F0A', '#BF5AF2', '#64D2FF', '#FFD60A', '#FF6482', '#5E5CE6', '#AC8E68'];

export function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export function createGame({ names, songs, target, categories }) {
  const seen = new Set();
  const unique = songs.filter(s => !seen.has(s.id) && seen.add(s.id));
  const state = {
    version: 1,
    createdAt: Date.now(),
    settings: { target, categories },
    players: names.map((name, i) => ({
      id: 'p' + i,
      name,
      color: PLAYER_COLORS[i % PLAYER_COLORS.length],
      tokens: START_TOKENS,
      timeline: [],
    })),
    deck: shuffle(unique),
    discard: [],
    current: 0,
    phase: 'listen',
    turn: null,
    lastResult: null,
    winner: null,
  };
  for (const p of state.players) p.timeline.push(draw(state));
  startTurn(state);
  return state;
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
  state.turn = { card: draw(state), gap: null, challenges: [], bonus: false };
  state.lastResult = null;
}

export const activePlayer = s => s.players[s.current];
export const playerById = (s, id) => s.players.find(p => p.id === id);

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
  return s.phase === 'listen' && activePlayer(s).tokens >= 1;
}

export function skip(s) {
  if (!canSkip(s)) return false;
  activePlayer(s).tokens -= 1;
  s.discard.push(s.turn.card);
  s.turn = { card: draw(s), gap: null, challenges: [], bonus: false };
  return true;
}

// Song nicht abspielbar → ohne Kosten austauschen
export function replaceUnplayable(s) {
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

export function challengers(s) {
  const done = new Set(s.turn.challenges.map(c => c.playerId));
  return s.players.filter((p, i) => i !== s.current && p.tokens >= 1 && !done.has(p.id));
}

export function addChallenge(s, playerId, gap) {
  const p = playerById(s, playerId);
  if (s.phase !== 'challenge' || !p || p.tokens < 1 || takenGaps(s).has(gap)) return;
  p.tokens -= 1;
  s.turn.challenges.push({ playerId, gap });
}

export function removeChallenge(s, playerId) {
  const idx = s.turn.challenges.findIndex(c => c.playerId === playerId);
  if (idx < 0) return;
  playerById(s, playerId).tokens += 1;
  s.turn.challenges.splice(idx, 1);
}

export function reveal(s) {
  if (s.phase !== 'challenge') return;
  const me = activePlayer(s);
  const card = s.turn.card;
  const correct = fits(me.timeline, s.turn.gap, card.year);
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
  s.lastResult = { correct, winnerId, gap: s.turn.gap };
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

export function canBuy(s, playerId) {
  const p = playerById(s, playerId);
  return p && p.tokens >= BUY_COST && s.phase !== 'over';
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

function checkWinner(s) {
  const w = s.players.find(p => p.timeline.length >= s.settings.target);
  if (w && !s.winner) s.winner = w.id;
}

export function nextTurn(s) {
  if (s.winner) {
    s.phase = 'over';
    return;
  }
  s.current = (s.current + 1) % s.players.length;
  startTurn(s);
}
