# -*- coding: utf-8 -*-
"""BIBLIOTECA de la música de Lyria (y de los SFX de ElevenLabs) ya generada en todos los videos, para REUTILIZARLA sin depender
de la API (pedido del usuario, 21-oct-2026: «hemos creado mucha música con Google… crea una biblioteca con etiquetas para que la
puedas reutilizar a futuro»). Regla de uso y de saldos: docs/apis.md · cómo se usa: docs/musica_biblioteca.md.

Qué guarda cada pieza (nucleo/datos/musica_biblioteca.json, versionado en git; el audio NO va a git):
  id «<video>__<archivo>», video, canal, estilo del video, tramo y escenas que cubría, el PROMPT exacto con que se pidió
  (audio/prompt_tramoN.txt o el LYRIA de guion.py), secciones con intensidad, etiquetas en español (instrumentos, ánimo, género,
  canal) y medidas del audio (duración, tempo, volumen, brillo, curva de energía en 12 puntos, huecos de silencio).
  La copia de cada pieza vive en E:\\FabricaAnimaciones\\musica_biblioteca\\<id>.mp3 (los .wav se pasan a mp3 320k): así sobrevive
  aunque se borre o se limpie el video de origen.

Uso (desde C:\\FabricaAnimaciones; también `python fab.py biblioteca …`):
  python nucleo/musica_biblioteca.py catalogar [--procs 8]          escanea, copia, mide y etiqueta (solo lo nuevo) + catálogo .md
  python nucleo/musica_biblioteca.py reetiquetar                    tras cambiar las tablas de etiquetas (no copia ni mide)
  python nucleo/musica_biblioteca.py buscar tierno piano cuna [--min 60] [--max 120] [--canal logia] [-n 12]
  python nucleo/musica_biblioteca.py ver <id>                       ficha completa (prompt, secciones, curva, usos)
  python nucleo/musica_biblioteca.py sugerir <video> [--excluir la_sena jalpa] [-n 5]
                                       para cada tramo de LYRIA del video: las piezas que mejor casan (texto + duración + intensidad)
  python nucleo/musica_biblioteca.py usar <id> <video> <tramo> [--desde 12.5]
                                       deja la pieza como videos/<v>/audio/lyria_tramoN.mp3 ya a la medida del tramo (recorte con
                                       fundido o bucle con cruce de 3 s) y anota el uso; luego `lyria_tramos.py armar` como siempre
  python nucleo/musica_biblioteca.py sfx catalogar | sfx buscar plato roto [-n 10] | sfx usar <id> <video>
                                       los efectos de ElevenLabs de videos/*/sfx/ con el prompt de su fx_audio.py/efectos.py
"""
import argparse
import ast
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from multiprocessing import Pool

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VIDEOS = os.path.join(RAIZ, "videos")
BIB = r"E:\FabricaAnimaciones\musica_biblioteca"
BIB_SFX = r"E:\FabricaAnimaciones\sfx_biblioteca"
JSON_M = os.path.join(RAIZ, "nucleo", "datos", "musica_biblioteca.json")
JSON_S = os.path.join(RAIZ, "nucleo", "datos", "sfx_biblioteca.json")
CATALOGO = os.path.join(RAIZ, "docs", "musica_biblioteca_catalogo.md")
EXTRA = [r"D:\videosnuevos"]          # sistema viejo (Platitube/googleimagenes): carpetas */*/music/*.mp3
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe" if os.path.exists(r"C:\ffmpeg\bin\ffmpeg.exe") else "ffmpeg"
EXT = (".mp3", ".wav", ".m4a", ".ogg", ".flac")

