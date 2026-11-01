# -*- coding: utf-8 -*-
"""ROBOTALLER a video: graba escenas del taller (panel_vivo.html, con Token, Torre y los minis) cuadro a cuadro, a 1080p.
No enseña nada real: toda la API del panel se responde con datos de utilería, así que ni sesiones, ni capturas, ni comentarios,
ni el historial pueden colarse en un video. Solo se dibuja el lienzo; las cifras que salgan las pone quien escribe el plan.

  from robotaller import grabar
  grabar("medios/scene-001.mp4", 6.0, [
      dict(t=0, pose="escribir"),                  # Taller.poner(pose): anda a su estación y hace la acción
      dict(t=3.5, pose="fallo"),
      dict(t=4.2, js="Taller.suelta && 0"),        # cualquier JS del taller en ese segundo
  ], pc=dict(cpu=71, gpu=88))

Requiere el panel en marcha (127.0.0.1:8765). `python nucleo/robotaller.py prueba` deja previews en el directorio actual.
"""
import base64
import json
import os
import re
import subprocess
import sys
import time
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

URL = "http://127.0.0.1:8765/v2/vivo"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
CSS = "#taller{position:fixed!important;inset:0!important;width:100vw!important;height:100vh!important;z-index:99999!important;background:#111}"

# rAF apagado: cada cuadro lo pide este script con Taller.pinta(t, dt), así el video no depende de lo rápido que vaya la PC
SIN_RAF = "window.requestAnimationFrame=()=>0;window.EN_VIDEO=true;"
# sin sesión real el robot siempre estaría «libre» y se iría a descansar en plena escena
SIEMPRE_OCUPADO = "window.principalAlDia=()=>false;"


# el monitor colgado en el taller: se dibuja dentro del lienzo (Cap.medio), así Token, bichos y partículas pasan POR DELANTE de la captura
MONITOR_JS = r"""
window.Monitor=(()=>{
  const g=document.getElementById('taller').getContext('2d'),X=430,Y=124,AN=1064,AL=626,B=20;
  const M={img:null,baja:false,ini:-1e9,gol:-1e9,golA:0,est:0,apag:false,ahora:0};
  const rebote=u=>{const n=7.5625,d=2.75;if(u<1/d)return n*u*u;if(u<2/d)return n*(u-=1.5/d)*u+.75;if(u<2.5/d)return n*(u-=2.25/d)*u+.9375;return n*(u-=2.625/d)*u+.984375;};
  function pinta(t){
    if(!M.baja&&t-M.ini>520)return;
    const fuera=-(Y+AL+60),of=M.baja?(1-rebote(Math.min(1,(t-M.ini)/800)))*fuera:Math.min(1,(t-M.ini)/500)**2*fuera;
    const a=t>M.gol?M.golA*Math.exp(-(t-M.gol)/800)*Math.sin((t-M.gol)/105):0,cx=X+AN/2;
    g.save();g.translate(cx,60+of);g.rotate(a);g.translate(-cx,-60);
    g.strokeStyle="#3a415e";g.lineWidth=7;g.lineCap="round";
    for(const x of [X+150,X+AN-150]){g.beginPath();g.moveTo(x,Y+4);g.lineTo(x,100-of);g.stroke();}
    g.shadowColor="rgba(91,192,255,.55)";g.shadowBlur=90;g.fillStyle="#232a42";g.beginPath();g.roundRect(X,Y,AN,AL,22);g.fill();g.shadowBlur=0;
    g.strokeStyle="#4a5478";g.lineWidth=3;g.stroke();
    const sx=X+B,sy=Y+B,sw=AN-2*B,sh=AL-2*B-14;
    g.fillStyle="#05070d";g.fillRect(sx,sy,sw,sh);
    if(M.img&&!M.apag)g.drawImage(M.img,sx,sy,sw,sh);
    if(t<M.est){for(let i=0;i<500;i++){const v=Math.random()*255|0;g.fillStyle=`rgb(${v},${v},${v})`;g.fillRect(sx+Math.random()*sw,sy+Math.random()*sh,10+Math.random()*44,3+Math.random()*8);}}
    const br=g.createLinearGradient(sx,sy,sx+sw*.5,sy+sh);br.addColorStop(0,"rgba(255,255,255,.06)");br.addColorStop(.35,"rgba(255,255,255,0)");g.fillStyle=br;g.fillRect(sx,sy,sw,sh);
    g.fillStyle=Math.sin(t/260)>0?"#5fe0a0":"#2c7a56";g.beginPath();g.arc(X+AN-40,Y+AL-13,6,0,7);g.fill();
    g.restore();
  }
  Taller.POSES.senala=T=>({boca:Math.abs(Math.sin(T*10))*.75,cara:"feliz",brD:[33,-50+Math.sin(T*5)*4],brI:[-15,-20],mira:3,incl:.07});
  const prev=Taller.Cap.medio;
  Taller.Cap.medio=(t,dt)=>{if(prev)prev(t,dt);M.ahora=t;pinta(t);};
  return {
    baja(){M.baja=true;M.ini=M.ahora;M.apag=false;},sube(){M.baja=false;M.ini=M.ahora;},
    golpe(a=.035){M.gol=M.ahora;M.golA=a;},estatica(ms=180){M.est=M.ahora+ms;},apaga(v=true){M.apag=v;},
    async frame(b){const i=await createImageBitmap(await (await fetch("data:image/jpeg;base64,"+b)).blob());if(M.img)M.img.close();M.img=i;},
  };
})();
"""


