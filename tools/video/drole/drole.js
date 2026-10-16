// Outils d'animation communs (temps t en secondes, rendu déterministe image par image)
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const easeOut = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const p = (t, s, d) => clamp((t - s) / d);
function pop(el, t, s, d = 0.35) { const k = p(t, s, d); el.style.opacity = k > 0 ? 1 : 0; el.style.transform = `scale(${k > 0 ? back(k) : 0})`; }
function slide(el, t, s, d = 0.35, dx = 0, dy = 40) { const k = easeOut(p(t, s, d)); el.style.opacity = k; el.style.transform = `translate(${(1 - k) * dx}px, ${(1 - k) * dy}px)`; }
function hide(el, t, s, d = 0.25) { if (t >= s) el.style.opacity = String(Math.min(+el.style.opacity || 0, 1 - p(t, s, d))); }
// Sons : liste d'événements {t, type} lue par le script de rendu pour fabriquer la bande-son
window.SONS = [];
function son(t, type) { window.SONS.push({ t, type }); }