# ── etiquetas: palabra del prompt (inglés) → etiqueta en español ──────────────────────────────────────────────────
INSTRUMENTOS = {
    "piano": ["piano"], "guitarra": ["guitar", "requinto"], "cuerdas": ["string ensemble", "strings", "string section", "viola"],
    "violín": ["violin", "fiddle"], "cello": ["cello"], "cajita de música": ["music box", "music-box"],
    "banda de viento": ["brass band", "tuba", "small-town band"], "metales": ["brass", "trumpet", "trombone"],
    "cornos": ["french horn", "horns", " horn"], "coro": ["choir", "choral", "chant", "voices pad", "vocal pad"],
    "sintetizador": ["synth", "synthesizer", "analog", "arpeggiat"], "percusión": ["drum", "percussion", "taiko", "timpani", "toms"],
    "arpa": ["harp"], "flauta": ["flute", "recorder", "pan pipe"], "silbido": ["whistle", "whistled"], "órgano": ["organ"],
    "campanas": ["bell", "chime", "celesta", "glockenspiel"], "marimba": ["marimba", "xylophone", "vibraphone"],
    "pizzicato": ["pizzicato"], "chiptune": ["chiptune", "8-bit", "8 bit", "chip-tune"], "laúd": ["lute", "mandolin", "oud"],
    "drone": ["drone"], "contrabajo": ["double bass", "upright bass", "bassline", "bass line"], "saxofón": ["sax"],
    "acordeón": ["accordion"], "ukulele": ["ukulele"], "gaita": ["bagpipe"], "tambores tribales": ["tribal drum", "war drum"],
}
ANIMO = {
    "tierno": ["tender", "gentle", "lullaby", "cradle", "sweet", "intimate", "loving"],
    "cálido": ["warm"], "triste": ["sad", "melanchol", "heartbreak", "grief", "lonely", "sorrow", "mourn", "tragic", "loss"],
    "esperanza": ["hope", "uplift", "major key", "optimis", "redemption"], "tenso": ["tense", "tension", "uneasy", "suspense", "anxious", "unsettling", "nervous"],
    "oscuro": ["dark", "ominous", "sinister", "menacing", "grim", "foreboding", "shadow"],
    "terror": ["horror", "creepy", "eerie", "dread", "scary", "haunt", "nightmare"],
    "épico": ["epic", "heroic", "triumph", "battle", "majestic", "grand ", "glorious"],
    "misterio": ["mystery", "mysterious", "investigat", "enigma", "detective", "secret"],
    "juguetón": ["playful", "whimsical", "quirky", "comic", "funny", "bouncy", "mischiev", "silly", "cartoon", "goofy"],
    "curioso": ["curious", "wonder", "discover", "explor", "fascinat"], "nostálgico": ["nostalg", "childhood", "vintage", "memory"],
    "calma": ["calm", "peaceful", "serene", "ambient", "relax", "meditat"],
    "emotivo": ["emotional", "swell", "climax", "moving", "cathartic", "crying", "tears"],
    "noir": ["noir", "smoky", "jazz club"], "acción": ["action", "driving", "urgent", "chase", "energetic", "propulsive"],
    "fiesta": ["festive", "celebrat", "party", "carnival", "fair "], "solemne": ["solemn", "sacred", "hymn", "requiem", "funeral", "reverent"],
    "rabia": ["anger", "angry", "rage", "aggressive", "furious"], "frío": ["cold", "icy", "frozen", "winter"],
}
GENERO = {
    "documental": ["documentary"], "cinematográfico": ["cinematic", "film score", "orchestral", "score"],
    "folk mexicano": ["mexican", "mariachi", "requinto", "ranchera", "son jarocho", "norteño", "huapango"],
    "fantasía medieval": ["medieval", "fantasy", "elven", "orc", "tavern", "celtic", "nordic", "viking", "dwarven", "skyrim", "warcraft"],
    "jazz": ["jazz", "swing", "bebop"], "electrónica": ["electronic", "synthwave", "techno", "lo-fi", "lofi", "edm"],
    "retro videojuego": ["chiptune", "8-bit", "retro game", "arcade", "video game", "nintendo"], "vals": ["waltz"],
    "western": ["western", "spaghetti"], "oriental": ["chinese", "japanese", "koto", "erhu", "shakuhachi", "persian", "arabic", "egypt"],
    "infantil": ["children", "kids", "nursery", "lullaby"], "thriller": ["thriller", "suspense"], "terror": ["horror"],
    "ciencia ficción": ["sci-fi", "outer space", "cosmic", "futurist", "spaceship"], "naturaleza": ["nature", "forest", "wildlife", "insect", "animal"],
}


def _pal(txt):
    return re.findall(r"[a-záéíóúñü0-9']+", txt.lower())


NEGADO = re.compile(r"\b(?:no|never|without|avoid|not)\b[^.;:\n]*")   # «No drum kit, no pop…» no etiqueta percusión


# texto fijo que lyria.py / lyria_tramos.py ponen en TODOS los prompts: no describe la pieza (daba «calma» a 193 de 245)
PLANTILLA = ["it must leave room for a narrator: keep the middle frequencies calm, no lead melody competing with speech.",
             "keep the middle frequencies calm", "end with a natural fade-out.", "instrumental only, no vocals, no singing, no spoken words.",
             "instrumental only, no vocals, no lyrics.", "leave room for a narrator", "lots of space so dialogue and narration sit on top"]


def etiquetas(txt):
    t = txt.lower()
    for frase in PLANTILLA:
        t = t.replace(frase, " ")
    t = " " + NEGADO.sub(" ", t) + " "
    sal = {}
    for grupo, mapa in (("instrumentos", INSTRUMENTOS), ("animo", ANIMO), ("genero", GENERO)):
        sal[grupo] = sorted(k for k, pals in mapa.items() if any(p in t for p in pals))
    return sal


# ── lo que dice el video de origen ──────────────────────────────────────────────────────────────────────────────
def _literal(nodo):
    try:
        return ast.literal_eval(nodo)
    except Exception:
        return None


def leer_guion(carpeta):
    """LYRIA, ESTILO_VISUAL, TITULO y MOTOR de guion.py sin importarlo (ast): los guiones importan cosas del video."""
    r = {}
    p = os.path.join(carpeta, "guion.py")
    if not os.path.exists(p):
        return r
    try:
        arbol = ast.parse(open(p, encoding="utf-8").read())
    except Exception:
        return r
    for n in arbol.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            nombre = n.targets[0].id
            if nombre in ("TITULO", "ESTILO_VISUAL", "MOTOR"):
                r[nombre] = _literal(n.value)
            elif nombre == "LYRIA":
                v = n.value
                if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "dict":
                    r["LYRIA"] = {kw.arg: _literal(kw.value) for kw in v.keywords}
                else:
                    r["LYRIA"] = _literal(v)
    return r


CANALES = os.path.join(RAIZ, "canales")


def _alias_canales():
    return {os.path.splitext(f)[0] for f in os.listdir(CANALES) if f.endswith(".json")} if os.path.isdir(CANALES) else set()