class _Pantalla:
    """Las capturas que pasan por el monitor. Entradas dict(de, a, clip, desde=0, vel=1, recorte=(x, y, an, al) en fracciones)."""

    def __init__(self, entradas):
        self.ent = sorted(entradas, key=lambda d: d["de"])
        self.act, self.cap, self.pos, self.fps = None, None, -1, 12

    def cuadro(self, t):
        import cv2
        d = next((x for x in self.ent if x["de"] <= t < x["a"]), None)
        if d is None:
            return None, False
        nuevo = d is not self.act
        if nuevo:
            if self.cap:
                self.cap.release()
            self.act, self.cap = d, cv2.VideoCapture(d["clip"])
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 12
            self.pos = int(d.get("desde", 0) * self.fps) - 1
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.pos + 1)
        meta = int((d.get("desde", 0) + (t - d["de"]) * d.get("vel", 1)) * self.fps)
        f = None
        while self.pos < meta:
            ok, g = self.cap.read()
            if not ok:
                break
            f, self.pos = g, self.pos + 1
        if f is None:
            return None, nuevo
        if d.get("recorte"):
            x, y, an, al = d["recorte"]
            h, w = f.shape[:2]
            f = f[int(y * h):int((y + al) * h), int(x * w):int((x + an) * w)]
        f = cv2.resize(f, (1024, 576), interpolation=cv2.INTER_AREA)
        return base64.b64encode(cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, 90])[1].tobytes()).decode(), nuevo


def muestra_pc(cpu=38, gpu=64, temp=61, vram=5.1, ram=52, c=71, e=64, red=4.2, tarea=None):
    """/api/v2/sistema de utilería, con las claves que lee Taller.datosPC."""
    return dict(edad=1, cpu=dict(uso=cpu, nucleos=[cpu] * 16, n=16), ram=dict(pct=ram, usado_gb=17.8, total_gb=34.3),
                gpu=dict(nombre="GPU", uso=gpu, temp=temp, mem=vram * 1024, mem_total=8188, watts=None, watts_max=115, ventilador=45, procesos=[]),
                discos=[dict(unidad="C:", pct=c, libre_gb=120, total_gb=476), dict(unidad="E:", pct=e, libre_gb=700, total_gb=2000)],
                io=dict(recv_mb_s=red, sent_mb_s=.4), io_discos={}, procesos=[], otros=[], tarea=tarea)


def _rutas(pg):
    """Toda la API responde utilería; nunca llega al panel real."""
    def responde(route):
        u = route.request.url
        if "/api/v2/sistema" in u:
            cuerpo = muestra_pc()
        elif "/api/v2/agente/sesiones" in u:
            cuerpo = []
        elif "/api/v2/agente" in u:
            cuerpo = dict(eventos=[], ev=[], ayudantes=[], equipo=[], web={}, contexto={}, etapa_actual=None)
        else:
            cuerpo = {}
        route.fulfill(status=200, content_type="application/json", body=json.dumps(cuerpo))
    pg.route("**/api/**", responde)


