#!/usr/bin/env python3
"""Selo DCX (DS-6): etiqueta de fita inclinada com uma onda em meio-tom.
Gera o SVG grande (>= 28px de altura) e o simplificado (16 a 27px).
Uso: python3 -I gerar-selo.py svg|p|css   (css = as duas variáveis para colar em components.css)"""
import math, sys

AC, PAPEL = '#e2463f', '#f2e6d4'
W, H, K = 120, 80, 14          # caixa 3:2, inclinação: o topo anda 14 para a direita
def x_em(x, y):                 # desloca x pela inclinação (y=0 topo)
    return x + K * (1 - y / H)

def corpo():
    # paralelogramo (etiqueta de fita) com o canto de baixo à esquerda chanfrado; cantos arredondados
    # pelo traço de 1.2 com junção redonda
    pts = [(K + 1, 1), (W - 1, 1), (W - K - 1, H - 1), (10, H - 1), (2.4, H - 10)]
    d = 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'
    return d

# um compasso de bateria desenhado à mão: bumbo, chimbal, caixa, chimbal (amplitude 0..1 por coluna)
ONDA = [.30, 1.0, .92, .80, .66, .52, .40, .30, .22, .34, .26, .18,
        .14, .86, .80, .66, .52, .40, .30, .22, .32, .24, .16, .12]
ONDA_P = [.95, .62, .34, .30, .88, .55, .32, .24]

def pontos(onda, rows, rmax, x0, x1, y0, y1, borda=.32):
    out = []
    cols = len(onda)
    dx = (x1 - x0) / (cols - 1); dy = (y1 - y0) / (rows - 1)
    yc = (y0 + y1) / 2
    for c, amp in enumerate(onda):
        for r in range(rows):
            y = y0 + r * dy
            u = abs(y - yc) / ((y1 - y0) / 2)          # 0 no eixo, 1 na borda
            k = min(1.0, max(0.0, (amp - u) / borda + .35))  # retícula: cheio no miolo, afina na borda da onda
            rad = rmax * k ** .8
            if rad < .42: continue
            x = x0 + c * dx                             # a onda fica em pé; só o cartão inclina
            out.append(f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{rad:.2f}'/>")
    return ''.join(out)

def grao():
    return ("<filter id='g' x='0' y='0' width='100%' height='100%' color-interpolation-filters='sRGB'>"
            "<feTurbulence type='fractalNoise' baseFrequency='1.6' numOctaves='1' seed='4' result='n'/>"
            "<feColorMatrix in='n' values='0 0 0 0 .32 0 0 0 0 .05 0 0 0 0 .03 2.0 0 0 0 -1.2' result='t'/>"
            "<feComposite in='t' in2='SourceGraphic' operator='in'/></filter>")

def svg(grande=True):
    d = corpo()
    if grande:
        dots = pontos(ONDA, 11, 1.85, 19, 104, 22, 70)
        filete = f"<path d='M19 12.6 L70 12.6' stroke='{PAPEL}' stroke-width='1.6' stroke-linecap='square'/>"
    else:
        dots = pontos(ONDA_P, 5, 4.2, 22, 104, 24, 68, borda=.4)
        filete = ''
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}'>" + "<defs>" + grao() + "</defs>"
            f"<path d='{d}' fill='{AC}' stroke='{AC}' stroke-width='1.2' stroke-linejoin='round'/>"
            f"<g fill='{PAPEL}'>{dots}</g>{filete}"
            f"<path d='{d}' fill='#000' filter='url(#g)' opacity='.5'/></svg>")

def uri(s):
    s = s.replace('%', '%25').replace('#', '%23').replace('<', '%3C').replace('>', '%3E').replace('"', "'")
    return 'url("data:image/svg+xml,' + s + '")'

if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'svg'
    if modo == 'svg':
        print(svg(True))
    elif modo == 'p':
        print(svg(False))
    else:
        print('  --dcx-selo-img: ' + uri(svg(True)) + ';')
        print('  --dcx-selo-img-p: ' + uri(svg(False)) + ';')