def leer_canal(carpeta):
    """Alias del canal del video: el que nombre la línea «- canal:» del ESTADO.md (entre backticks o suelto, aunque vaya tras
    el nombre bonito: «Bitácora Perdida (`bitacora_perdida`)») o, si no, el canal cuyo `publicados` lo registra."""
    alias = _alias_canales()
    p = os.path.join(carpeta, "ESTADO.md")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8", errors="ignore").read().splitlines()[:10]:
            if not re.match(r"-\s*canal:", ln.strip(), re.I):
                continue
            for a in re.findall(r"`([a-z_0-9]+)`", ln) + re.findall(r"[a-z_0-9]+", ln.lower()):
                if a in alias:
                    return a
            m = re.match(r"-\s*canal:\s*`?([a-z_0-9]+)", ln.strip())
            if m:
                return m.group(1)
    v = os.path.basename(os.path.normpath(carpeta))
    for a in sorted(alias):
        try:
            pub = json.load(open(os.path.join(CANALES, a + ".json"), encoding="utf-8")).get("publicados", [])
        except (ValueError, OSError):
            continue
        if any(x.get("video") == v for x in pub):
            return a
    return ""


SECC = re.compile(r"\[(\d+):(\d+)\s*-\s*(\d+):(\d+)\]\s*[^:]*:\s*Intensity\s*(\d+)/10\.\s*(.*)")


def secciones(prompt):
    out = []
    for ln in prompt.splitlines():
        m = SECC.match(ln.strip())
        if m:
            a, b, c, d, i, desc = m.groups()
            out.append(dict(t0=int(a) * 60 + int(b), t1=int(c) * 60 + int(d), intensidad=int(i), desc=desc.strip()))
    return out


def prompt_de(carpeta_audio, archivo, guion):
    """Prompt exacto (audio/prompt_tramoN.txt) o, si no hay, el que arma lyria.py con LYRIA de guion.py."""
    m = re.search(r"tramo(\d+)", archivo)
    if m:
        p = os.path.join(carpeta_audio, f"prompt_tramo{m.group(1)}.txt")
        if os.path.exists(p):
            return open(p, encoding="utf-8", errors="ignore").read().strip(), int(m.group(1))
    ly = guion.get("LYRIA") or {}
    if not isinstance(ly, dict):
        return "", int(m.group(1)) if m else None
    partes = [ly.get("estilo") or ""]
    tr = ly.get("tramos") or []
    if m and tr and int(m.group(1)) <= len(tr) and isinstance(tr[int(m.group(1)) - 1], (list, tuple)):
        ids, nota = tr[int(m.group(1)) - 1][0], tr[int(m.group(1)) - 1][1]
        partes.append(nota)
        esc = ly.get("escenas") or {}
        partes += [f"{i}: {esc[i][0]}" for i in ids if i in esc and isinstance(esc[i], (list, tuple))]
    else:
        for i, v in (ly.get("escenas") or {}).items():
            if isinstance(v, (list, tuple)) and v:
                partes.append(f"{i}: {v[0]}")
    return "\n".join(p for p in partes if p), int(m.group(1)) if m else None


def escenas_de(guion, tramo):
    ly = guion.get("LYRIA") or {}
    tr = ly.get("tramos") if isinstance(ly, dict) else None
    if tramo and tr and tramo <= len(tr) and isinstance(tr[tramo - 1], (list, tuple)):
        return list(tr[tramo - 1][0])
    return []


# ── medidas del audio ───────────────────────────────────────────────────────────────────────────────────────────
def medir(ruta):
    import librosa
    import numpy as np
    y, sr = librosa.load(ruta, sr=22050, mono=True)
    dur = len(y) / sr
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    db = 20 * np.log10(rms + 1e-6)
    t = np.arange(len(rms)) * 512 / sr
    nb = 12
    energia = [float(np.mean(rms[int(len(rms) * k / nb):max(int(len(rms) * (k + 1) / nb), int(len(rms) * k / nb) + 1)])) for k in range(nb)]
    mx = max(energia) or 1.0
    energia = [round(e / mx, 2) for e in energia]
    huecos, ini = [], None
    for ti, d in zip(t, db):                                   # silencios internos > 1,5 s (Lyria a veces deja huecos)
        if d < -50:
            ini = ti if ini is None else ini
        else:
            if ini is not None and ti - ini > 1.5 and ini > 1.0 and ti < dur - 1.0:
                huecos.append([round(ini, 1), round(ti, 1)])
            ini = None
    try:
        tempo = float(np.atleast_1d(librosa.beat.beat_track(y=y, sr=sr)[0])[0])
    except Exception:
        tempo = 0.0
    cent = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    return dict(dur=round(dur, 2), rms_db=round(float(20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-9)), 1),
                tempo=round(tempo, 1), brillo_hz=int(cent), energia=energia, huecos=huecos,
                dinamica=round(max(energia) - min(energia), 2))


def _md5(ruta):
    h = hashlib.md5()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ── catalogar ───────────────────────────────────────────────────────────────────────────────────────────────────
def fuentes():
    """[(video, carpeta_video, ruta_audio, archivo)] de toda la música de Lyria en disco."""
    out = []
    for v in sorted(os.listdir(VIDEOS)):
        cv = os.path.join(VIDEOS, v)
        ca = os.path.join(cv, "audio")
        if v.startswith(("_", ".")) or not os.path.isdir(ca):
            continue
        for f in sorted(os.listdir(ca)):
            if "lyria" in f.lower() and f.lower().endswith(EXT) and "sin_silencio" not in f and not f.startswith("_t"):
                out.append((v, cv, os.path.join(ca, f), f))
    for raiz in EXTRA:                                         # sistema viejo: <canal>/<video>/music/*.mp3
        if not os.path.isdir(raiz):
            continue
        for canal in sorted(os.listdir(raiz)):
            pc = os.path.join(raiz, canal)
            if not os.path.isdir(pc):
                continue
            for v in sorted(os.listdir(pc)):
                pm = os.path.join(pc, v, "music")
                if os.path.isdir(pm):
                    for f in sorted(os.listdir(pm)):
                        if f.lower().endswith(EXT):
                            out.append((f"{canal}_{v}", os.path.join(pc, v), os.path.join(pm, f), f))
    return out


