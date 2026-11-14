# -*- coding: utf-8 -*-
"""APK «Estudio Amaya» (10-nov-2026): la app de Amaya, por el dominio (clicknbusiness.com.mx/amaya/ → túnel de hoy).

    python nucleo/amaya/android/construir_apk.py        → nucleo/amaya/android/amaya.apk (fuera de git; mandarla por Rayo)

Misma receta sin Gradle y misma llave de firma que la app de la Fábrica (nucleo/app_movil/android/construir_apk.py:
aapt2 + javac + d8 + zipalign + apksigner). Lleva DENTRO la llave de Amaya (`clave_amaya` de panel_remoto.json, que solo
abre /amaya/): por eso el .apk NUNCA se sube al dominio ni a git. Si se cambia la llave, recompilar e instalar encima.
"""
import glob
import json
import os
import shutil
import sys
import tempfile
import time
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.dirname(os.path.dirname(AQUI))
RAIZ = os.path.dirname(NUCLEO)
sys.path.insert(0, os.path.join(NUCLEO, "app_movil", "android"))
sys.path.insert(0, os.path.dirname(AQUI))
import construir_apk as FAB                    # noqa: E402  (ultimo, correr, llave y SDK de la app de la Fábrica)
from icono import icono                        # noqa: E402  (el mismo icono que la página: «A» con estrella)

SALIDA = os.path.join(AQUI, "amaya.apk")


def clave_amaya():
    try:
        c = json.load(open(os.path.join(RAIZ, "panel_remoto.json"), encoding="utf-8"))
    except (OSError, ValueError):
        c = {}
    k = c.get("clave_amaya")
    if not k:
        sys.exit("No hay clave_amaya en panel_remoto.json: corre antes `python fab.py panel --remoto`.")
    return k


def main():
    bt = FAB.ultimo(os.path.join(FAB.SDK, "build-tools", "*"))
    android_jar = os.path.join(FAB.ultimo(os.path.join(FAB.SDK, "platforms", "android-*")), "android.jar")
    aapt2, zipalign = os.path.join(bt, "aapt2.exe"), os.path.join(bt, "zipalign.exe")
    d8, apksigner = os.path.join(bt, "d8.bat"), os.path.join(bt, "apksigner.bat")
    tmp = tempfile.mkdtemp(prefix="amaya_apk_")
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
        java = os.path.join(tmp, "src", "MainActivity.java")
        os.makedirs(os.path.dirname(java))
        open(java, "w", encoding="utf-8").write(open(os.path.join(AQUI, "MainActivity.java"), encoding="utf-8").read()
                                                .replace("@CLAVE@", clave_amaya()))
        flat, base, gen = os.path.join(tmp, "flat.zip"), os.path.join(tmp, "base.apk"), os.path.join(tmp, "gen")
        FAB.correr([aapt2, "compile", "--dir", res, "-o", flat])
        FAB.correr([aapt2, "link", "-o", base, "-I", android_jar, "--manifest", manifest, "--java", gen, flat, "--auto-add-overlay"])
        clases, dex = os.path.join(tmp, "clases"), os.path.join(tmp, "dex")
        fuentes = [java] + glob.glob(os.path.join(gen, "**", "*.java"), recursive=True)
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
        try:
            os.remove(SALIDA + ".idsig")
        except OSError:
            pass
        print(f"APK listo: {SALIDA} ({os.path.getsize(SALIDA) / 1024:.0f} KB, versión {codigo})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
