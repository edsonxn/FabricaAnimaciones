# -*- coding: utf-8 -*-
"""APK «En vivo» (4-nov-2026): el control remoto del directo SOLO en la wifi de la casa, sin túnel ni clave del panel.

    python nucleo/envivo/android/construir_apk.py        → nucleo/envivo/android/envivo.apk (mandarla por Rayo)

Misma receta sin Gradle que la app de la Fábrica (nucleo/app_movil/android/construir_apk.py: aapt2 + javac + d8 + zipalign +
apksigner, misma llave local). La app busca la PC por UDP (puerto 8792) y abre http://PC:8790/movil.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(AQUI)), "app_movil", "android"))
import construir_apk as FAB                    # noqa: E402  (ultimo, correr, llave y SDK de la app de la Fábrica)

SALIDA = os.path.join(AQUI, "envivo.apk")


def icono(lado):
    """Punto rojo «en vivo» sobre negro cálido con ondas: se distingue del icono de la Fábrica."""
    k = 4
    im = Image.new("RGBA", (lado * k, lado * k), (11, 10, 9, 255))
    g = ImageDraw.Draw(im)
    c, r = lado * k / 2, lado * k * 0.13
    for i, a in ((1, 200), (2, 120)):
        rr = r + i * lado * k * 0.12
        g.arc((c - rr, c - rr, c + rr, c + rr), 300, 60, fill=(236, 230, 214, a), width=int(lado * k * 0.045))
        g.arc((c - rr, c - rr, c + rr, c + rr), 120, 240, fill=(236, 230, 214, a), width=int(lado * k * 0.045))
    g.ellipse((c - r, c - r, c + r, c + r), fill=(196, 38, 30, 255))
    return im.resize((lado, lado), Image.LANCZOS)


def main():
    bt = FAB.ultimo(os.path.join(FAB.SDK, "build-tools", "*"))
    android_jar = os.path.join(FAB.ultimo(os.path.join(FAB.SDK, "platforms", "android-*")), "android.jar")
    aapt2, zipalign = os.path.join(bt, "aapt2.exe"), os.path.join(bt, "zipalign.exe")
    d8, apksigner = os.path.join(bt, "d8.bat"), os.path.join(bt, "apksigner.bat")
    tmp = tempfile.mkdtemp(prefix="envivo_apk_")
    try:
        res = os.path.join(tmp, "res")
        for carpeta, lado in (("mipmap-mdpi", 48), ("mipmap-hdpi", 72), ("mipmap-xhdpi", 96), ("mipmap-xxhdpi", 144), ("mipmap-xxxhdpi", 192)):
            os.makedirs(os.path.join(res, carpeta))
            icono(lado).save(os.path.join(res, carpeta, "ic_launcher.png"))
        codigo = int(time.time() // 60)
        man = open(os.path.join(AQUI, "AndroidManifest.xml"), encoding="utf-8").read()
        man = man.replace("@VERSION_CODE@", str(codigo)).replace("@VERSION_NAME@", time.strftime("1.%Y%m%d.%H%M"))
        manifest = os.path.join(tmp, "AndroidManifest.xml")
        open(manifest, "w", encoding="utf-8").write(man)
        flat, base, gen = os.path.join(tmp, "flat.zip"), os.path.join(tmp, "base.apk"), os.path.join(tmp, "gen")
        FAB.correr([aapt2, "compile", "--dir", res, "-o", flat])
        FAB.correr([aapt2, "link", "-o", base, "-I", android_jar, "--manifest", manifest, "--java", gen, flat, "--auto-add-overlay"])
        clases, dex = os.path.join(tmp, "clases"), os.path.join(tmp, "dex")
        fuentes = [os.path.join(AQUI, "MainActivity.java")] + glob.glob(os.path.join(gen, "**", "*.java"), recursive=True)
        FAB.correr(["javac", "--release", "11", "-encoding", "UTF-8", "-classpath", android_jar, "-d", clases, *fuentes])
        os.makedirs(dex)
        FAB.correr([d8, "--release", "--min-api", "24", "--lib", android_jar, "--output", dex,
                    *glob.glob(os.path.join(clases, "**", "*.class"), recursive=True)], shell=False)
        with zipfile.ZipFile(base, "a", zipfile.ZIP_DEFLATED) as z:
            z.write(os.path.join(dex, "classes.dex"), "classes.dex")
        alineado = os.path.join(tmp, "alineado.apk")
        FAB.correr([zipalign, "-f", "-p", "4", base, alineado])
        FAB.correr([apksigner, "sign", "--ks", FAB.LLAVE, "--ks-pass", f"pass:{FAB.CLAVE_LLAVE}", "--key-pass",
                    f"pass:{FAB.CLAVE_LLAVE}", "--out", SALIDA, alineado])
        FAB.correr([apksigner, "verify", SALIDA])
        print(f"APK listo: {SALIDA} ({os.path.getsize(SALIDA) / 1024:.0f} KB, versión {codigo})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