def _slug(s):
    return re.sub(r"[^a-z0-9_]+", "_", s.lower()).strip("_")


def _ficha(arg):
    video, cv, ruta, archivo = arg
    try:
        guion = leer_guion(cv)
        prompt, tramo = prompt_de(os.path.dirname(ruta), archivo, guion)
        if not prompt:                                         # sistema viejo: el prompt suele estar junto a la pieza
            base = os.path.splitext(ruta)[0]
            for cand in (base + ".txt", base + ".prompt.txt"):
                if os.path.exists(cand):
                    prompt = open(cand, encoding="utf-8", errors="ignore").read().strip()
        ly = guion.get("LYRIA") if isinstance(guion.get("LYRIA"), dict) else {}
        estilo = (ly or {}).get("estilo") or ""
        idp = f"{_slug(video)}__{_slug(os.path.splitext(archivo)[0])}"
        destino = os.path.join(BIB, idp + ".mp3")
        if not os.path.exists(destino):
            if ruta.lower().endswith(".mp3"):
                shutil.copy2(ruta, destino)
            else:
                subprocess.run([FFMPEG, "-v", "error", "-y", "-i", ruta, "-c:a", "libmp3lame", "-b:a", "320k", destino], check=True)
        med = medir(destino)
        canal = leer_canal(cv)
        texto = " ".join([estilo, prompt, video, archivo])
        et = etiquetas(texto)
        sec = secciones(prompt)
        var = bool(re.search(r"(^_|_b\.|corto|prueba|test|con_silencio|_orig|largo)", archivo))
        return dict(id=idp, video=video, archivo_origen=ruta, archivo=os.path.basename(destino), md5=_md5(ruta), canal=canal,
                    estilo_video=guion.get("ESTILO_VISUAL") or "", titulo_video=guion.get("TITULO") or "", tramo=tramo,
                    escenas=escenas_de(guion, tramo), estilo=estilo, prompt=prompt, secciones=sec,
                    intensidad=[s["intensidad"] for s in sec], etiquetas=et, medidas=med, variante=var, usos=[],
                    catalogado=time.strftime("%Y-%m-%d"))
    except Exception as e:                                     # una pieza rota no frena el catálogo
        return dict(error=f"{ruta}: {e}")


def cargar(ruta):
    if os.path.exists(ruta):
        return json.load(open(ruta, encoding="utf-8"))
    return {"piezas": {}}


def guardar(ruta, d):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    tmp = ruta + ".tmp"
    json.dump(d, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, ruta)


def catalogar(procs=8):
    os.makedirs(BIB, exist_ok=True)
    d = cargar(JSON_M)
    vistos = {p["archivo_origen"] for p in d["piezas"].values()}
    hashes = {p["md5"]: k for k, p in d["piezas"].items()}
    nuevas = [f for f in fuentes() if f[2] not in vistos]
    print(f"{len(nuevas)} piezas nuevas por catalogar ({len(d['piezas'])} ya en la biblioteca)", flush=True)
    with Pool(procs) as pool:
        for i, r in enumerate(pool.imap_unordered(_ficha, nuevas), 1):
            if "error" in r:
                print("  ERROR", r["error"], flush=True)
                continue
            if r["md5"] in hashes and hashes[r["md5"]] != r["id"]:      # la misma pieza copiada a otro video: un solo registro
                orig = d["piezas"][hashes[r["md5"]]]
                orig.setdefault("copias", []).append(r["archivo_origen"])
                try:
                    os.remove(os.path.join(BIB, r["archivo"]))
                except OSError:
                    pass
                continue
            d["piezas"][r["id"]] = r
            hashes[r["md5"]] = r["id"]
            if i % 20 == 0:
                guardar(JSON_M, d)
                print(f"  {i}/{len(nuevas)}", flush=True)
    d["actualizado"] = time.strftime("%Y-%m-%d %H:%M")
    guardar(JSON_M, d)
    escribir_catalogo(d)
    tot = sum(p["medidas"]["dur"] for p in d["piezas"].values())
    print(f"Biblioteca: {len(d['piezas'])} piezas, {tot / 60:.0f} min de música → {JSON_M} y {CATALOGO}")


def escribir_catalogo(d):
    P = sorted(d["piezas"].values(), key=lambda p: (p["video"], p["archivo"]))
    por = {}
    for p in P:
        for a in (p["etiquetas"]["animo"] or ["(sin ánimo)"]):
            por.setdefault(a, []).append(p)
    L = ["# Catálogo de la biblioteca de música (generado por `python nucleo/musica_biblioteca.py catalogar`; NO editar a mano)", "",
         f"{len(P)} piezas · {sum(p['medidas']['dur'] for p in P) / 60:.0f} min · actualizado {d.get('actualizado', '')}. "
         "Cómo buscar y reutilizar: `docs/musica_biblioteca.md`. Audio en `E:\\FabricaAnimaciones\\musica_biblioteca\\<id>.mp3`.", ""]
    L += ["## Por video", "", "| id | dur | canal | tramo · escenas | instrumentos | ánimo | género | curva |", "|---|---|---|---|---|---|---|---|"]
    barras = "▁▂▃▄▅▆▇█"
    for p in P:
        curva = "".join(barras[min(7, int(e * 7.99))] for e in p["medidas"]["energia"])
        esc = ", ".join(p["escenas"][:5]) + ("…" if len(p["escenas"]) > 5 else "")
        L.append(f"| `{p['id']}`{' (var.)' if p['variante'] else ''} | {p['medidas']['dur']:.0f} s | {p['canal'] or '—'} | "
                 f"{p['tramo'] or '—'} · {esc or '—'} | {', '.join(p['etiquetas']['instrumentos'][:5])} | "
                 f"{', '.join(p['etiquetas']['animo'][:5])} | {', '.join(p['etiquetas']['genero'][:3])} | {curva} |")
    L += ["", "## Por ánimo (para buscar rápido)", ""]
    for a in sorted(por):
        L.append(f"- **{a}** ({len(por[a])}): " + ", ".join(f"`{p['id']}`" for p in por[a]))
    open(CATALOGO, "w", encoding="utf-8").write("\n".join(L) + "\n")


