#!/usr/bin/env python3
"""Gera ../textures.css. Cada textura e um SVG pequeno (feTurbulence + filtros) embutido como
data URI, ladrilhavel (stitchTiles). Editar aqui e rodar:  python3 -I gerar-textures.py
Nada de imagem externa, nada de fonte, nada de terceiros."""
import os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, '..', 'textures.css')


def uri(svg):
    svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip()
    svg = svg.replace('%', '%25').replace('#', '%23').replace('<', '%3C').replace('>', '%3E').replace('"', "'")
    return 'url("data:image/svg+xml,' + svg + '")'


def turb(freq, octv, seed, res='', typ='fractalNoise'):
    r = f" result='{res}'" if res else ''
    return f"<feTurbulence type='{typ}' baseFrequency='{freq}' numOctaves='{octv}' seed='{seed}' stitchTiles='stitch'{r}/>"


def mat(rgb, a, b, inp='', res=''):
    """cor fixa rgb (0..1), alfa = a*R + b (limiar suave sobre o ruido)"""
    i = f" in='{inp}'" if inp else ''
    r = f" result='{res}'" if res else ''
    R, G, B = rgb
    return f"<feColorMatrix{i}{r} values='0 0 0 0 {R} 0 0 0 0 {G} 0 0 0 0 {B} {a} 0 0 0 {b}'/>"


def tile(w, h, filt):
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'>"
               f"<filter id='f' x='0' y='0' width='100%' height='100%' color-interpolation-filters='sRGB'>{filt}</filter>"
               f"<rect width='100%' height='100%' filter='url(#f)'/></svg>")


SEPIA = (.34, .25, .13)
FERRUGEM = (.52, .31, .13)
GRAFITE = (.10, .11, .12)
BRANCO = (1, 1, 1)
QUENTE = (1, .97, .9)

T = {}
# papel: fibras curtas nas duas direcoes (o maximo de dois ruidos esticados)
T['fibras'] = (260, tile(260, 260,
    turb('.55 .07', 2, 7, 'a') + turb('.07 .55', 2, 19, 'b') +
    "<feBlend in='a' in2='b' mode='lighten'/>" + mat(SEPIA, 3.2, -2.12)))
# grao de papel: pontos escuros (multiply) e claros (screen) do mesmo ruido
T['grao-escuro'] = (180, tile(180, 180, turb('.9', 2, 3) + mat(SEPIA, 4.5, -2.75)))
T['grao-claro'] = (180, tile(180, 180, turb('.9', 2, 3) + mat(QUENTE, -4.5, 1.75)))
# manchas de oxidacao (foxing): nuvens raras + pintas pequenas
T['manchas'] = (600, tile(600, 600,
    turb('.011', 4, 23, 'n1') + mat(FERRUGEM, 2.6, -1.74, 'n1', 'm1') +
    turb('.08', 2, 5, 'n2') + mat(FERRUGEM, 7, -5.25, 'n2', 'm2') +
    "<feMerge><feMergeNode in='m1'/><feMergeNode in='m2'/></feMerge>"))
# cartao: linhas vergê (laid) e de corrente, tortas pelo ruido
T['verge'] = (240, uri(
    "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><defs>"
    "<pattern id='p' width='240' height='3' patternUnits='userSpaceOnUse'><rect width='240' height='1' fill='#5a4526' fill-opacity='.15'/></pattern>"
    "<filter id='d' filterUnits='userSpaceOnUse' x='-12' y='-12' width='264' height='264'>" + turb('.03 .25', 2, 4) +
    "<feDisplacementMap in='SourceGraphic' scale='1.2' xChannelSelector='R' yChannelSelector='G'/></filter></defs>"
    "<g filter='url(#d)'><rect x='-12' y='-12' width='264' height='264' fill='url(#p)'/>"
    "<rect x='40' y='-12' width='1.4' height='264' fill='#5a4526' fill-opacity='.09'/><rect x='160' y='-12' width='1.4' height='264' fill='#5a4526' fill-opacity='.09'/></g></svg>"))
# serigrafia: densidade irregular da tinta (rodo desigual) e falhas onde a tinta nao passou
T['mancha-tinta'] = (420, tile(420, 420, turb('.007 .011', 3, 31) + mat((0, 0, 0), 1.1, -.42)))
T['falha-tinta'] = (260, tile(260, 260,
    turb('.55 .4', 3, 41, 'a') + mat(BRANCO, -14, 10.3, 'a', 'x') +
    turb('.035', 3, 8, 'b') + mat(BRANCO, -9, 6.9, 'b', 'y') +
    "<feComposite in='x' in2='y' operator='in'/>"))