def grabar(salida, dur, plan=(), fps=30, w=1920, h=1080, pc=None, tema=None, crf=18, esquema="dark", fiesta="ninguna", monitor=(), hasta=None, previo=None):
    """Graba `dur` segundos del taller en `salida` (mp4 sin audio). plan = pasos dict(t, pose|js). monitor = capturas en la pantalla colgada (_Pantalla).
    hasta = se detiene en ese segundo, con el plan ya aplicado (pruebas). previo = JS propio del video, una vez, antes del primer cuadro (utilería dibujada en el taller)."""
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    ff = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", salida], stdin=subprocess.PIPE)
    plan = sorted(plan, key=lambda p: p.get("t", 0))
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True, channel="chrome")
        pg = nav.new_page(viewport=dict(width=w, height=h), device_scale_factor=1, color_scheme=esquema)
        pg.add_init_script(SIN_RAF)
        _rutas(pg)
        errores = []
        pg.on("pageerror", lambda ex: errores.append(str(ex)))
        pg.goto(f"{URL}?fiesta={fiesta}" + (f"&canal={tema}" if tema else ""), wait_until="load")
        pg.evaluate(SIEMPRE_OCUPADO)
        pg.add_style_tag(content=CSS)
        pg.evaluate("dispatchEvent(new Event('resize'))")
        pg.evaluate("m=>Taller.datosPC(m)", pc or muestra_pc())
        if monitor:
            pg.evaluate(MONITOR_JS)
        if previo:
            pg.evaluate(previo)
        if "senala" not in pg.evaluate("Object.keys(Taller.POSES)"):
            pg.evaluate("Taller.POSES.senala=T=>({boca:Math.abs(Math.sin(T*10))*.75,cara:'feliz',brD:[33,-50+Math.sin(T*5)*4],brI:[-15,-20],mira:3,incl:.07})")
        pantalla = _Pantalla(monitor)
        dt = 1000 / fps
        i = 0
        for n in range(int(round(min(dur, hasta or dur) * fps))):
            t = n * dt
            while i < len(plan) and plan[i].get("t", 0) * 1000 <= t:
                paso = plan[i]
                i += 1
                if paso.get("pose"):
                    pg.evaluate("n=>Taller.poner(n,null,true)", paso["pose"])
                if paso.get("js"):
                    pg.evaluate(paso["js"])
            imagen, cambio = pantalla.cuadro(t / 1000)
            if cambio:
                pg.evaluate("Monitor.estatica(170)")
            if imagen:
                pg.evaluate("b=>Monitor.frame(b)", imagen)
            datos = pg.evaluate("([t,dt])=>{Taller.pinta(t,dt);return document.getElementById('taller').toDataURL('image/jpeg',.95)}", [t + 5000, dt])
            ff.stdin.write(base64.b64decode(datos.split(",", 1)[1]))
        nav.close()
    ff.stdin.close()
    ff.wait()
    if errores:
        print("(aviso) errores de la página:", errores[:3])
    return salida


# ---- lo REAL: grabar_real pasa por aquí toda la API. Lo de los tres canales protegidos se QUITA de las listas; lo demás privado se tapa
TAPA = "▒▒▒▒"
_USUARIO = re.compile(r"[/\\]?\b[cC]:?[/\\]+Users[/\\]+\w+|\bjaire\w*", re.I)    # rutas con el usuario de Windows
_DINERO = re.compile(r"ingres|revenue|rpm|cpm|usd|dinero|ganancia|saldo|estimad", re.I)


def _rojos():
    import filtro_canal as F
    return F.rojo(), [re.compile(p) for t, p in F.PATRONES if t != "id de voz"]


def enmascara(obj, _r=[]):
    """Limpia cualquier JSON: quita de las listas lo que delate a un canal protegido, quita las claves de dinero y tapa correos, claves y enlaces."""
    if not _r:
        _r.extend(_rojos())
    rojo, patrones = _r
    if isinstance(obj, str):
        obj = _USUARIO.sub(TAPA, rojo.sub(TAPA, obj))
        for m in patrones:
            obj = m.sub(TAPA, obj)
        return obj
    if isinstance(obj, list):
        return [enmascara(x) for x in obj if not (isinstance(x, (dict, list, str)) and rojo.search(json.dumps(x, ensure_ascii=False)))]
    if isinstance(obj, dict):
        return {k: enmascara(v) for k, v in obj.items() if not rojo.search(str(k)) and not _DINERO.search(str(k))}
    return obj


def _sin_catalogo(u, datos):
    """Nada de estrenos que tapen la grabación; lo protegido ya lo quita enmascara."""
    if "/api/v2/vivo/mundo" in u and isinstance(datos, dict):
        datos.update(master=None, voz=[])
    return datos