# ── buscar / ver / sugerir / usar ───────────────────────────────────────────────────────────────────────────────
def _texto(p):
    e = p["etiquetas"]
    return " ".join([p["prompt"], p["estilo"], p["video"], p["canal"], p["estilo_video"], " ".join(p["escenas"]),
                     " ".join(e["instrumentos"] + e["animo"] + e["genero"])])


def _idf(P):
    df = Counter()
    docs = {}
    for k, p in P.items():
        toks = set(_pal(_texto(p)))
        docs[k] = Counter(_pal(_texto(p)))
        df.update(toks)
    n = len(P)
    return {w: math.log((n + 1) / (c + 0.5)) for w, c in df.items()}, docs


def _cos(q, d, idf):
    num = sum(q[w] * d.get(w, 0) * idf.get(w, 0) ** 2 for w in q)
    nq = math.sqrt(sum((q[w] * idf.get(w, 0)) ** 2 for w in q)) or 1
    nd = math.sqrt(sum((c * idf.get(w, 0)) ** 2 for w, c in d.items())) or 1
    return num / (nq * nd)


# sinónimos español → inglés del prompt (se busca en los dos idiomas)
ES_EN = {"tierno": "tender gentle", "triste": "sad melancholic", "cuna": "lullaby cradle", "cajita": "music box", "guitarra": "guitar",
         "cuerdas": "strings", "esperanza": "hopeful", "miedo": "horror dread", "terror": "horror eerie", "oscuro": "dark ominous",
         "misterio": "mystery", "épico": "epic heroic", "epico": "epic heroic", "fiesta": "festive celebration", "feria": "fair waltz",
         "vals": "waltz", "banda": "brass band", "calma": "calm peaceful", "tenso": "tense suspense", "juguetón": "playful whimsical",
         "jugueton": "playful whimsical", "medieval": "medieval fantasy", "coro": "choir", "tambores": "drums", "llanto": "emotional crying",
         "emotivo": "emotional swell", "noche": "night", "amanecer": "dawn", "niño": "child childhood", "infancia": "childhood",
         "nostalgia": "nostalgic", "mexicano": "mexican", "silbido": "whistle"}


ES_EN_SFX = {"roto": "broken shatter smash", "rompe": "shatter smash break", "plato": "plate ceramic dish", "vidrio": "glass shatter",
             "freno": "brake brakes screech", "frenon": "brakes screech skid", "troca": "pickup truck engine", "carro": "car engine",
             "puerta": "door", "portazo": "door slam", "reja": "gate metal", "grito": "scream shout yell", "gritos": "shouting yelling",
             "golpe": "punch hit impact thud", "pared": "wall", "puñetazo": "punch fist wall", "lluvia": "rain", "grillos": "crickets night",
             "gallo": "rooster", "pajaros": "birds birdsong", "pájaros": "birds birdsong", "feria": "fair carnival crowd", "multitud": "crowd",
             "gente": "crowd people murmur", "aplausos": "applause clapping", "llanto": "crying sobbing", "risa": "laugh laughing",
             "risas": "laughing laughter", "pasos": "footsteps steps", "viento": "wind", "celular": "phone smartphone", "vibra": "vibrate buzz",
             "notificacion": "notification message", "notificación": "notification message", "mensaje": "message notification",
             "radio": "radio static", "rueda": "wheel creak", "rechinido": "creak squeak", "perro": "dog bark", "ladrido": "dog bark",
             "moto": "motorcycle", "combi": "minibus van", "cocina": "kitchen", "silla": "chair", "mesa": "table", "llaves": "keys",
             "beso": "kiss", "abrazo": "hug", "corazon": "heartbeat", "latido": "heartbeat", "trueno": "thunder", "fuego": "fire crackle",
             "agua": "water", "olas": "waves sea", "campana": "bell", "campanas": "bells church", "banda": "brass band", "musica": "music"}


def buscar(palabras, dmin=0, dmax=1e9, canal=None, n=12, excluir=(), mostrar=True, d=None):
    d = d or cargar(JSON_M)
    P = {k: p for k, p in d["piezas"].items() if dmin <= p["medidas"]["dur"] <= dmax and (not canal or p["canal"] == canal)
         and p["video"] not in excluir}
    if not P:
        return []
    idf, docs = _idf(d["piezas"])
    q = Counter()
    for w in palabras:
        q.update(_pal(w))
        q.update(_pal(ES_EN.get(w.lower(), "")))
    res = sorted(((round(_cos(q, docs[k], idf), 3), k) for k in P), reverse=True)[:n]
    if mostrar:
        for s, k in res:
            p = P[k]
            print(f"{s:5.3f}  {k:<52} {p['medidas']['dur']:6.1f} s  {p['canal'] or '—':<18} "
                  f"{'/'.join(p['etiquetas']['animo'][:4])} · {'/'.join(p['etiquetas']['instrumentos'][:4])}")
    return res


