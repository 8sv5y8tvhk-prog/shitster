// Deezer-API per JSONP (kein CORS-Proxy nötig). Preview-Links laufen ab,
// deshalb wird zu jeder Karte erst beim Abspielen der frische Link geholt.

const cache = new Map();

function jsonp(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const cb = '__dz' + Math.random().toString(36).slice(2);
    const script = document.createElement('script');
    const timer = setTimeout(() => done(new Error('timeout')), timeout);
    function done(err, data) {
      clearTimeout(timer);
      delete window[cb];
      script.remove();
      err ? reject(err) : resolve(data);
    }
    window[cb] = data => done(null, data);
    script.onerror = () => done(new Error('network'));
    script.src = `${url}${url.includes('?') ? '&' : '?'}output=jsonp&callback=${cb}`;
    document.head.appendChild(script);
  });
}

export async function getTrack(id) {
  const hit = cache.get(id);
  if (hit && hit.expires > Date.now()) return hit.data;
  const d = await jsonp(`https://api.deezer.com/track/${id}`);
  if (d.error) throw new Error(d.error.message || 'deezer');
  const data = {
    preview: d.preview || null,
    playable: !!d.preview && d.readable !== false,
    cover: d.album?.cover_xl || d.album?.cover_big || null,
    link: d.link,
  };
  cache.set(id, { data, expires: Date.now() + 10 * 60 * 1000 });
  return data;
}