def _rutas_reales(pg, sesion=None, cuadro=None, imagenes=False):
    """La API real, tapada. Las imágenes del historial no pasan salvo imagenes=True (revisadas a mano): una captura del navegador puede traer Studio o un correo."""
    def responde(route):
        u = route.request.url
        if "/v2/vivo/img/" in u:
            return route.fallback() if imagenes else route.abort()
        r = route.fetch()
        if "json" not in r.headers.get("content-type", ""):
            return route.fulfill(response=r)
        datos = _sin_catalogo(u, r.json())
        if "/api/v2/agente/sesiones" in u and sesion and isinstance(datos, list):
            datos = [x for x in datos if x.get("id") == sesion]
        if "/api/v2/sistema" in u and isinstance(datos, dict):
            datos.update(procesos=[], otros=[], tarea=None)
            if isinstance(datos.get("gpu"), dict):
                datos["gpu"]["procesos"] = []
        if cuadro:
            datos = cuadro(u, datos)
        route.fulfill(status=200, content_type="application/json", body=json.dumps(enmascara(datos), ensure_ascii=False))

    def imagen(route):                          # ni miniatura ni foto de un canal protegido, venga por donde venga
        if route.request.resource_type in ("image", "media") and rojo.search(unquote(route.request.url)):
            return route.abort()
        route.fallback()
    def canales(route):                         # la pestaña Canales trae sus datos dentro del HTML (const DATA), no por la API
        r = route.fetch()
        h = r.text()
        m = re.search(r"const DATA = (.*);\n", h)
        if not m:
            return route.abort()
        limpio = json.dumps(enmascara(json.loads(m.group(1).replace("<\\/", "</"))), ensure_ascii=False).replace("</", "<\\/")
        route.fulfill(response=r, body=h[:m.start(1)] + limpio + h[m.end(1):])
    rojo = _rojos()[0]
    pg.route("**/*", imagen)
    pg.route("**/api/**", responde)
    pg.route("**/v2/vivo/img/**", responde)
    pg.route("**/canales", canales)


def grabar_real(salida, url, dur, acciones=(), fps=12, w=1600, h=900, escala=1.5, sesion=None, cuadro=None, esquema="dark", espera=2.0, css="", imagenes=False, reloj=None):
    """Graba en tiempo real una página del panel con la API tapada. acciones = pasos dict(t, js). Mantiene la cadencia repitiendo cuadros si la PC se atrasa."""
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    ff = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264",
                           "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", salida], stdin=subprocess.PIPE)
    acciones = sorted(acciones, key=lambda p: p.get("t", 0))
    base = URL.rsplit("/v2", 1)[0]
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=False, channel="chrome", args=["--window-position=-3000,0", "--enable-webgl", "--ignore-gpu-blocklist", "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding", "--autoplay-policy=no-user-gesture-required"])
        pg = nav.new_page(viewport=dict(width=w, height=h), device_scale_factor=escala, color_scheme=esquema)
        _rutas_reales(pg, sesion, cuadro, imagenes)
        pg.goto(url if url.startswith("file:") else base + url, wait_until="load")
        if css:
            pg.add_style_tag(content=css)
        time.sleep(espera)
        ini, hecho, i, ultimo, marcas = time.time(), 0, 0, None, []
        while hecho < dur * fps:
            ahora = time.time() - ini
            if reloj and len(marcas) <= ahora * 2:     # qué mostraba la página en cada momento, para cortar luego sin mirar cuadro por cuadro
                marcas.append((round(ahora, 1), pg.evaluate(reloj)))
            while i < len(acciones) and acciones[i].get("t", 0) <= ahora:
                pg.evaluate(acciones[i]["js"])
                i += 1
            ultimo = pg.screenshot(type="jpeg", quality=88)
            ahora = time.time() - ini
            while hecho < max(1, ahora * fps) and hecho < dur * fps:
                ff.stdin.write(ultimo)
                hecho += 1
        nav.close()
    ff.stdin.close()
    ff.wait()
    if reloj:
        json.dump(marcas, open(salida + ".json", "w", encoding="utf-8"), ensure_ascii=False)
    return salida


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prueba":
        grabar("robotaller_prueba.mp4", 8, [dict(t=0, pose="escribir"), dict(t=4, pose="pintar")])
        print("ok: robotaller_prueba.mp4")