def ver(idp):
    d = cargar(JSON_M)
    p = d["piezas"].get(idp)
    if not p:
        sys.exit(f"No existe {idp}. Prueba `buscar`.")
    barras = "▁▂▃▄▅▆▇█"
    m = p["medidas"]
    print(f"{p['id']}  ({p['medidas']['dur']} s · {m['tempo']} bpm · {m['rms_db']} dB · brillo {m['brillo_hz']} Hz)")
    print(f"video {p['video']} · canal {p['canal'] or '—'} · estilo {p['estilo_video'] or '—'} · tramo {p['tramo']} · escenas {p['escenas']}")
    print("curva  ", "".join(barras[min(7, int(e * 7.99))] for e in m["energia"]), " huecos", m["huecos"] or "—")
    print("etiquetas", json.dumps(p["etiquetas"], ensure_ascii=False))
    print("audio  ", os.path.join(BIB, p["archivo"]))
    print("usos   ", p.get("usos") or "—")
    print("\nPROMPT:\n" + (p["prompt"] or "(sin prompt guardado)"))


def _tl(video):
    return json.load(open(os.path.join(VIDEOS, video, "timeline.json"), encoding="utf-8"))


def tramos_video(video):
    """[(n, ids, nota, t0, t1, texto)] de los tramos de LYRIA del video (con sus tiempos reales del timeline)."""
    g = leer_guion(os.path.join(VIDEOS, video))
    ly = g.get("LYRIA") or {}
    tl = _tl(video)
    esc = {e["id"]: e for e in tl["escenas"]}
    tr = ly.get("tramos") or [([e["id"] for e in tl["escenas"]], "")]
    out = []
    for n, (ids, nota) in enumerate(tr, 1):
        t0, t1 = esc[ids[0]]["t0"], esc[ids[-1]]["t1"]
        texto = " ".join([ly.get("estilo") or "", nota] + [str((ly.get("escenas") or {}).get(i, ("",))[0]) for i in ids])
        inten = [(ly.get("escenas") or {}).get(i, ("", 4))[1] for i in ids]
        out.append((n, ids, nota, t0, t1, texto, inten))
    return out


def _curva_tramo(video, ids, inten):
    """Intensidad pedida (1-10) del tramo en 12 puntos, ponderada por la duración real de cada escena."""
    esc = {e["id"]: e for e in _tl(video)["escenas"]}
    t0, t1 = esc[ids[0]]["t0"], esc[ids[-1]]["t1"]
    out = []
    for b in range(12):
        t = t0 + (b + 0.5) * (t1 - t0) / 12
        i = next((k for k, s in enumerate(ids) if esc[s]["t0"] <= t < esc[s]["t1"]), len(ids) - 1)
        out.append(inten[i])
    return out


def _parecido_intensidad(pedida, p):
    """Bono/castigo por cómo casa la curva de la pieza con la intensidad pedida: forma (correlación) y nivel medio."""
    e = p["medidas"]["energia"]
    m = sum(pedida) / len(pedida)
    sa = math.sqrt(sum((x - m) ** 2 for x in pedida)) or 1e-9
    me = sum(e) / len(e)
    sb = math.sqrt(sum((x - me) ** 2 for x in e)) or 1e-9
    corr = sum((x - m) * (y - me) for x, y in zip(pedida, e)) / (sa * sb) if sa > 1e-6 and sb > 1e-6 else 0.0
    nivel_p = (sum(p["intensidad"]) / len(p["intensidad"])) if p["intensidad"] else None
    castigo = 0.03 * abs(nivel_p - m) if nivel_p is not None else 0.0      # 5 puntos de diferencia = −0,15
    return 0.12 * corr - castigo


def sugerir(video, excluir=(), n=5):
    d = cargar(JSON_M)
    excl = set(excluir) | {video}
    for k, ids, nota, t0, t1, texto, inten in tramos_video(video):
        need = (t1 - t0) + 3.0
        pedida = _curva_tramo(video, ids, inten)
        print(f"\n== tramo {k}: {', '.join(ids)}  ({t0:.1f}-{t1:.1f} s → pieza de ~{need:.0f} s)  intensidad {inten}")
        res = buscar([texto], excluir=excl, n=60, mostrar=False, d=d)
        mejores = []
        for s, idp in res:
            p = d["piezas"][idp]
            dur = p["medidas"]["dur"]
            ajuste = 0.15 if 0.88 * need <= dur <= 1.12 * need else (0.07 if dur > need else -0.10 * min(1.0, (need - dur) / need))
            pen = -0.1 if p["medidas"]["huecos"] else 0.0
            pen += -0.05 if p["variante"] else 0.0
            mejores.append((round(s + ajuste + pen + _parecido_intensidad(pedida, p), 3), idp, dur))
        barras = "▁▂▃▄▅▆▇█"
        print("  pedida  " + "".join(barras[min(7, int(x / 10 * 7.99))] for x in pedida))
        for s, idp, dur in sorted(mejores, reverse=True)[:n]:
            p = d["piezas"][idp]
            curva = "".join(barras[min(7, int(x * 7.99))] for x in p["medidas"]["energia"])
            print(f"  {s:5.3f}  {curva}  {idp:<48} {dur:6.1f} s  int {p['intensidad'] or '—'}  "
                  f"{'/'.join(p['etiquetas']['animo'][:4])} · {'/'.join(p['etiquetas']['instrumentos'][:3])}")
        print(f"  → python fab.py biblioteca usar <id> {video} {k} [--desde s]   (ver la pieza: biblioteca ver <id>)")


