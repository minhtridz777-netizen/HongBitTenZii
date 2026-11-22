"""Sinh map thu nghiem 'lab_bac' (stages/lab_bac.def + .sff): rong 3 man hinh, co 6 bac lo lung.
Chay: python tools/gen_stage_lab.py
Toa do map: localcoord 640x360, mat dat y = 320 (zoffset). Bac khai bao trong [Constants] (doc boi shared/system/platforms.zss).
"""
import os, sys, io, struct, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from sff2 import read_sff, write_sff

W_LOCAL, H_LOCAL, GROUND = 640, 360, 320
WORLD_L, WORLD_R = -960, 960
PLATS = [  # (x1, x2, y) - nhay thuong cao ~72, nhay doi ~125
    (-600, -420, -50),
    (-380, -180, -95),
    (-100, 60, -140),
    (120, 320, -60),
    (380, 580, -50),
    (640, 840, -100),
]

def to_p8(img):
    """RGBA -> (anh P co mau 0 trong suot, bang mau 256 RGBA)."""
    img = img.convert('RGBA')
    alpha = img.getchannel('A')
    q = img.convert('RGB').quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:255 * 3]
    idx = [0 if a < 128 else i + 1 for i, a in zip(q.getdata(), alpha.getdata())]
    out = Image.new('P', img.size)
    full = [0, 0, 0] + pal + [0, 0, 0] * (256 - 1 - len(pal) // 3)
    out.putpalette(full[:768])
    out.putdata(idx)
    rgba = b''.join(bytes((full[i * 3], full[i * 3 + 1], full[i * 3 + 2], 0 if i == 0 else 255)) for i in range(256))
    return out, rgba

def sky():
    im = Image.new('RGBA', (64, 800))
    d = ImageDraw.Draw(im)
    for y in range(800):
        k = min(1, max(0, (y - 120) / 520))
        d.line([(0, y), (64, y)], fill=(int(70 + 90 * k), int(130 + 80 * k), int(200 + 40 * k), 255))
    return im

def hills(w, h, col, seed, amp):
    random.seed(seed)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts, y = [], h * 0.5
    for x in range(0, w + 8, 8):
        y = max(4, min(h - 10, y + random.uniform(-amp, amp)))
        pts.append((x, y))
    d.polygon(pts + [(w, h), (0, h)], fill=col)
    return im

def ground(w):
    im = Image.new('RGBA', (w, 140))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, im.height], fill=(110, 78, 50, 255))
    d.rectangle([0, 0, w, 5], fill=(90, 170, 70, 255))
    random.seed(3)
    for _ in range(w // 6):
        x, y = random.randrange(w), random.randrange(5, im.height)
        d.point((x, y), fill=(130, 95, 62, 255))
    return im

def ledge(w):
    im = Image.new('RGBA', (w, 18), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, 10], fill=(150, 150, 160, 255))     # mat da
    d.rectangle([0, 0, w - 1, 2], fill=(200, 200, 210, 255))      # vien sang tren
    d.rectangle([3, 11, w - 4, 14], fill=(90, 90, 100, 255))      # day
    for x in range(0, w, 24):
        d.line([(x, 3), (x, 10)], fill=(120, 120, 130, 255), width=2)
    return im

world_w = WORLD_R - WORLD_L
layers = [  # (group, img, axis_x, axis_y)
    (0, sky(), 0, 0),
    (1, hills(world_w, 140, (60, 90, 130, 255), 1, 10), 0, 0),
    (2, hills(world_w, 100, (50, 110, 80, 255), 2, 7), 0, 0),
    (3, ground(world_w), 0, 0),
]
for i, (x1, x2, y) in enumerate(PLATS):
    layers.append((10 + i, ledge(x2 - x1), 0, 0))

base = read_sff('stages/stage0.sff')
sff = dict(header=base['header'], sprites=[], pals=[])
preview = Image.new('RGBA', (world_w, H_LOCAL))
for g, img, ax, ay in layers:
    p8, rgba = to_p8(img)
    sff['pals'].append(dict(g=1, n=len(sff['pals']) + 1, ncol=256, link=0, data=rgba))
    buf = io.BytesIO()
    p8.save(buf, format='PNG', optimize=True)
    sff['sprites'].append(dict(g=g, n=0, w=img.width, h=img.height, ax=ax, ay=ay, link=0, fmt=10, depth=8,
                               data=struct.pack('<I', img.width * img.height) + buf.getvalue(),
                               pal=len(sff['pals']) - 1, flags=0))
os.makedirs('stages', exist_ok=True)
write_sff('stages/lab_bac.sff', sff)

# ---- file .def ----
consts = ['plat.count = %d' % len(PLATS)]
bgs = []
for i, (x1, x2, y) in enumerate(PLATS):
    n = i + 1
    consts += ['plat%d.x1 = %d' % (n, x1), 'plat%d.x2 = %d' % (n, x2), 'plat%d.y = %d' % (n, y)]
    bgs.append(f"""[BG Bac {n}]
type = normal
mask = 1
spriteno = {10 + i}, 0
start = {x1}, {GROUND + y}
delta = 1, 1
""")
DEF = f"""; Map thu nghiem LAB: rong 3 man hinh, 6 bac lo lung (sinh bang tools/gen_stage_lab.py)
; Bac: khai bao o [Constants], xu ly boi shared/system/platforms.zss

[Info]
name = "Lab Bac"
displayname = "Lab Bac"
mugenversion = 1.0
author = "MugenFake"

[Constants]
{chr(10).join(consts)}

[Camera]
startx = 0
starty = 0
boundleft = {WORLD_L + W_LOCAL // 2}
boundright = {WORLD_R - W_LOCAL // 2}
boundhigh = -160
boundlow = 0
verticalfollow = .6
floortension = 20
tension = 120
autocenter = 1
zoomout = .8
zoomin = 1
overdrawhigh = 0
overdrawlow = 0
cuthigh = 0
cutlow = 0

[PlayerInfo]
p1startx = -80
p1starty = 0
p1facing = 1
p2startx = 80
p2starty = 0
p2facing = -1
leftbound = {WORLD_L + 20}
rightbound = {WORLD_R - 20}

[Bound]
screenleft = 20
screenright = 20

[StageInfo]
zoffset = {GROUND}
autoturn = 1
resetBG = 1
localcoord = {W_LOCAL}, {H_LOCAL}
xscale = 1
yscale = 1

[Shadow]
intensity = 80
color = 0,0,0
yscale = .25

[Reflection]
intensity = 0

[Music]
bgmusic =

[BGdef]
spr = lab_bac.sff
debugbg = 0

[BG Troi]
type = normal
spriteno = 0, 0
start = 0, -300
delta = .05, .2
tile = 1, 0

[BG Doi xa]
type = normal
mask = 1
spriteno = 1, 0
start = {WORLD_L}, 140
delta = .3, .3

[BG Doi gan]
type = normal
mask = 1
spriteno = 2, 0
start = {WORLD_L}, 210
delta = .6, .6

[BG Dat]
type = normal
mask = 1
spriteno = 3, 0
start = {WORLD_L}, {GROUND - 2}
delta = 1, 1

{chr(10).join(bgs)}"""
open('stages/lab_bac.def', 'w', encoding='utf-8', newline='\r\n').write(DEF)
print('ok:', len(sff['sprites']), 'sprites')