# metal escovado: estrias longas no eixo x, escuras e claras com sementes diferentes
T['escovado-escuro'] = (640, tile(640, 120, turb('.0011 .6', 2, 13) + mat(GRAFITE, 1.3, -.5)))
T['escovado-claro'] = (640, tile(640, 120, turb('.0011 .6', 2, 29) + mat(BRANCO, -1.5, .66)))
T['riscos'] = (700, tile(700, 700,
    turb('.0016 .9', 1, 3, 'a') + turb('.9 .0016', 1, 9, 'b') +
    "<feBlend in='a' in2='b' mode='lighten'/>" + mat(BRANCO, 26, -19.3)))
# elastomero/plastico: fosco de molde (micro pontilhado)
T['fosco-escuro'] = (160, tile(160, 160, turb('1.3', 1, 17) + mat(GRAFITE, 3.2, -1.82)))
T['fosco-claro'] = (160, tile(160, 160, turb('1.3', 1, 17) + mat(BRANCO, -3.2, 1.38)))
# vidro fume do visor: grao do vidro
T['vidro'] = (200, tile(200, 200, turb('.75', 3, 52) + mat((0, 0, 0), 2.4, -1.05)))
# poeira: pontos raros e fiapos (claro para superficie escura, escuro para papel)
_poeira = (turb('.65', 1, 61, 'a') + "<feColorMatrix in='a' result='p' values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 34 0 0 0 -25.6'/>" +
           turb('.06 .3', 2, 6, 'b') + "<feColorMatrix in='b' result='q' values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 22 0 0 0 -17.2'/>" +
           "<feMerge><feMergeNode in='p'/><feMergeNode in='q'/></feMerge>")
T['poeira-clara'] = (520, tile(520, 520, _poeira + "<feColorMatrix values='0 0 0 0 .93 0 0 0 0 .91 0 0 0 0 .86 0 0 0 .8 0'/>"))
T['poeira-escura'] = (520, tile(520, 520, _poeira + "<feColorMatrix values='0 0 0 0 .30 0 0 0 0 .26 0 0 0 0 .20 0 0 0 .55 0'/>"))
# desgaste: sujeira acumulada em nuvens baixas
_pontos = (turb('.65', 1, 61) + "<feColorMatrix values='0 0 0 0 .93 0 0 0 0 .91 0 0 0 0 .86 34 0 0 0 -25.8'/>")
T['poeira-fina'] = (360, tile(360, 360, _pontos))
T['sujeira'] = (620, tile(620, 620, turb('.0055', 3, 90) + mat((.24, .19, .11), 1.9, -.92)))
# impressao: retícula AM a 45 graus, ponto cresce e encolhe com o ruido (offset de verdade, nao padrao fixo)
T['reticula'] = (240, uri(
    "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><defs>"
    "<radialGradient id='g'><stop offset='0' stop-color='#fff'/><stop offset='1' stop-color='#000'/></radialGradient>"
    "<pattern id='p' width='5.65685' height='5.65685' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'>"
    "<rect width='6' height='6'/><circle cx='2.82843' cy='2.82843' r='2.82843' fill='url(#g)'/></pattern>"
    "<filter id='f' x='0' y='0' width='100%' height='100%' color-interpolation-filters='sRGB'>" + turb('.012', 2, 12, 'n') +
    "<feComposite in='SourceGraphic' in2='n' operator='arithmetic' k2='1' k3='.9' k4='-.47'/>"
    "<feColorMatrix values='0 0 0 0 .11 0 0 0 0 .11 0 0 0 0 .11 14 0 0 0 -7'/></filter></defs>"
    "<rect width='240' height='240' fill='url(#p)' filter='url(#f)'/></svg>"))

# DS-5 capa de cassete: tinta mosqueada (densidade da tinta em nuvens medias + pintas), clara para
# cartao preto (a tinta prata/cinza que nao cobriu por igual) e escura para a faixa cinza
_mosq = turb('.018 .03', 4, 73, 'a') + turb('.22', 2, 11, 'b') + "<feBlend in='a' in2='b' mode='multiply'/>"
# DS-6: mancha bem mais rala (a ref-01 é preto quase chapado com grão fino): limiar mais alto, alfa máximo menor
T['mosqueado-claro'] = (480, tile(480, 480, _mosq + mat((.40, .38, .34), 1.15, -.56)))
T['mosqueado-escuro'] = (480, tile(480, 480, _mosq + mat((.16, .15, .12), -1.7, .80)))

