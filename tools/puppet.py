"""MODEL TEST - bup be khop noi ve bang code (thu vien).
Moi tu the (pose) = goc cac khop. Ve ra anh P (chi so mau) de doi mau theo palette nhan vat.
He toa do: localcoord 640x360, nhan vat cao ~70 px, quay mat sang PHAI. Truc (axis) = giua 2 chan, mat dat.
"""
import math
from PIL import Image, ImageDraw

CANVAS = (112, 112)
AXIS = (56, 100)

# ---- chi so mau trong palette nhan vat (nhom 1) ----
C_OUT = 1      # vien
C_MAIN = 2     # than truoc (sang)
C_MAIN_D = 3   # chi sau (toi)
C_ACC = 4      # mau phu: dai lung, bang tay
C_ACC_D = 5
C_HEAD = 6     # dau
C_HEAD_D = 7
C_EYE = 8      # kinh mat (cho biet huong mat)

# ---- ti le: 1.0 = cao ~70 px; 0.8 = cao ~56 px (chot sau khi test) ----
SCALE = 0.8
# ---- kich thuoc xuong (px) ----
TORSO, NECK = 21 * SCALE, 2 * SCALE
HEAD_R = round(7 * SCALE)
UARM, FARM = 11 * SCALE, 10 * SCALE
THIGH, SHIN = 15 * SCALE, 15 * SCALE
HIP_Y = -32 * SCALE
# do day net ve (px)
W_TORSO, W_UARM, W_FARM, W_THIGH, W_SHIN, W_FOOT = 8, 4, 3, 5, 4, 3

DEFAULT = dict(
    x=0, y=2,          # dich hong (y + = thap xuong)
    t=4,               # nghieng than (do, + = cui ve truoc)
    fa=(20, 50),       # tay truoc: (goc canh tay tu phuong thang xuong, + = ve truoc), (gap khuyu)
    ba=(-15, 40),      # tay sau
    fl=('ik', 7, -2),  # chan truoc: ('ik', x, y) = dat co chan tai diem (so voi axis, tu tinh goc)
    bl=('ik', -8, -2), #   hoac (goc dui, gap goi) khi o tren khong
    hide=False,
)

def P(**kw):
    p = dict(DEFAULT)
    p.update(kw)
    return p

def lerp(a, b, k):
    out = {}
    for key in a:
        va, vb = a[key], b[key]
        if isinstance(va, tuple):
            if len(va) != len(vb) or (va and isinstance(va[0], str)) != (vb and isinstance(vb[0], str)):
                out[key] = va if k < 0.5 else vb
            else:
                out[key] = tuple(x if isinstance(x, str) else x + (y - x) * k for x, y in zip(va, vb))
        elif isinstance(va, bool):
            out[key] = va if k < 0.5 else vb
        else:
            out[key] = va + (vb - va) * k
    return out

def _pt(o, ang, ln):
    """Diem cach o mot doan ln theo goc ang (do, 0 = thang xuong, + = ve phia truoc/phai)."""
    a = math.radians(ang)
    return (o[0] + math.sin(a) * ln, o[1] + math.cos(a) * ln)

def skeleton(p):
    ox, oy = AXIS[0] + p['x'] * SCALE, AXIS[1] + p['y'] * SCALE
    hip = (ox, oy + HIP_Y)
    t = math.radians(p['t'])
    neck = (hip[0] + math.sin(t) * TORSO, hip[1] - math.cos(t) * TORSO)
    head = (neck[0] + math.sin(t) * (NECK + HEAD_R), neck[1] - math.cos(t) * (NECK + HEAD_R))
    sh = (neck[0] - math.sin(t) * 2, neck[1] + math.cos(t) * 2)
    S = dict(hip=hip, neck=neck, head=head, sh=sh)
    for side, key in (('f', 'fa'), ('b', 'ba')):
        a1, e = p[key]
        el = _pt(sh, a1, UARM)
        ha = _pt(el, a1 + e, FARM)
        S[side + 'el'], S[side + 'ha'] = el, ha
    for side, key in (('f', 'fl'), ('b', 'bl')):
        if isinstance(p[key][0], str):  # IK: dat co chan vao diem chi dinh, goi gap ve phia truoc
            tx, ty = AXIS[0] + p[key][1] * SCALE, AXIS[1] + p[key][2] * SCALE
            dx, dy = tx - hip[0], ty - hip[1]
            d = max(1.0, min(THIGH + SHIN - 0.01, math.hypot(dx, dy)))
            at = math.degrees(math.atan2(dx, dy))
            ca = (THIGH ** 2 + d ** 2 - SHIN ** 2) / (2 * THIGH * d)
            a1 = at + math.degrees(math.acos(max(-1, min(1, ca))))
            kn = _pt(hip, a1, THIGH)
            an = (hip[0] + dx / max(1e-6, math.hypot(dx, dy)) * d, hip[1] + dy / max(1e-6, math.hypot(dx, dy)) * d)
        else:
            a1, k = p[key]
            kn = _pt(hip, a1, THIGH)
            an = _pt(kn, a1 - k, SHIN)
        ft = (an[0] + 4, an[1])
        S[side + 'kn'], S[side + 'an'], S[side + 'ft'] = kn, an, ft
    return S

