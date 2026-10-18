"""Procedural audio for The Common Cents: ragtime piano bed, 1930s cartoon sound effects, and the final mix.
Everything is synthesised with numpy, so there is nothing to license."""
import subprocess
import numpy as np

SR = 44100
MUSIC_LEVEL = 0.09   # background bed (before ducking)
DUCK = 0.7           # how far the music dips under the voice (0..1)
SFX_LEVEL = 0.16     # sound effects
DOC_LEVEL = 0.11     # long-form documentary underscore (softer timbre than the ragtime, so a touch higher)
_rng = np.random.default_rng(11)

def _t(dur): return np.arange(int(SR * dur)) / SR

def _env(n, attack=0.004, release=0.03):
    e = np.ones(n)
    a, r = min(n, int(SR * attack)), min(n, int(SR * release))
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def band(x, lo=None, hi=None):
    """Zero-phase FFT band filter (no scipy here)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    if lo: X[f < lo] *= (f[f < lo] / lo) ** 2
    if hi: X[f > hi] *= (hi / f[f > hi]) ** 2
    return np.fft.irfft(X, len(x))

def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1
    return x / m * peak

# ---------- piano + ragtime ----------
def midi_hz(m): return 440 * 2 ** ((m - 69) / 12)

def piano(m, dur, vel=1.0):
    f, t = midi_hz(m), _t(dur)
    sig = np.zeros_like(t)
    for detune in (1.0, 1.0035):                       # two slightly-off strings: honky-tonk
        for k in range(1, 8):
            sig += (1 / k ** 1.15) * np.sin(2 * np.pi * k * f * detune * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k))
    return sig * _env(len(t)) * vel / 6

CHORDS = {"C": (0, [0, 4, 7]), "C7": (0, [0, 4, 7, 10]), "G7": (7, [7, 11, 2, 5]), "F": (5, [5, 9, 0]),
          "Fm": (5, [5, 8, 0]), "A7": (9, [9, 1, 4, 7]), "D7": (2, [2, 6, 9, 0])}
PROG = ["C", "C", "G7", "G7", "C", "C7", "F", "Fm", "C", "A7", "D7", "G7", "C", "F", "C", "G7"]

def ragtime(seconds, bpm=112):
    """Stride left hand (bass on 1 & 3, chord stabs on 2 & 4) + syncopated 3-3-2 right-hand arpeggios."""
    beat = 60 / bpm; bar = 4 * beat; s16 = beat / 4
    loop_len = int(SR * bar * len(PROG))
    out = np.zeros(loop_len + SR * 2)
    def put(at, sig):
        i = int(at * SR); out[i:i + len(sig)] += sig[:len(out) - i]
    for b, name in enumerate(PROG):
        root, tones = CHORDS[name]; t0 = b * bar
        put(t0, piano(36 + root, 0.9, 0.9)); put(t0 + 2 * beat, piano(36 + (root + 7) % 12, 0.9, 0.8))
        stab = sorted(55 + ((p - 55) % 12) for p in tones)
        for k in (1, 3):
            for p in stab: put(t0 + k * beat, piano(p, 0.35, 0.33))
        mel = sorted(72 + ((p - 72) % 12) for p in tones) + [84 + ((tones[0] - 84) % 12)]
        if b % 2: mel = mel[::-1]
        pos = [0, 3, 6, 8, 11, 14]
        for j, p16 in enumerate(pos):
            nxt = pos[j + 1] if j + 1 < len(pos) else 16
            put(t0 + p16 * s16, piano(mel[j % len(mel)], (nxt - p16) * s16 + 0.25, 0.6 + 0.15 * (p16 % 8 == 0)))
    loop = out[:loop_len] + np.pad(out[loop_len:], (0, loop_len - len(out[loop_len:])))[:loop_len]
    reps = int(np.ceil(seconds * SR / loop_len)) + 1
    music = np.tile(loop, reps)[:int(seconds * SR)]
    music = band(music, lo=180, hi=3800)                       # old-record bandwidth
    crackle = np.zeros_like(music)
    idx = _rng.integers(0, len(music), size=int(seconds * 18))
    crackle[idx] = _rng.uniform(-1, 1, size=len(idx)) * 0.6
    hiss = band(_rng.standard_normal(len(music)), lo=2000, hi=8000) * 0.012
    return norm(music) * 0.9 + crackle * 0.25 + hiss

# ---------- documentary underscore (long-form doodle videos) ----------
def _pad(m, dur):
    """Soft synth pad note: detuned partials, slow attack and release."""
    f, t = midi_hz(m), _t(dur)
    sig = sum((1 / k ** 1.6) * np.sin(2 * np.pi * k * f * dt * t + k) for k in range(1, 6) for dt in (0.997, 1.003))
    env = np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 1.2).clip(0)
    return sig * env / 8

def _pluck(m, dur=0.9, vel=1.0):
    """Marimba-ish pluck."""
    f, t = midi_hz(m), _t(dur)
    sig = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)
    return sig * np.exp(-t * 6) * _env(len(t), 0.002, 0.05) * vel / 2

DOC_PROGS = [   # (root midi, chord tones as semitones above root) per bar
    [(57, (0, 3, 7)), (53, (0, 4, 7)), (48, (0, 4, 7)), (55, (0, 4, 7))],          # Am F C G   (curious)
    [(50, (0, 3, 7)), (57, (0, 3, 7)), (53, (0, 4, 7)), (52, (0, 4, 7))],          # Dm Am F E  (tension)
    [(48, (0, 4, 7)), (55, (0, 4, 7)), (57, (0, 3, 7)), (53, (0, 4, 7))],          # C G Am F   (resolution)
]

def underscore(seconds, variant=0, bpm=84):
    """One looping documentary bed: pad chords, soft 8th-note plucks, a low pulse on beats 1 and 3."""
    beat = 60 / bpm; bar = 4 * beat
    prog_ = DOC_PROGS[variant % len(DOC_PROGS)] * 2
    loop_len = int(SR * bar * len(prog_))
    out = np.zeros(loop_len + SR * 3)
    def put(at, sig):
        i = int(at * SR); out[i:i + len(sig)] += sig[:len(out) - i]
    rng = np.random.default_rng(variant + 5)
    for b, (root, tones) in enumerate(prog_):
        t0 = b * bar
        for tn in tones: put(t0, _pad(root + tn, bar + 1.2) * 0.9)
        put(t0, _pad(root - 12, bar + 1.2) * 0.7)
        for k in (0, 2):
            tt = _t(0.4); put(t0 + k * beat, np.sin(2 * np.pi * midi_hz(root - 24) * tt) * np.exp(-tt * 8) * 0.5)
        arp = [root + 12 + tones[i % len(tones)] + (12 if i >= 3 else 0) for i in range(6)]
        for j in range(8):
            if variant == 1 and j % 2: continue
            put(t0 + j * beat / 2, _pluck(arp[(j * 2 + b) % len(arp)], 0.9, 0.5 + 0.2 * (j % 4 == 0) + rng.uniform(-0.08, 0.08)))
    loop = out[:loop_len] + np.pad(out[loop_len:], (0, loop_len - len(out[loop_len:])))[:loop_len]
    loop = band(loop, lo=60, hi=6000)
    reps = int(np.ceil(seconds * SR / loop_len)) + 1
    return norm(np.tile(loop, reps)[:int(seconds * SR)])

def doc_bed(total, sections):
    """Underscore that changes variant at each chapter start, with 1.5 s crossfades."""
    n = int(SR * total)
    cuts = [0.0] + [c for c in sorted(sections) if 0 < c < total] + [total]
    out = np.zeros(n + SR * 2)
    for k in range(len(cuts) - 1):
        a, b = cuts[k], min(total, cuts[k + 1] + 1.5)
        seg = underscore(b - a + 0.1, variant=k)[:int(SR * (b - a))]
        fade = np.ones(len(seg)); x = min(len(seg), int(SR * 1.5))
        if k: fade[:x] = np.linspace(0, 1, x)
        if k < len(cuts) - 2: fade[-x:] *= np.linspace(1, 0, x)
        i = int(SR * a); out[i:i + len(seg)] += (seg * fade)[:len(out) - i]
    return out[:n]

# ---------- sound effects ----------
def sfx_pop():
    t = _t(0.08); f = 900 - 6000 * t
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40)

def sfx_chaching():
    def bell(dur):
        t = _t(dur)
        return sum(a * np.sin(2 * np.pi * f * t) for f, a in ((2093, 1), (2637, .7), (3136, .6), (4186, .4))) * np.exp(-t * 7)
    click = band(_rng.standard_normal(int(SR * 0.02)), lo=1500) * np.exp(-_t(0.02) * 200)
    out = np.zeros(int(SR * 0.9))
    out[:len(click)] += click * 0.8
    out[int(SR * 0.11):int(SR * 0.11) + int(SR * 0.7)] += bell(0.7)[:len(out) - int(SR * 0.11)]
    return norm(out)

def sfx_coins(n=7):
    out = np.zeros(int(SR * (0.07 * n + 0.4)))
    for k in range(n):
        t = _t(0.25); f = _rng.uniform(3000, 5200)
        ping = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 18)
        i = int(SR * (k * 0.07 + _rng.uniform(0, 0.03))); out[i:i + len(ping)] += ping[:len(out) - i]
    return norm(out)

def sfx_boing():
    t = _t(0.7); f = 170 * (1 + 0.5 * np.sin(2 * np.pi * 9 * t) * np.exp(-4 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return norm((np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-t * 3.5) * _env(len(t)))

def sfx_slide(up=True, dur=0.65):
    t = _t(dur); a, b = (480, 1500) if up else (1500, 480)
    f = a * (b / a) ** (t / dur) * (1 + 0.02 * np.sin(2 * np.pi * 6 * t))
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) ** 0.5)

def sfx_whoosh(dur=0.5):
    n = band(_rng.standard_normal(int(SR * dur)), lo=300, hi=2500)
    return norm(n * np.sin(np.pi * _t(dur) / dur) ** 2)

def sfx_honk():
    out = np.zeros(int(SR * 0.6))
    for st in (0.0, 0.28):
        t = _t(0.22)
        tone = np.sign(np.sin(2 * np.pi * 392 * t)) + np.sign(np.sin(2 * np.pi * 494 * t))
        i = int(SR * st); out[i:i + len(t)] += tone * _env(len(t), 0.01, 0.04)
    return norm(band(out, hi=2500))

def sfx_glug(n=4):
    out = np.zeros(int(SR * (0.14 * n + 0.2)))
    for k in range(n):
        t = _t(0.11); f = 160 + 1600 * t + _rng.uniform(-20, 20)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.11)
        i = int(SR * k * 0.14); out[i:i + len(b)] += b
    return norm(out)

def sfx_drumroll(dur=1.0):
    out = np.zeros(int(SR * (dur + 0.3)))
    hit = band(_rng.standard_normal(int(SR * 0.05)), lo=200, hi=5000) * np.exp(-_t(0.05) * 60)
    k = 0.0
    while k < dur:
        i = int(SR * k); out[i:i + len(hit)] += hit * (0.4 + 0.6 * k / dur)
        k += 1 / 26
    return norm(out)

def sfx_stamp():
    t = _t(0.35); f = 110 * np.exp(-t * 6) + 45
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    crack = band(_rng.standard_normal(len(t)), lo=800) * np.exp(-t * 60) * 0.5
    return norm(thump + crack)

def sfx_cymbal():
    t = _t(1.4)
    return norm(band(_rng.standard_normal(len(t)), lo=4000) * np.exp(-t * 3))

def sfx_tick(dur=1.6, rate=4):
    out = np.zeros(int(SR * (dur + 0.1)))
    for k in range(int(dur * rate)):
        t = _t(0.03); f = 3200 if k % 2 == 0 else 2500
        c = np.sin(2 * np.pi * f * t) * np.exp(-t * 180)
        i = int(SR * k / rate); out[i:i + len(c)] += c
    return norm(out)

def sfx_click():
    t = _t(0.03)
    return norm(band(_rng.standard_normal(len(t)), lo=2000) * np.exp(-t * 250))

def sfx_paper(dur=0.35):
    n = band(_rng.standard_normal(int(SR * dur)), lo=1500, hi=7000)
    am = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 23 * _t(dur)))
    return norm(n * am * np.sin(np.pi * _t(dur) / dur))

def sfx_type(n=6):
    out = np.zeros(int(SR * (0.09 * n + 0.1)))
    for k in range(n):
        c = sfx_click() * _rng.uniform(0.6, 1)
        i = int(SR * (k * 0.09 + _rng.uniform(0, 0.02))); out[i:i + len(c)] += c[:len(out) - i]
    return norm(out)

def sfx_bell():
    t = _t(1.5)
    return norm(sum(a * np.sin(2 * np.pi * f * t) for f, a in ((880, 1), (1760, .4), (2640, .2))) * np.exp(-t * 3))

def sfx_impact():
    t = _t(0.9); f = 70 * np.exp(-t * 3) + 30
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4) + band(_rng.standard_normal(len(t)), hi=600) * np.exp(-t * 12) * 0.4)

def sfx_soft_pop():
    t = _t(0.12); f = 500 + 900 * np.exp(-t * 40)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35))

SFX = dict(click=sfx_click, paper=sfx_paper, type=sfx_type, bell=sfx_bell, impact=sfx_impact, soft_pop=sfx_soft_pop,
           tick=sfx_tick, pop=sfx_pop, chaching=sfx_chaching, coins=sfx_coins, boing=sfx_boing, whoosh=sfx_whoosh, honk=sfx_honk,
           glug=sfx_glug, drumroll=sfx_drumroll, stamp=sfx_stamp, cymbal=sfx_cymbal,
           slide_up=lambda: sfx_slide(True), slide_down=lambda: sfx_slide(False))

# ---------- mix ----------
def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)

def mix(total, voice_parts, events, music=True, out="mix.wav", sections=()):
    """voice_parts: [(start_s, samples)], events: [(time_s, sfx_name, gain)]. Music ducks under the voice."""
    n = int(SR * (total + 0.5))
    voice = np.zeros(n); fx = np.zeros(n)
    for st, s in voice_parts:
        i = int(st * SR); voice[i:i + len(s)] += s[:n - i]
    cache = {}
    for at, name, gain in events:
        if name not in cache: cache[name] = SFX[name]()
        s = cache[name]; i = max(0, int(at * SR)); fx[i:i + len(s)] += s[:n - i] * gain
    bed = np.zeros(n)
    if music:
        bed = (doc_bed(total + 0.5, sections) if music == "doc" else ragtime(total + 0.5))[:n]
        env = np.convolve(np.abs(voice), np.ones(int(SR * 0.12)) / (SR * 0.12), mode="same")
        duck = 1 - DUCK * np.clip(env / (np.max(env) * 0.25 + 1e-9), 0, 1)
        fade = np.clip(np.minimum(np.arange(n) / (SR * 0.4), (n - np.arange(n)) / (SR * 1.2)), 0, 1)
        bed = bed * duck * fade * (DOC_LEVEL if music == "doc" else MUSIC_LEVEL)
    y = norm(voice) * 0.92 + bed + fx * SFX_LEVEL
    y = np.tanh(y * 1.1) / np.tanh(1.1)                         # gentle limiter
    pcm = (np.clip(y, -1, 1) * 32767).astype("<i2").tobytes()
    import wave
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)
    return out