def usar(idp, video, tramo, desde=0.0):
    import numpy as np
    import soundfile as sf
    d = cargar(JSON_M)
    p = d["piezas"].get(idp)
    if not p:
        sys.exit(f"No existe {idp}")
    tr = {t[0]: t for t in tramos_video(video)}[int(tramo)]
    need = (tr[4] - tr[3]) + 3.0
    src = os.path.join(BIB, p["archivo"])
    tmp = os.path.join(VIDEOS, video, "audio", "_bib.wav")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(desde), "-i", src, "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", tmp],
                   check=True)
    x, sr = sf.read(tmp, always_2d=True)
    os.remove(tmp)
    cr = int(3.0 * sr)
    if len(x) < need * sr / 1.12:                              # corta: bucle con cruce de 3 s hasta cubrir el tramo
        y = x.copy()
        while len(y) < need * sr:
            a = y[-cr:] * np.cos(np.linspace(0, np.pi / 2, cr))[:, None] + x[:cr] * np.sin(np.linspace(0, np.pi / 2, cr))[:, None]
            y = np.vstack([y[:-cr], a, x[cr:]])
        x = y
    if len(x) > need * sr * 1.12:                              # larga: se recorta con fundido de 2,5 s (armar ajusta el resto)
        n = int(need * sr)
        x = x[:n].copy()
        f = int(2.5 * sr)
        x[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
    dest_wav = os.path.join(VIDEOS, video, "audio", f"_bib_tramo{tramo}.wav")
    sf.write(dest_wav, x.astype(np.float32), sr, subtype="FLOAT")
    for viejo in os.listdir(os.path.join(VIDEOS, video, "audio")):
        if re.fullmatch(rf"lyria_tramo{tramo}\.(mp3|wav|m4a|ogg)", viejo):
            os.replace(os.path.join(VIDEOS, video, "audio", viejo), os.path.join(VIDEOS, video, "audio", "_antes_" + viejo))
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", dest_wav, "-c:a", "libmp3lame", "-b:a", "320k",
                    os.path.join(VIDEOS, video, "audio", f"lyria_tramo{tramo}.mp3")], check=True)
    os.remove(dest_wav)
    open(os.path.join(VIDEOS, video, "audio", f"prompt_tramo{tramo}.txt"), "w", encoding="utf-8").write(
        f"BIBLIOTECA: {idp} (desde {desde} s) — reutilizada el {time.strftime('%Y-%m-%d')}\n\n{p['prompt']}")
    p.setdefault("usos", []).append(dict(video=video, tramo=int(tramo), desde=desde, fecha=time.strftime("%Y-%m-%d")))
    guardar(JSON_M, d)
    print(f"audio/lyria_tramo{tramo}.mp3 ← {idp} ({len(x) / sr:.1f} s para un tramo de {need:.1f} s). "
          f"Siguiente: python ../../nucleo/lyria_tramos.py armar (desde videos/{video})")


# ── SFX ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def _sfx_prompts(cv):
    """{nombre: prompt} de los dicts SFX de fx_audio.py / efectos.py / escenas.py del video y de SFX_ELEVEN en guion.py
    (ast, sin importarlos)."""
    out = {}
    g = os.path.join(cv, "guion.py")
    if os.path.exists(g):
        try:
            for n in ast.parse(open(g, encoding="utf-8").read()).body:
                if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "SFX_ELEVEN" for t in n.targets):
                    for k, v in (_literal(n.value) or {}).items():
                        out[k] = v.get("prompt", "") if isinstance(v, dict) else (v[0] if isinstance(v, (tuple, list)) else v)
        except Exception:
            pass
    for f in ("fx_audio.py", "efectos.py", "_fx.py"):
        p = os.path.join(cv, f)
        if not os.path.exists(p):
            continue
        try:
            arbol = ast.parse(open(p, encoding="utf-8").read())
        except Exception:
            continue
        for n in ast.walk(arbol):
            if isinstance(n, ast.Dict):
                for k, v in zip(n.keys, n.values):
                    kk = _literal(k) if k is not None else None
                    vv = _literal(v)
                    if isinstance(kk, str):
                        if isinstance(vv, (tuple, list)) and vv and isinstance(vv[0], str) and len(vv[0]) > 15:
                            out[kk] = vv[0]
                        elif isinstance(vv, dict) and isinstance(vv.get("prompt"), str):
                            out[kk] = vv["prompt"]
                        elif isinstance(vv, str) and len(vv) > 25 and " " in vv:
                            out.setdefault(kk, vv)
    return out


def sfx_catalogar():
    os.makedirs(BIB_SFX, exist_ok=True)
    d = cargar(JSON_S)
    hashes = {p["md5"]: k for k, p in d["piezas"].items()}
    nuevos = 0
    for v in sorted(os.listdir(VIDEOS)):
        cv = os.path.join(VIDEOS, v)
        cs = os.path.join(cv, "sfx")
        if v.startswith(("_", ".")) or not os.path.isdir(cs):
            continue
        prompts = _sfx_prompts(cv)
        for f in sorted(os.listdir(cs)):
            if not f.lower().endswith(EXT):
                continue
            ruta = os.path.join(cs, f)
            h = _md5(ruta)
            if h in hashes:
                continue
            nombre = os.path.splitext(f)[0]
            if nombre not in prompts and re.sub(r"_\d+$", "", nombre) in prompts:     # variantes de SFX_ELEVEN: pop_2 → pop
                prompts[nombre] = prompts[re.sub(r"_\d+$", "", nombre)]
            idp = f"{_slug(v)}__{_slug(nombre)}"
            shutil.copy2(ruta, os.path.join(BIB_SFX, idp + os.path.splitext(f)[1].lower()))
            try:
                import soundfile as sf
                dur = round(sf.info(ruta).duration, 2)
            except Exception:
                dur = None
            d["piezas"][idp] = dict(id=idp, video=v, nombre=nombre, archivo=idp + os.path.splitext(f)[1].lower(), md5=h,
                                    prompt=prompts.get(nombre, ""), dur=dur, canal=leer_canal(cv))
            hashes[h] = idp
            nuevos += 1
    for p in d["piezas"].values():                     # canal mal leído antes del 22-oct-2026 («Bitácora Perdida (`…`)» → '')
        cv = os.path.join(VIDEOS, p["video"])
        if p.get("canal") in ("", "sin", "ninguno", None) and os.path.isdir(cv):
            p["canal"] = leer_canal(cv)
    d["actualizado"] = time.strftime("%Y-%m-%d %H:%M")
    guardar(JSON_S, d)
    print(f"SFX: {nuevos} nuevos · {len(d['piezas'])} en total → {JSON_S} (audio en {BIB_SFX})")


