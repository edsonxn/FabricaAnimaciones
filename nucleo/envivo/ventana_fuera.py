# -*- coding: utf-8 -*-
"""Esconde (o trae) la ventana de Edge del directo SIN minimizarla (5-nov-2026).

Minimizada, Windows deja de dibujarla y OBS transmite negro. Fuera de las pantallas (x = -20000) sigue viva: OBS la capta
igual y no estorba. Se le da el tamaño exacto para que su área de página sea 1920x1080 (Windows no limita SetWindowPos al
tamaño de la pantalla).

    python nucleo/envivo/ventana_fuera.py esconder     la manda fuera de la vista (lo hace solo `directo_yt.py obs`)
    python nucleo/envivo/ventana_fuera.py traer        la trae a la pantalla principal para verla
"""
import ctypes
import ctypes.wintypes as wt
import sys

TITULO = "En vivo"
u = ctypes.windll.user32
u.SetProcessDPIAware()


def ventanas():
    res = []

    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(h, _):
        n = u.GetWindowTextLengthW(h)
        b = ctypes.create_unicode_buffer(n + 1)
        u.GetWindowTextW(h, b, n + 1)
        c = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, c, 64)
        if b.value == TITULO and c.value == "Chrome_WidgetWin_1" and u.IsWindowVisible(h):
            res.append(h)
        return True
    u.EnumWindows(cb, 0)
    return res


def area(h):
    r = wt.RECT()
    u.GetClientRect(h, ctypes.byref(r))
    return r.right - r.left, r.bottom - r.top


BARRA = 31   # Edge en modo app dibuja su barra de título DENTRO del área de cliente: la página queda debajo (OBS la recorta)


def colocar(h, x, y, w=1920, alto=1080 + BARRA):
    if u.IsIconic(h):
        u.ShowWindow(h, 9)                               # SW_RESTORE
    ve, vc = wt.RECT(), wt.RECT()
    u.GetWindowRect(h, ctypes.byref(ve))
    u.GetClientRect(h, ctypes.byref(vc))
    dw = (ve.right - ve.left) - vc.right                 # marco + barra de título
    dh = (ve.bottom - ve.top) - vc.bottom
    SWP_NOZORDER, SWP_NOACTIVATE = 0x4, 0x10
    u.SetWindowPos(h, 0, x, y, w + dw, alto + dh, SWP_NOZORDER | SWP_NOACTIVATE)
    return area(h)


def main():
    accion = sys.argv[1] if len(sys.argv) > 1 else "esconder"
    hs = ventanas()
    if not hs:
        raise SystemExit("no encontré la ventana «En vivo» de Edge")
    for h in hs:
        print(accion, h, colocar(h, -20000 if accion == "esconder" else 0, 0))


if __name__ == "__main__":
    main()
