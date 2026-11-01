# -*- coding: utf-8 -*-
"""APK de la app «Fábrica» (28-oct-2026) sin Gradle: aapt2 + javac + d8 + zipalign + apksigner del Android SDK de la PC.

    python nucleo/app_movil/android/construir_apk.py [--nota "qué cambió"]... [--sin-subir]

Deja nucleo/app_movil/fabrica.apk (se descarga desde el panel móvil: «📲 App» → /v2/app/fabrica.apk) y los iconos de la
app web (icono-192.png, icono-512.png). Anota la versión en version.json (la app instalada más vieja ofrece «Descargar la
app nueva» al entrar: actualiza.js) y la sube al dominio (clicknbusiness.com.mx/panel/fabrica.apk, sin clave) con la puerta. La llave de firma (fabrica.keystore, fuera de git) se crea la primera vez y se
reutiliza: con otra llave Android no deja actualizar encima y habría que desinstalar.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(AQUI)
SALIDA = os.path.join(APP, "fabrica.apk")
LLAVE = os.path.join(AQUI, "fabrica.keystore")
CLAVE_LLAVE = "fabrica-app"            # solo protege la llave local de firma (sideload), no da acceso a nada
SDK = os.environ.get("ANDROID_HOME") or os.path.join(os.environ["LOCALAPPDATA"], "Android", "Sdk")


def ultimo(patron):
    xs = sorted(glob.glob(patron), key=lambda p: [int(x) if x.isdigit() else x for x in os.path.basename(p).replace("android-", "").split(".")])
    if not xs:
        sys.exit(f"No encontré {patron}")
    return xs[-1]


def correr(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"Falló: {' '.join(map(str, cmd))}\n{r.stdout}\n{r.stderr}")
    return r


def icono(lado):
    """Cuadro redondeado con degradado violeta→rosa y una fábrica blanca (chimeneas + dientes de sierra + pantalla ▶)."""
    k = 4                                                   # sobremuestreo para bordes suaves
    n = lado * k
    fondo = Image.new("RGB", (n, n))
    px = fondo.load()
    a, b = (122, 98, 255), (255, 95, 168)
    for y in range(n):
        for x in range(0, n):
            t = (x + y) / (2 * n)
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    mascara = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * .23), fill=255)
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    im.paste(fondo, (0, 0), mascara)
    d = ImageDraw.Draw(im)
    u = n / 100
    blanco = (255, 255, 255, 255)
    d.rectangle([22 * u, 22 * u, 31 * u, 52 * u], fill=blanco)                     # chimeneas
    d.rectangle([36 * u, 30 * u, 44 * u, 52 * u], fill=blanco)
    d.polygon([(18 * u, 78 * u), (18 * u, 50 * u), (38 * u, 40 * u), (38 * u, 50 * u), (58 * u, 40 * u), (58 * u, 50 * u),
               (82 * u, 38 * u), (82 * u, 78 * u)], fill=blanco)                   # nave con techo de sierra
    d.rounded_rectangle([42 * u, 55 * u, 74 * u, 72 * u], radius=3 * u, fill=(122, 98, 255, 255))   # pantalla
    d.polygon([(54 * u, 58.5 * u), (54 * u, 68.5 * u), (63 * u, 63.5 * u)], fill=blanco)            # ▶
    for i, x in enumerate((24, 31)):
        d.ellipse([(x - 3) * u, (14 - i * 3) * u, (x + 5) * u, (20 - i * 3) * u], fill=(255, 255, 255, 150))   # humo
    return im.resize((lado, lado), Image.LANCZOS)


def anota_version(codigo, nombre, notas):
    ruta = os.path.join(APP, "version.json")
    v = json.load(open(ruta, encoding="utf-8"))
    v["apk"].update(codigo=codigo, nombre=nombre, notas=notas or v["apk"].get("notas") or [])
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=1)


def sube_al_dominio():
    sys.path.insert(0, os.path.dirname(APP))
    import panel_remoto as R
    c = R.leer_cfg()
    if not c.get("dominio") or not c.get("url"):
        print("Sin dominio o sin túnel: el APK queda solo en /v2/app/fabrica.apk")
        return
    if R.publicar_dominio(c, forzar=True):
        print(f"Subido: {c['dominio']['url'].rsplit('/', 2)[0]}/panel/fabrica.apk")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nota", action="append", help="novedad de esta versión (se muestra al actualizar)")
    ap.add_argument("--sin-subir", action="store_true")
    a = ap.parse_args()
    bt = ultimo(os.path.join(SDK, "build-tools", "*"))
    plataforma = ultimo(os.path.join(SDK, "platforms", "android-*"))
    android_jar = os.path.join(plataforma, "android.jar")
    aapt2, zipalign = os.path.join(bt, "aapt2.exe"), os.path.join(bt, "zipalign.exe")
    d8, apksigner = os.path.join(bt, "d8.bat"), os.path.join(bt, "apksigner.bat")
    tmp = tempfile.mkdtemp(prefix="fab_apk_")
    try:
        # iconos (app web y lanzador de Android)
        icono(192).save(os.path.join(APP, "icono-192.png"))
        icono(512).save(os.path.join(APP, "icono-512.png"))
        res = os.path.join(tmp, "res")
        for carpeta, lado in (("mipmap-mdpi", 48), ("mipmap-hdpi", 72), ("mipmap-xhdpi", 96), ("mipmap-xxhdpi", 144), ("mipmap-xxxhdpi", 192)):
            os.makedirs(os.path.join(res, carpeta))
            icono(lado).save(os.path.join(res, carpeta, "ic_launcher.png"))
        # manifest con versión (cada build se instala encima de la anterior)
        codigo = int(time.time() // 60)                  # minutos desde 1970: siempre crece (el primero, 26102822, era fecha+hora)
        man = open(os.path.join(AQUI, "AndroidManifest.xml"), encoding="utf-8").read()
        man = man.replace("@VERSION_CODE@", str(codigo)).replace("@VERSION_NAME@", time.strftime("1.%Y%m%d.%H%M"))
        manifest = os.path.join(tmp, "AndroidManifest.xml")
        open(manifest, "w", encoding="utf-8").write(man)
        # recursos
        flat = os.path.join(tmp, "flat.zip")
        correr([aapt2, "compile", "--dir", res, "-o", flat])
        base = os.path.join(tmp, "base.apk")
        gen = os.path.join(tmp, "gen")
        correr([aapt2, "link", "-o", base, "-I", android_jar, "--manifest", manifest, "--java", gen, flat, "--auto-add-overlay"])
        # código
        clases = os.path.join(tmp, "clases")
        fuentes = [os.path.join(AQUI, "MainActivity.java")] + glob.glob(os.path.join(gen, "**", "*.java"), recursive=True)
        correr(["javac", "--release", "11", "-encoding", "UTF-8", "-classpath", android_jar, "-d", clases, *fuentes])
        dex = os.path.join(tmp, "dex")
        os.makedirs(dex)
        correr([d8, "--release", "--min-api", "24", "--lib", android_jar, "--output", dex,
                *glob.glob(os.path.join(clases, "**", "*.class"), recursive=True)], shell=False)
        with zipfile.ZipFile(base, "a", zipfile.ZIP_DEFLATED) as z:
            z.write(os.path.join(dex, "classes.dex"), "classes.dex")
        alineado = os.path.join(tmp, "alineado.apk")
        correr([zipalign, "-f", "-p", "4", base, alineado])
        # firma (llave local persistente)
        if not os.path.isfile(LLAVE):
            correr(["keytool", "-genkeypair", "-keystore", LLAVE, "-storepass", CLAVE_LLAVE, "-keypass", CLAVE_LLAVE,
                    "-alias", "fabrica", "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
                    "-dname", "CN=Fabrica de Animaciones, O=Click N Business, C=MX"])
        correr([apksigner, "sign", "--ks", LLAVE, "--ks-pass", f"pass:{CLAVE_LLAVE}", "--key-pass", f"pass:{CLAVE_LLAVE}",
                "--out", SALIDA, alineado])
        correr([apksigner, "verify", SALIDA])
        nombre = time.strftime("1.%Y%m%d.%H%M")
        anota_version(codigo, nombre, a.nota)
        print(f"APK listo: {SALIDA} ({os.path.getsize(SALIDA) / 1024:.0f} KB, versión {codigo})")
        if not a.sin_subir:
            sube_al_dominio()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