def _sfx_quemada(p, canal, video=None):
    """True si el público de `canal` ya oyó la pieza: nació en ese canal o ya se usó en él (o es del mismo video)."""
    if video and (p["video"] == video or any(u.get("video") == video for u in p.get("usos", []))):
        return True
    return bool(canal) and (p.get("canal") == canal or any(u.get("canal") == canal for u in p.get("usos", [])))


def sfx_buscar(palabras, n=10, canal=None, video=None, salida=True, dur=None):
    """TF-IDF sobre nombre+prompt. Con `canal`, descarta lo que ese público ya oyó (regla 22-oct-2026: no repetir SFX en el
    mismo canal). Con `dur`, descarta piezas de largo muy distinto (< 0,4× o > 4× + 1 s)."""
    d = cargar(JSON_S)
    P = {k: p for k, p in d["piezas"].items() if not _sfx_quemada(p, canal, video)
         and (not dur or not p.get("dur") or 0.4 * dur <= p["dur"] <= 4 * dur + 1)}
    if not P:
        return []
    df = Counter()
    docs = {}
    for k, p in P.items():
        toks = _pal(" ".join([p["nombre"].replace("_", " "), p["prompt"], p["video"]]))
        docs[k] = Counter(toks)
        df.update(set(toks))
    idf = {w: math.log((len(P) + 1) / (c + 0.5)) for w, c in df.items()}
    q = Counter()
    for w in palabras:
        for x in _pal(w):
            q.update([x])
            q.update(_pal(ES_EN_SFX.get(x, "") or ES_EN.get(x, "")))
    res = sorted(((round(_cos(q, docs[k], idf), 3), k) for k in P), reverse=True)[:n]
    if salida:
        for s, k in res:
            p = P[k]
            print(f"{s:5.3f}  {k:<40} {p['dur'] or 0:5.1f} s  {(p.get('canal') or '-'):<18} {p['prompt'][:80]}")
    return res


def sfx_usar(idp, video, nombre=None):
    """Copia la pieza a videos/<v>/sfx/<nombre>.<ext> y anota el uso con el canal del video (para no repetirla ante él)."""
    d = cargar(JSON_S)
    p = d["piezas"].get(idp)
    if not p:
        sys.exit(f"No existe {idp}")
    dest = os.path.join(VIDEOS, video, "sfx")
    os.makedirs(dest, exist_ok=True)
    final = os.path.join(dest, (nombre or p["nombre"]) + os.path.splitext(p["archivo"])[1])
    shutil.copy2(os.path.join(BIB_SFX, p["archivo"]), final)
    p.setdefault("usos", []).append(dict(video=video, canal=leer_canal(os.path.join(VIDEOS, video)),
                                         nombre=nombre or p["nombre"], fecha=time.strftime("%Y-%m-%d")))
    guardar(JSON_S, d)
    print(f"{final} ← {idp}  («{p['prompt'][:80]}»)")
    return final


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("orden")
    ap.add_argument("resto", nargs="*")
    ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--min", type=float, default=0)
    ap.add_argument("--max", type=float, default=1e9)
    ap.add_argument("--canal")
    ap.add_argument("-n", type=int, default=12)
    ap.add_argument("--excluir", nargs="*", default=[])
    ap.add_argument("--desde", type=float, default=0.0)
    ap.add_argument("--nombre")
    a = ap.parse_args()
    if a.orden == "catalogar":
        catalogar(a.procs)
    elif a.orden == "reetiquetar":                      # tras cambiar las tablas de etiquetas: sin volver a copiar ni medir
        d = cargar(JSON_M)
        for p in d["piezas"].values():
            p["etiquetas"] = etiquetas(" ".join([p["estilo"], p["prompt"], p["video"], os.path.basename(p["archivo_origen"])]))
        guardar(JSON_M, d)
        escribir_catalogo(d)
        print(f"{len(d['piezas'])} piezas re-etiquetadas → {CATALOGO}")
    elif a.orden == "buscar":
        buscar(a.resto, a.min, a.max, a.canal, a.n, a.excluir)
    elif a.orden == "ver":
        ver(a.resto[0])
    elif a.orden == "sugerir":
        sugerir(a.resto[0], a.excluir, min(a.n, 8) if a.n != 12 else 5)
    elif a.orden == "usar":
        usar(a.resto[0], a.resto[1], a.resto[2], a.desde)
    elif a.orden == "sfx":
        sub = a.resto[0] if a.resto else "buscar"
        if sub == "catalogar":
            sfx_catalogar()
        elif sub == "buscar":
            sfx_buscar(a.resto[1:], a.n, a.canal)
        elif sub == "usar":
            sfx_usar(a.resto[1], a.resto[2], a.nombre)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