css = []
w = css.append
w("""/* DCX Audio · design system · texturas (DS-1)
 * GERADO por fonte/gerar-textures.py (editar la). Depende de tokens.css.
 *
 * Ideia: cada material e uma pilha de camadas fisicas, como as pecas do 404 (alojamento,
 * borda, superficie): fundo de cor + camada escura (multiply: fibra, mancha, sujeira) +
 * camada clara (screen: grao claro, estria de luz, poeira). As camadas sao SVG feTurbulence
 * ladrilhaveis em data URI, sem arquivo externo.
 *
 * Intensidade: --tex-intensity (0 = liso, 1 = padrao, 1.6 = maximo). Vale para tudo, pode ser
 * trocada por elemento. --tx-desloc muda a origem dos ladrilhos (use .tx-v2/.tx-v3 para que
 * dois cartoes vizinhos nao fiquem iguais).
 *
 * Uso: <div class="tx tx-papel">...</div>   modificadores: .tx-desgaste .tx-poeira .tx-reticula
 *      tinta de serigrafia em texto/logo/bloco: .tx-tinta (e .tx-registro para titulo grande)
 *      componentes: .tx-tecla (elastomero, estados .down/.lit), .tx-visor (LED), .tx-lcd
 *      capa de cassete (DS-5): .tx-capa (cartao preto), .tx-faixa (faixa cinza), .tx-prata,
 *      .tx-dobra (+ .tx-dobra-h; posicao em --dobra)
 *
 * ONDE NAO USAR
 *   - atras de texto corrido ou abaixo de 16px: no maximo papel com --tex-intensity <= .6;
 *     manual e documentacao ficam em .tx-papel leve ou liso
 *   - .tx-tinta (falhas) e .tx-registro so em titulo >= 32px, numeral e logo; nunca em texto
 *     de leitura, link, botao de interface ou campo de formulario
 *   - .tx-reticula so em bloco de cor ou imagem, nunca atras de texto
 *   - nada de textura em foco de teclado, estados de erro, graficos de dados e tabelas
 *   - a face das maquinas ja tem acabamento proprio: nao aplicar por cima dos paineis
 *   - impressao, alto contraste e "reduzir transparencia" desligam tudo (fim do arquivo)
 */
""")
w(':root {\n  --tex-intensity: 1;\n')
for k, (size, u) in T.items():
    w(f'  --tx-{k}: {u};\n')
w('}\n')
w("""
/* ---------------------------------------------------------------- motor de camadas */
.tx { position: relative; isolation: isolate; }
.tx::before, .tx::after {
  content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none; border-radius: inherit;
  opacity: calc(var(--tex-intensity) * .625);
}
/* escuras: e1..e3 do material, e4 impressao, e5 desgaste */
.tx::before {
  background-image: var(--tx-e6, none), var(--tx-e5, none), var(--tx-e4, none), var(--tx-e3, none), var(--tx-e2, none), var(--tx-e1, none);
  background-size: var(--tx-e6s, 100% 100%), var(--tx-e5s, auto), var(--tx-e4s, auto), var(--tx-e3s, auto), var(--tx-e2s, auto), var(--tx-e1s, auto);
  background-position: 0 0, var(--tx-desloc, 0 0), var(--tx-desloc, 0 0), var(--tx-desloc, 0 0), var(--tx-desloc, 0 0), var(--tx-desloc, 0 0);
  mix-blend-mode: multiply;
  box-shadow: var(--tx-borda-gasta, 0 0 0 transparent), var(--tx-borda, 0 0 0 transparent);
}
/* claras: c1..c2 do material, c3 riscos, c4 poeira */
.tx::after {
  background-image: var(--tx-c5, none), var(--tx-c4, none), var(--tx-c3, none), var(--tx-c2, none), var(--tx-c1, none);
  background-size: var(--tx-c5s, 100% 100%), var(--tx-c4s, auto), var(--tx-c3s, auto), var(--tx-c2s, auto), var(--tx-c1s, auto);
  background-position: 0 0, var(--tx-desloc, 0 0), var(--tx-desloc, 0 0), var(--tx-desloc, 0 0), var(--tx-desloc, 0 0);
  mix-blend-mode: screen;
}
.tx-v2 { --tx-desloc: 137px 61px; }
.tx-v3 { --tx-desloc: 311px 197px; }
""")
S = {k: f'{v[0]}px' for k, v in T.items()}
S['escovado-escuro'] = S['escovado-claro'] = '640px 120px'
def lay(slot, name):
    return f'--tx-{slot}: var(--tx-{name}); --tx-{slot}s: {S[name]};'
