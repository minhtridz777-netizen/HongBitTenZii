"""Ve vet chem do tham + bac (hinh tam) va dong vao nakroth.sff.
Chay: python gen_slash_sff.py <kfm.sff nguon> <nakroth.sff dich> <thu muc xem truoc>
Nhom sprite 8000-8099 (quy uoc: hieu ung). Bang mau rieng (8000,1) - khong bi doi mau theo palette nhan vat.
"""
import sys, os, io, math, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from sff2 import read_sff, write_sff

src, dst, prev = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(prev, exist_ok=True)

# ---- Bang mau: 0 trong suot, 1..255 do tham -> do -> hong -> bac trang ----
stops = [(0.0, (40, 0, 6)), (0.35, (150, 0, 20)), (0.6, (230, 30, 50)),
         (0.8, (255, 130, 140)), (1.0, (245, 245, 255))]
def grad(u):
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if u <= b:
            k = (u - a) / (b - a)
            return tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3))
    return stops[-1][1]
PAL = [(0, 0, 0)] + [grad(i / 254) for i in range(255)]

SS = 4  # ve phong to 4 lan roi thu nho cho min

def arc_layer(size, cx, cy, rx, ry, t0, t1, thick, reveal=1.0, rot=0):
    """Mat na luoi liem: cung ellipse, day o giua, nhon 2 dau."""
    w, h = size
    img = Image.new('L', (w * SS, h * SS), 0)
    d = ImageDraw.Draw(img)
    n = 60
    # canh cung (ban day du) vao giua khung
    full = [(cx + rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
             cy + ry * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    bx = (min(p[0] for p in full) + max(p[0] for p in full)) / 2
    by = (min(p[1] for p in full) + max(p[1] for p in full)) / 2 + thick * 0.4
    cx, cy = cx + (w / 2 - bx), cy + (h / 2 - by)
    t1r = t0 + (t1 - t0) * reveal
    outer, inner = [], []
    for i in range(n + 1):
        u = i / n
        t = math.radians(t0 + (t1r - t0) * u)
        px, py = cx + rx * math.cos(t), cy + ry * math.sin(t)
        # phap tuyen huong vao tam
        nx, ny = -math.cos(t) * ry, -math.sin(t) * rx
        ln = math.hypot(nx, ny) or 1
        # do day lon dan ve phia dau lui cua nhat chem (cam giac toc do)
        k = math.sin(math.pi * u) ** 0.8 * (0.35 + 0.65 * u)
        th = thick * k
        outer.append((px * SS, py * SS))
        inner.append(((px + nx / ln * th) * SS, (py + ny / ln * th) * SS))
    d.polygon(outer + inner[::-1], fill=255)
    if rot:
        img = img.rotate(rot, resample=Image.BICUBIC, center=(w * SS / 2, h * SS / 2))
    return img.resize((w, h), Image.LANCZOS)

def compose(layers):
    """layers: list (mask, intensity). Tra ve anh do sang 0..1 (list float)."""
    w, h = layers[0][0].size
    acc = [0.0] * (w * h)
    for m, k in layers:
        for i, v in enumerate(m.getdata()):
            acc[i] = max(acc[i], v / 255 * k)
    return acc, w, h

def to_p(acc, w, h):
    im = Image.new('P', (w, h))
    im.putpalette([c for rgb in PAL for c in rgb])
    im.putdata([0 if v < 0.04 else max(1, min(255, int(v * 255))) for v in acc])
    return im

def slash_frames(size, cx, cy, rx, ry, t0, t1, thick, rot=0):
    frames = []
    # (reveal, do sang, he so do day)
    for reveal, bright, tk in [(0.45, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 0.7, 0.75), (1.0, 0.4, 0.5)]:
        L = []
        L.append((arc_layer(size, cx, cy, rx, ry, t0, t1, thick * 1.7 * tk, reveal, rot).filter(ImageFilter.GaussianBlur(2)), 0.45 * bright))
        L.append((arc_layer(size, cx, cy, rx, ry, t0, t1, thick * tk, reveal, rot), 0.75 * bright))
        L.append((arc_layer(size, cx, cy, rx, ry, t0, t1, thick * 0.35 * tk, reveal, rot), 1.0 * bright))
        frames.append(to_p(*compose(L)))
    return frames

def glint_frames():
    out = []
    for s, b in [(6, 0.7), (11, 1.0), (7, 0.6)]:
        w = h = 28
        img = Image.new('L', (w * SS, h * SS), 0)
        d = ImageDraw.Draw(img)
        c = w * SS / 2
        for ang in (0, 90):
            a = math.radians(ang)
            L, W = s * SS, 1.6 * SS
            pts = [(c + math.cos(a) * L, c + math.sin(a) * L), (c + math.cos(a + 1.57) * W, c + math.sin(a + 1.57) * W),
                   (c - math.cos(a) * L, c - math.sin(a) * L), (c - math.cos(a + 1.57) * W, c - math.sin(a + 1.57) * W)]
            d.polygon(pts, fill=255)
        m = img.resize((w, h), Image.LANCZOS)
        out.append(to_p(*compose([(m.filter(ImageFilter.GaussianBlur(1.5)), 0.6 * b), (m, b)])))
    return out

def trail_frames():
    out = []
    for ln, b in [(1.0, 1.0), (0.8, 0.7), (0.6, 0.4)]:
        w, h = 120, 30
        img = Image.new('L', (w * SS, h * SS), 0)
        d = ImageDraw.Draw(img)
        x1 = w * SS * (1 - ln)
        d.polygon([(x1, h * SS / 2), (w * SS * 0.9, h * SS * 0.28), (w * SS, h * SS / 2), (w * SS * 0.9, h * SS * 0.72)], fill=255)
        m = img.resize((w, h), Image.LANCZOS)
        out.append(to_p(*compose([(m.filter(ImageFilter.GaussianBlur(2)), 0.5 * b), (m, 0.8 * b)])))
    return out

# ---- Danh sach hieu ung: nhom -> frames ----
FX = {
    8000: slash_frames((110, 60), 50, 14, 52, 22, 200, 340, 12),            # chem ngang (cung tren)
    8010: slash_frames((110, 90), 55, 30, 50, 22, 200, 340, 12, rot=-35),   # chem cheo xuong
    8020: slash_frames((110, 100), 55, 40, 50, 22, 200, 340, 12, rot=55),   # vay len
    8030: slash_frames((200, 70), 100, 18, 95, 24, 195, 345, 18),           # chem quet lon (cuong hoa)
    8040: [a for a in slash_frames((110, 90), 55, 30, 50, 22, 200, 340, 10, rot=30)],  # cheo phai (dung cho X)
    8045: [a for a in slash_frames((110, 90), 55, 30, 50, 22, 200, 340, 10, rot=-30)], # cheo trai
    8050: glint_frames(),                                                     # loe dao
    8060: trail_frames(),                                                     # vet luot
}

sff = read_sff(src)
sff['sprites'] = [s for s in sff['sprites'] if not (8000 <= s['g'] < 8100)]
sff['pals'] = [p for p in sff['pals'] if not (p['g'] == 8000)]
pal_index = len(sff['pals'])
sff['pals'].append(dict(g=8000, n=1, ncol=256, link=0,
                        data=b''.join(bytes((r, g, b, 0 if i == 0 else 255)) for i, (r, g, b) in enumerate(PAL))))

sheet = []
for g, frames in FX.items():
    for n, im in enumerate(frames):
        buf = io.BytesIO()
        im.save(buf, format='PNG', optimize=True)
        w, h = im.size
        data = struct.pack('<I', w * h) + buf.getvalue()
        sff['sprites'].append(dict(g=g, n=n, w=w, h=h, ax=w // 2, ay=h // 2, link=0, fmt=10, depth=8,
                                   data=data, pal=pal_index, flags=0))
        sheet.append(im.convert('RGB'))
write_sff(dst, sff)

# Anh xem truoc (nen den) de kiem tra bang mat
W = sum(i.width for i in sheet[:16]) + 16 * 4
rows = [sheet[i:i + 4] for i in range(0, len(sheet), 4)]
H = sum(max(i.height for i in r) + 4 for r in rows)
pv = Image.new('RGB', (max(sum(i.width + 4 for i in r) for r in rows), H), (20, 20, 24))
y = 0
for r in rows:
    x = 0
    for im in r:
        pv.paste(im, (x, y)); x += im.width + 4
    y += max(i.height for i in r) + 4
pv = pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST)
pv.save(os.path.join(prev, 'slash_preview.png'))
print('sprites', len(sff['sprites']), 'pals', len(sff['pals']), 'fx frames', len(sheet))
