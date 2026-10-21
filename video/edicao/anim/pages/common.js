// Utilitários comuns: tempo determinístico, easing e beats escaláveis.
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, u) => a + (b - a) * u;
const ease = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
// progresso suavizado 0..1 iniciando em t0 e durando d
const prog = (t, t0, d = 0.7) => ease((t - t0) / d);
// janela visível: entra em t0, sai terminando em t1
const win = (t, t0, t1, fi = .6, fo = .6) => Math.min(prog(t, t0, fi), 1 - prog(t, t1 - fo, fo));
const $ = id => document.getElementById(id);
const css = (el, o) => Object.assign((typeof el === 'string' ? $(el) : el).style, o);
// entrada suave (fade + subida)
function fadeUp(el, u, dy = 30) {
  el = typeof el === 'string' ? $(el) : el;
  el.style.opacity = u;
  el.style.transform = `translateY(${(1 - u) * dy}px)`;
}

// Configuração vinda do renderizador (window.__ANIM) ou da querystring (?dur=12&beats={...}&alpha=1)
function setupAnim(name, defDur, defBeats) {
  const q = new URLSearchParams(location.search);
  const cfg = Object.assign({}, window.__ANIM || {});
  if (!cfg.dur && q.get('dur')) cfg.dur = parseFloat(q.get('dur'));
  if (!cfg.beats && q.get('beats')) cfg.beats = JSON.parse(q.get('beats'));
  if (cfg.alpha === undefined && q.get('alpha')) cfg.alpha = q.get('alpha') === '1';
  const dur = cfg.dur || defDur;
  const k = dur / defDur;
  const B = {};
  for (const n in defBeats) B[n] = defBeats[n] * k;          // escala proporcional
  if (cfg.beats) for (const n in cfg.beats) B[n] = +cfg.beats[n]; // sobrescreve (segundos absolutos)
  window.META = { name, defDur, defBeats, dur, beats: B };
  if (cfg.alpha) { document.body.classList.add('alpha'); document.documentElement.style.background = 'transparent'; }
  return { dur, B, alpha: !!cfg.alpha };
}

// Gera HTML de uma linha de código com realce simples
const KW = ['int', 'float', 'bool', 'void', 'if', 'return', 'true', 'false', 'const', 'unsigned', 'long'];
function hlCode(s) {
  const esc = x => x.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  let cm = '';
  const i = s.indexOf('//');
  if (i >= 0) { cm = s.slice(i); s = s.slice(0, i); }
  let out = esc(s).replace(/\b([A-Za-z_]\w*)\b|\b(\d+(?:\.\d+)?f?)\b/g, (m, w, n) => {
    if (w && KW.includes(w)) return `<span class="kw">${w}</span>`;
    if (w && /^[A-Z_][A-Z0-9_]+$/.test(w)) return `<span class="tok-${w}">${w}</span>`;
    if (n) return `<span class="num">${n}</span>`;
    return m;
  });
  if (cm) out += `<span class="cm">${esc(cm)}</span>`;
  return out;
}