w(f"""
/* cada .tx zera as camadas: um material dentro de outro nao herda as camadas do de fora */
.tx {{
  --tx-e1: none; --tx-e2: none; --tx-e3: none; --tx-e4: none; --tx-e5: none; --tx-e6: none;
  --tx-c1: none; --tx-c2: none; --tx-c3: none; --tx-c4: none; --tx-c5: none;
  --tx-borda: 0 0 0 transparent; --tx-borda-gasta: 0 0 0 transparent;
}}

/* ---------------------------------------------------------------- papel envelhecido */
.tx-papel {{
  background-color: var(--dcx-branco); color: var(--dcx-preto);
  {lay('e1','fibras')} {lay('e2','grao-escuro')} {lay('e3','manchas')}
  {lay('c1','grao-claro')}
  /* borda amarelada: a folha oxida primeiro pelas beiradas */
  --tx-borda: inset 0 0 0 1px rgba(120, 85, 30, .10), inset 0 0 28px rgba(150, 105, 40, .22), inset 0 0 4px rgba(120, 80, 25, .18);
}}
/* cartao: papel mais grosso, vergê aparente, mais oxidado */
.tx-cartao {{
  background-color: var(--dcx-branco-creme); color: var(--dcx-preto);
  {lay('e1','fibras')} {lay('e2','verge')} {lay('e3','manchas')}
  {lay('c1','grao-claro')}
  --tx-borda: inset 0 0 0 1px rgba(110, 75, 25, .16), inset 0 0 40px rgba(150, 100, 35, .30), inset 0 0 6px rgba(110, 70, 20, .22);
  box-shadow: var(--dcx-sombra-cartao);
}}
/* serigrafia em bloco de cor (cartaz, faixa): densidade irregular da tinta + grao */
.tx-serigrafia {{
  {lay('e1','mancha-tinta')} {lay('e2','grao-escuro')}
  {lay('c1','grao-claro')}
}}
/* tinta de serigrafia em texto grande, numeral ou logo: falhas onde a tela nao passou tinta */
.tx-tinta {{
  -webkit-mask-image: var(--tx-falha-tinta), linear-gradient(rgb(0 0 0 / calc(1 - var(--tex-intensity) * .625)), rgb(0 0 0 / calc(1 - var(--tex-intensity) * .625)));
  -webkit-mask-size: {S['falha-tinta']}, 100% 100%;
  -webkit-mask-composite: source-over;
  mask-image: var(--tx-falha-tinta), linear-gradient(rgb(0 0 0 / calc(1 - var(--tex-intensity) * .625)), rgb(0 0 0 / calc(1 - var(--tex-intensity) * .625)));
  mask-size: {S['falha-tinta']}, 100% 100%;
  mask-composite: add;
  mask-position: var(--tx-desloc, 0 0), 0 0;
}}
/* registro desalinhado: segunda passada de tinta meio pixel fora (so titulo grande) */
.tx-registro {{ text-shadow: calc(var(--tex-intensity) * .9px) calc(var(--tex-intensity) * .5px) 0 var(--tx-registro-cor, rgb(118 35 43 / .55)); }}

/* ---------------------------------------------------------------- metal escovado (aluminio do 404) */
.tx-metal {{
  background-color: var(--dcx-aluminio-2);
  background-image:
    /* faixa de reflexo larga e irregular, ao longo da escovacao */
    linear-gradient(180deg, rgb(255 255 255 / 0) 0%, rgb(255 255 255 / .16) 18%, rgb(255 255 255 / .04) 31%, rgb(255 255 255 / 0) 46%, rgb(0 0 0 / .05) 78%, rgb(0 0 0 / .1) 100%),
    linear-gradient(155.9deg, var(--dcx-aluminio-1) 9%, var(--dcx-aluminio-2) 113%);
  color: var(--dcx-marinho);
  {lay('e1','escovado-escuro')} {lay('e2','fosco-escuro')}
  {lay('c1','escovado-claro')} {lay('c2','riscos')}
  --tx-borda: inset 0 1px 0 rgb(255 255 255 / .55), inset 0 -1px 0 rgb(20 24 30 / .25);
}}
/* metal girado (tampa de knob, botao redondo): aneis de torno + dois reflexos opostos */
.tx-metal-girado {{
  border-radius: 50%;
  background:
    repeating-radial-gradient(circle at 50% 50%, rgb(255 255 255 / 0) 0 .7px, rgb(255 255 255 / .09) .9px, rgb(0 0 0 / .06) 1.4px, rgb(255 255 255 / 0) 1.9px),
    conic-gradient(from 18deg, #9a9ea6, #e6e9ee 8%, #a7abb2 19%, #8d9199 31%, #b9bdc4 44%, #9a9ea6 50%, #eef0f3 58%, #a3a7ae 69%, #8b8f97 81%, #c3c6cc 92%, #9a9ea6);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .5), inset 0 -1px 1px rgb(0 0 0 / .35), var(--dcx-sombra-alojamento);
  {lay('c2','riscos')}
}}

/* ---------------------------------------------------------------- plastico injetado (tecla de funcao) */
.tx-plastico {{
  background-color: var(--dcx-elastomero-1);
  background-image: linear-gradient(to bottom, var(--dcx-elastomero-1), var(--dcx-elastomero-2));
  {lay('e1','fosco-escuro')}
  {lay('c1','fosco-claro')}
  --tx-borda: inset 0 1px 0 rgb(255 255 255 / .35), inset 0 -2px 2px -1px rgb(0 0 0 / .18);
}}

/* ---------------------------------------------------------------- modificadores */
/* desgaste: sujeira em nuvens + escurecimento onde o dedo e a mesa encostam (base) + riscos */
.tx-desgaste {{
  {lay('e5','sujeira')} {lay('c3','riscos')}
  --tx-borda-gasta: inset 0 -10px 14px -10px rgba(45, 32, 12, .45), inset 0 0 0 1px rgba(45, 32, 12, .12);
}}
.tx-poeira {{ {lay('c4','poeira-clara')} }}
.tx-papel.tx-poeira, .tx-cartao.tx-poeira {{ {lay('e4','poeira-escura')} --tx-c4: none; }}
.tx-reticula {{ {lay('e4','reticula')} }}

/* ---------------------------------------------------------------- tecla de elastomero (pecas do 404)
 * <button class="tx-tecla" style="--w:64px;--h:42px"><i class="a"></i><i class="b"></i><i class="s"></i><span>REC</span></button>
 * a = alojamento, b = borda do elastomero, s = superficie moldada. .down = pressionado, .lit = aceso */
.tx-tecla {{ position: relative; width: var(--w, 64px); height: var(--h, 42px); margin: 0; padding: 0; border: 0; background: none; cursor: pointer; font: 700 11px/.98 var(--dcx-fonte-painel-cond); letter-spacing: -.2px; color: #30312f; -webkit-tap-highlight-color: transparent; }}
.tx-tecla > i {{ position: absolute; display: block; box-sizing: border-box; isolation: isolate; }}
.tx-tecla .a {{ inset: 0; border-radius: var(--dcx-r-4); background: var(--dcx-alojamento); box-shadow: var(--dcx-sombra-alojamento); }}
.tx-tecla .b {{ left: 2px; top: 2px; width: calc(var(--w, 64px) - 4px); height: calc(var(--h, 42px) - 5px); border-radius: var(--dcx-r-3); background: var(--dcx-elastomero-borda); border: 1px solid #0d100e; }}
.tx-tecla .s {{ left: 4px; top: 3px; width: calc(var(--w, 64px) - 8px); height: calc(var(--h, 42px) - 7px); border-radius: var(--dcx-r-2); border: .6px solid #b9bdc1; background: linear-gradient(to bottom, var(--dcx-elastomero-1), var(--dcx-elastomero-2)); }}
.tx-tecla .a::after, .tx-tecla .s::before, .tx-tecla .s::after {{ content: ""; position: absolute; inset: 0; border-radius: inherit; z-index: -1; pointer-events: none; opacity: calc(var(--tex-intensity) * .625); }}
/* poeira presa no vao do alojamento */
.tx-tecla .a::after {{ background: var(--tx-poeira-fina) 0 0 / {S['poeira-fina']}; background-position: var(--tx-desloc, 0 0); mix-blend-mode: screen; z-index: 0; }}
/* silicone fosco: micro pontilhado escuro e claro */
.tx-tecla .s::before {{ background: var(--tx-fosco-escuro) 0 0 / {S['fosco-escuro']}; mix-blend-mode: multiply; z-index: 0; }}
.tx-tecla .s::after {{ background: var(--tx-fosco-claro) 0 0 / {S['fosco-claro']}; mix-blend-mode: screen; z-index: 0; }}
.tx-tecla > span {{ position: absolute; left: 50%; top: calc((var(--h, 42px) - 4px) / 2); transform: translate(-50%, -50%); white-space: nowrap; text-align: center; z-index: 1; pointer-events: none; }}
.tx-tecla.lit .b {{ background: var(--dcx-vinho); }}
.tx-tecla.lit .s {{ border-color: #f38c91; background: linear-gradient(to bottom, var(--dcx-rosa), var(--dcx-rosa-sombra)); }}
.tx-tecla.lit > span {{ color: var(--dcx-vinho-tinta); }}
.tx-tecla.down .a {{ box-shadow: none; }}
.tx-tecla.down .s {{ box-shadow: var(--dcx-sombra-moldada); }}
.tx-tecla.down > span {{ transform: translate(-50%, calc(-50% + .5px)); }}
.tx-tecla:focus-visible {{ outline: 2px solid var(--dcx-marinho); outline-offset: 3px; border-radius: var(--dcx-r-4); }}

/* ---------------------------------------------------------------- visor LED de 7 segmentos (cores do 404)
 * <div class="tx-visor"><div class="vidro"> svg com .sg / .sg.on </div></div> */
.tx-visor {{ position: relative; display: inline-block; padding: 2px; background: #191a17; border: 2px solid #3f4038; box-shadow: inset 0 1px 2px rgb(0 0 0 / .6); }}
.tx-visor .vidro {{ position: relative; isolation: isolate; padding: 10px 11px 8px; background: linear-gradient(to bottom, #201c14, #281c17 60%, #3d211c); overflow: hidden; }}
.tx-visor .vidro::before {{ content: ""; position: absolute; inset: 0; z-index: -1; background: var(--tx-vidro) 0 0 / {S['vidro']}; mix-blend-mode: multiply; opacity: calc(var(--tex-intensity) * .625); }}
/* reflexo no vidro (faixa diagonal de janela) e poeira por cima do vidro */
.tx-visor .vidro::after {{ content: ""; position: absolute; inset: 0; z-index: 2; pointer-events: none; mix-blend-mode: screen; opacity: calc(var(--tex-intensity) * .625);
  background: var(--tx-poeira-fina) 0 0 / {S['poeira-fina']},
    linear-gradient(104deg, rgb(255 240 220 / 0) 0 21%, rgb(255 240 220 / .10) 21% 24%, rgb(255 240 220 / .05) 24% 33%, rgb(255 240 220 / 0) 33% 100%),
    linear-gradient(to bottom, rgb(255 255 255 / .07), rgb(255 255 255 / 0) 2px); }}
.tx-visor svg {{ display: block; overflow: visible; }}
.tx-visor .sg {{ fill: var(--dcx-segmento-apagado); }}
.tx-visor .sg.on {{ fill: var(--dcx-vermelho-display); filter: drop-shadow(var(--dcx-brilho-led)) drop-shadow(0 0 7px rgb(245 57 37 / calc(var(--tex-intensity) * .22))); }}

/* LED redondo (peak, rec): apagado mostra a cor do plastico vermelho, aceso tem brilho e halo */
.tx-led {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: radial-gradient(circle at 38% 32%, #6a3a32 0 18%, var(--dcx-segmento-apagado) 55%, #2a1612 100%); box-shadow: inset 0 1px 1px rgb(0 0 0 / .5), 0 0 0 1.5px #191a17, 0 1px 0 1.5px rgb(255 255 255 / .12); }}
.tx-led.on {{ background: radial-gradient(circle at 38% 32%, #fff3e6 0 9%, #ff7a5c 24%, var(--dcx-vermelho-display) 55%, #a8200f 100%); box-shadow: 0 0 0 1.5px #191a17, 0 0 6px 1px rgb(245 57 37 / .6), 0 0 16px 3px rgb(245 57 37 / calc(var(--tex-intensity) * .2)); }}

/* LCD reflexivo apagado (sem luz de fundo): matriz de pontos e vidro. Cor provisoria a partir do
 * cinza de painel; a cor certa do LCD de cada maquina vem do core/css/base.css (card DS-3) */
.tx-lcd {{ position: relative; isolation: isolate; overflow: hidden; background: color-mix(in srgb, var(--dcx-cinza-painel) 70%, #6f7a5e); color: rgb(20 24 16 / .82); box-shadow: inset 0 2px 3px rgb(0 0 0 / .45), inset 0 0 0 2px #191a17; }}
.tx-lcd::before {{ content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none; opacity: calc(var(--tex-intensity) * .625); mix-blend-mode: multiply;
  background: repeating-linear-gradient(90deg, rgb(0 0 0 / .14) 0 .5px, transparent .5px 3px), repeating-linear-gradient(0deg, rgb(0 0 0 / .14) 0 .5px, transparent .5px 3px), var(--tx-vidro) 0 0 / {S['vidro']}; }}
.tx-lcd::after {{ content: ""; position: absolute; inset: 0; pointer-events: none; mix-blend-mode: screen; opacity: calc(var(--tex-intensity) * .625);
  background: linear-gradient(104deg, rgb(255 255 255 / 0) 0 58%, rgb(255 255 255 / .12) 58% 61%, rgb(255 255 255 / 0) 61%), var(--tx-poeira-fina) 0 0 / {S['poeira-fina']}; }}

/* ---------------------------------------------------------------- capa de cassete (DS-5)
 * cartao preto impresso: tinta preta mosqueada (o cartao aparece em nuvens), grao claro de impressao,
 * cantos e arestas gastos (a prata e o preto saem primeiro nas quinas) */
.tx-capa {{
  background-color: var(--dcx-capa); color: var(--dcx-prata);
  {lay('e1','grao-escuro')}
  {lay('c1','mosqueado-claro')} {lay('c2','poeira-fina')}
  --tx-borda: inset 0 0 0 1px rgb(255 248 230 / .05), inset 0 0 36px rgb(190 180 160 / .07), inset 0 0 3px rgb(220 210 190 / .10);
}}
/* faixa cinza larga: tinta cinza chapada, mosqueado escuro onde o rodo carregou mais */
.tx-faixa {{
  background-color: var(--dcx-faixa); color: var(--dcx-faixa-tinta);
  background-image: linear-gradient(180deg, var(--dcx-faixa-clara), var(--dcx-faixa) 38%, color-mix(in srgb, var(--dcx-faixa) 92%, #000));
  {lay('e1','mosqueado-escuro')} {lay('e2','grao-escuro')}
  {lay('c1','grao-claro')}
}}
/* tinta prata sobre preto (palavra-marca, numeral, ficha): falhas + mosqueado na propria letra */
.tx-prata {{ color: var(--dcx-prata-clara); }}
/* dobra do cartao: vinco escuro + aresta clara numa posicao (--dobra-x ou --dobra-y, em %) */
.tx-dobra {{
  --tx-e6: linear-gradient(var(--dobra-ang, 90deg), transparent calc(var(--dobra, 62%) - 9px), rgb(0 0 0 / .16) calc(var(--dobra, 62%) - 1px), rgb(0 0 0 / .42) var(--dobra, 62%), transparent calc(var(--dobra, 62%) + .6px));
  --tx-c5: linear-gradient(var(--dobra-ang, 90deg), transparent calc(var(--dobra, 62%) + .4px), rgb(255 246 226 / .30) calc(var(--dobra, 62%) + 1px), rgb(255 246 226 / .07) calc(var(--dobra, 62%) + 3px), transparent calc(var(--dobra, 62%) + 14px));
}}
.tx-dobra-h {{ --dobra-ang: 180deg; }}

/* ---------------------------------------------------------------- desligar */
@media print {{ :root {{ --tex-intensity: 0; }} }}
@media (prefers-contrast: more) {{ :root {{ --tex-intensity: 0; }} .tx-registro {{ text-shadow: none; }} }}
@media (prefers-reduced-transparency: reduce) {{ :root {{ --tex-intensity: .4; }} }}
""")

out = ''.join(css)
open(SAIDA, 'w').write(out)
print(SAIDA, len(out.encode()), 'bytes')
