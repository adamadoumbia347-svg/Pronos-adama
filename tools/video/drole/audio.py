"""Bande-son des vidéos humoristiques : musique originale + bruitages synthétisés.
Usage : python3 audio.py sons.json <variante> sortie.wav"""
import json, sys, wave
import numpy as np
cfg = json.load(open(sys.argv[1])); V = int(sys.argv[2]); OUT = sys.argv[3]
SR = 44100; D = cfg["duree"]; N = int(SR * D)
out = np.zeros(N); rng = np.random.default_rng(V)
def add(sig, start, vol=1.0):
    i0 = int(start * SR)
    if i0 >= N: return
    n = min(len(sig), N - i0); out[i0:i0+n] += vol * sig[:n]
def tt(d): return np.arange(int(d * SR)) / SR
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def pluck(f, d=0.22, v=0.12):
    t = tt(d); return v * np.exp(-t * 14) * (np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t))
# --- musique : basse "pizzicato" + mélodie sautillante, 128 BPM ---
beat = 60 / 128
PROG = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]
MEL = [[0, 2, 4, 2, 7, 4, 2, 0], [4, 7, 9, 7, 4, 2, 4, 7], [0, 4, 7, 12, 7, 4, 2, 4]]
scale = [0, 2, 4, 5, 7, 9, 11, 12, 14]
for bar in range(int(D / (4 * beat)) + 1):
    ch = PROG[(bar + V) % 4]; t0 = bar * 4 * beat
    for k in range(4):
        add(pluck(midi(ch[0] - 24 + (7 if k % 2 else 0)), 0.3, 0.22), t0 + k * beat)
    mel = MEL[(bar + V) % len(MEL)]
    for k, deg in enumerate(mel):
        if (k + bar) % 3 == 2: continue
        add(pluck(midi(ch[0] + 12 + deg), 0.18, 0.07), t0 + k * beat / 2)
    for k in range(4):  # charleston léger
        n = rng.standard_normal(int(0.05 * SR)); add(n * np.exp(-tt(0.05) * 60), t0 + k * beat + beat / 2, 0.03)
# --- bruitages ---
def pop_(f0=500):
    t = tt(0.12); f = f0 * (1 + 2.5 * np.exp(-t * 40)); return 0.35 * np.exp(-t * 30) * np.sin(2*np.pi*np.cumsum(f)/SR)
def ding():
    t = tt(0.8); return 0.25 * np.exp(-t * 5) * (np.sin(2*np.pi*1318*t) + 0.5*np.sin(2*np.pi*1975*t))
def miaou():
    t = tt(0.55); f = 520 + 380*np.sin(np.pi*t/0.55)**1.5 - 120*t + 15*np.sin(2*np.pi*7*t)
    ph = 2*np.pi*np.cumsum(f)/SR; env = np.sin(np.pi*t/0.55)**0.7
    return 0.22 * env * (np.sin(ph) + 0.45*np.sin(2*ph) + 0.25*np.sin(3*ph))
def whoosh():
    t = tt(0.45); n = np.convolve(rng.standard_normal(len(t)), np.ones(10)/10, "same"); return 0.5 * n * np.sin(np.pi*t/0.45)**2
def boom():
    t = tt(0.6); return 0.8 * np.exp(-t*7) * np.sin(2*np.pi*(90*np.exp(-t*6)+35)*t) + 0.15*rng.standard_normal(len(t))*np.exp(-t*25)
def crash():
    t = tt(0.9); n = rng.standard_normal(len(t)) * np.exp(-t * 6)
    tinkle = sum(np.sin(2*np.pi*f*t) * np.exp(-t*(8+i)) for i, f in enumerate([2400, 3100, 3700, 4500, 5200]))
    return 0.35 * n + 0.08 * tinkle
def scratch():
    t = tt(0.35); f = 900 * np.exp(-t * 6) + 80; return 0.3 * np.sign(np.sin(2*np.pi*np.cumsum(f)/SR)) * np.exp(-t*4)
def ouaf():
    s = np.zeros(int(0.45 * SR))
    for k, d0 in enumerate([0.0, 0.2]):
        t = tt(0.16); f = 330 + 260 * np.exp(-t * 18)
        ph = 2*np.pi*np.cumsum(f)/SR
        b = (np.sin(ph) + 0.6*np.sin(2*ph) + 0.3*np.sin(3*ph)) + 0.25*rng.standard_normal(len(t))
        b *= np.exp(-t * 16) * np.minimum(1, t * 120) * 0.3
        i0 = int(d0 * SR); s[i0:i0+len(b)] += b
    return s
def fete():
    s = np.zeros(int(0.8 * SR))
    for i, m in enumerate([72, 76, 79, 84, 88]):
        p = pluck(midi(m), 0.3, 0.18); i0 = int(i * 0.07 * SR); s[i0:i0+len(p)] += p[:len(s)-i0]
    return s
FX = {"pop": lambda: pop_(500), "pop2": lambda: pop_(700), "ding": ding, "miaou": miaou, "whoosh": whoosh,
      "boom": boom, "crash": crash, "scratch": scratch, "fete": fete, "ouaf": ouaf}
musique = out.copy(); out[:] = 0
for e in cfg["sons"]: add(FX[e["type"]](), e["t"])
# baisse la musique pendant les bruitages forts, puis mixe
mix = 0.55 * musique + out
fade = int(0.8 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = np.tanh(mix / max(1e-9, np.max(np.abs(mix))) * 1.2) * 0.9
with wave.open(OUT, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