def _seg(d, a, b, w, fill):
    d.line([a, b], fill=C_OUT, width=w + 2)
    r = (w + 2) / 2
    for q in (a, b):
        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=C_OUT)
    d.line([a, b], fill=fill, width=w)
    r = w / 2
    for q in (a, b):
        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=fill)

def render(p):
    img = Image.new('P', CANVAS, 0)
    if p.get('hide'):
        return img, skeleton(p)
    d = ImageDraw.Draw(img)
    S = skeleton(p)
    # chi sau
    _seg(d, S['sh'], S['bel'], W_UARM, C_MAIN_D); _seg(d, S['bel'], S['bha'], W_FARM, C_MAIN_D)
    _seg(d, S['hip'], S['bkn'], W_THIGH, C_MAIN_D); _seg(d, S['bkn'], S['ban'], W_SHIN, C_MAIN_D)
    _seg(d, S['ban'], S['bft'], W_FOOT, C_ACC_D)
    # than + dai lung
    _seg(d, S['hip'], S['neck'], W_TORSO, C_MAIN)
    bx, by = S['hip']
    d.line([(bx - 4, by - 2), (bx + 4, by - 2)], fill=C_ACC, width=2)
    # chan truoc
    _seg(d, S['hip'], S['fkn'], W_THIGH, C_MAIN); _seg(d, S['fkn'], S['fan'], W_SHIN, C_MAIN)
    _seg(d, S['fan'], S['fft'], W_FOOT, C_ACC)
    # dau + kinh mat (huong mat)
    hx, hy = S['head']
    d.ellipse([hx - HEAD_R - 1, hy - HEAD_R - 1, hx + HEAD_R + 1, hy + HEAD_R + 1], fill=C_OUT)
    d.ellipse([hx - HEAD_R, hy - HEAD_R, hx + HEAD_R, hy + HEAD_R], fill=C_HEAD)
    d.rectangle([hx + 1, hy - 2, hx + HEAD_R, hy + 1], fill=C_EYE)
    d.line([(hx - HEAD_R + 1, hy + 2), (hx - 2, hy + 4)], fill=C_HEAD_D, width=1)
    # tay truoc
    _seg(d, S['sh'], S['fel'], W_UARM, C_MAIN); _seg(d, S['fel'], S['fha'], W_FARM, C_MAIN)
    q = S['fha']
    d.ellipse([q[0] - 2.5, q[1] - 2.5, q[0] + 2.5, q[1] + 2.5], fill=C_OUT)
    d.ellipse([q[0] - 1.5, q[1] - 1.5, q[0] + 1.5, q[1] + 1.5], fill=C_ACC)
    return img, S

def body_box(img):
    """Clsn2 tu dong: khung bao phan than (toa do so voi axis)."""
    bb = img.getbbox()
    if not bb:
        return None
    x0, y0, x1, y1 = bb
    return [x0 - AXIS[0] + 3, y0 - AXIS[1] + 2, x1 - AXIS[0] - 3, y1 - AXIS[1]]

def tip_box(S, part, w=14, h=12):
    """Clsn1 quanh dau tay/chan: part = 'fha','bha','fft','bft','fkn'... (w, h tinh theo ti le 1.0)"""
    x, y = S[part]
    x, y = x - AXIS[0], y - AXIS[1]
    w, h = w * SCALE, h * SCALE
    return [int(x - w / 2 + 2), int(y - h / 2), int(x + w / 2 + 2), int(y + h / 2)]

def sbox(b):
    """Doi hop toa do viet o ti le 1.0 sang ti le hien tai."""
    return [int(round(v * SCALE)) for v in b]

def make_palette(main, acc, head=(230, 220, 200), eye=(60, 230, 255)):
    def shade(c, k):
        return tuple(max(0, min(255, int(v * k))) for v in c)
    cols = [(0, 0, 0)] * 256
    cols[C_OUT] = (24, 22, 30)
    cols[C_MAIN] = main
    cols[C_MAIN_D] = shade(main, 0.62)
    cols[C_ACC] = acc
    cols[C_ACC_D] = shade(acc, 0.62)
    cols[C_HEAD] = head
    cols[C_HEAD_D] = shade(head, 0.7)
    cols[C_EYE] = eye
    return cols
