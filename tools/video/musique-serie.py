# Petite musique originale (synthèse), 24 s, 120 BPM, avec "whoosh" aux changements de scène.
import numpy as np, wave, sys
V = int(sys.argv[1]); SORTIE = sys.argv[2]
SR = 44100; D = 22.0; N = int(SR * D)
t = np.arange(N) / SR
out = np.zeros(N)
beat = 0.5  # 120 BPM
rng_arp = V
def note(f, start, dur, vol=0.18, kind="pluck"):
    i0 = int(start * SR); n = int(dur * SR)
    if i0 >= N: return
    n = min(n, N - i0); tt = np.arange(n) / SR
    if kind == "pluck":
        env = np.exp(-tt * 6)
        sig = np.sin(2*np.pi*f*tt) + 0.35*np.sin(2*np.pi*2*f*tt) + 0.12*np.sin(2*np.pi*3*f*tt)
    else:  # pad
        env = np.minimum(1, tt / 0.3) * np.minimum(1, (dur - tt) / 0.3)
        sig = np.sin(2*np.pi*f*tt) + 0.5*np.sin(2*np.pi*f*1.005*tt)
    out[i0:i0+n] += vol * env * sig
def midi(m): return 440 * 2 ** ((m - 69) / 12)
# Progression C - Am - F - G (2 temps x 4 par accord = 2 s)
PROG = [
 [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]],
 [[62, 65, 69], [58, 62, 65], [60, 64, 67], [57, 60, 64]],
 [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]],
 [[57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]],
 [[65, 69, 72], [62, 65, 69], [58, 62, 65], [60, 64, 67]],
 [[55, 59, 62], [60, 64, 67], [57, 60, 64], [53, 57, 60]]]
chords = PROG[V % len(PROG)]
for bar in range(int(D / 2)):
    ch = chords[bar % 4]
    for m in ch: note(midi(m - 12), bar * 2, 2.0, 0.05, "pad")
    note(midi(ch[0] - 24), bar * 2, 0.45, 0.22)       # basse
    note(midi(ch[0] - 24), bar * 2 + 1.0, 0.45, 0.18)
    # arpège enjoué en croches
    arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]
    for k, m in enumerate(arp):
        if bar == 0 and k < 2: continue
        note(midi(m + 12), bar * 2 + k * 0.25, 0.25, 0.07)
# percussions : kick sur chaque temps, clap sur 2 et 4
for k in range(int(D / beat)):
    s = k * beat; i0 = int(s * SR); n = int(0.25 * SR)
    if i0 + n > N: break
    tt = np.arange(n) / SR
    out[i0:i0+n] += 0.5 * np.sin(2*np.pi*(110*np.exp(-tt*25)+45)*tt) * np.exp(-tt*14)
    if k % 2 == 1:
        nz = np.random.default_rng(k).standard_normal(int(0.12*SR))
        out[i0:i0+len(nz)] += 0.12 * nz * np.exp(-np.arange(len(nz))/SR*30)
# whoosh aux transitions
for s in [3.2, 5.4, 9.6, 13.8, 18.0]:
    i0 = int((s - 0.3) * SR); n = int(0.5 * SR); tt = np.arange(n) / SR
    nz = np.random.default_rng(int(s*10)).standard_normal(n)
    env = np.sin(np.pi * tt / 0.5) ** 2
    # filtre passe-bas grossier glissant (moyenne mobile)
    nz = np.convolve(nz, np.ones(8)/8, mode="same")
    out[i0:i0+n] += 0.18 * nz * env
# fondu de fin
fade = int(1.2 * SR); out[-fade:] *= np.linspace(1, 0, fade)
out = out / np.max(np.abs(out)) * 0.85
pcm = (out * 32767).astype(np.int16)
with wave.open(SORTIE, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok")
