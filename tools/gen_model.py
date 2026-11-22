"""Sinh MODEL TEST cho mot nhan vat: <thu muc>/<ten>.sff + <ten>.air
Chay: python tools/gen_model.py <thu muc nhan vat> <ten file> <mau chinh R,G,B> <mau phu R,G,B> [--no-moves]
  vd: python tools/gen_model.py shared/char_template mau 150,155,170 220,70,60
  --no-moves: chi anim chung (dung cho Bu Nhin).
Tat ca so anim theo KHUNG_CHUAN.md. In ra elem co Clsn1 cua tung anim de dung trong AnimElem.
"""
import os, sys, io, math, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from puppet import P, lerp, render, body_box, tip_box, make_palette, AXIS
from sff2 import read_sff, write_sff

out_dir, name = sys.argv[1], sys.argv[2]
main_c = tuple(int(v) for v in sys.argv[3].split(','))
acc_c = tuple(int(v) for v in sys.argv[4].split(','))
WITH_MOVES = '--no-moves' not in sys.argv

ANIMS = []   # (no, frames, loop, comment) ; frame = (pose, time, opts)

def A(no, frames, loop=None, comment=''):
    ANIMS.append((no, frames, loop, comment))

def F(p, t, **o):
    return (p, t, o)

def tween(p0, p1, n, t, **o):
    return [F(lerp(p0, p1, (i + 1) / n), t, **o) for i in range(n)]

def ik(x, y=-2):
    return ('ik', x, y)

# ============================ TU THE CO BAN ============================
STAND = P()
STAND2 = P(y=3, fa=(22, 55), ba=(-13, 45))
CROUCH = P(y=14, t=18, fa=(40, 70), ba=(10, 70), fl=ik(9), bl=ik(-9))
JUMP_UP = P(y=-6, t=0, fa=(60, 70), ba=(-30, 90), fl=(60, 90), bl=(10, 70))
JUMP_FALL = P(y=-4, t=-4, fa=(80, 30), ba=(-50, 40), fl=(30, 40), bl=(-10, 30))
JUMP_FWD = P(y=-6, t=12, fa=(70, 60), ba=(-40, 70), fl=(70, 100), bl=(30, 110))
JUMP_BACK = P(y=-6, t=-12, fa=(30, 60), ba=(-60, 50), fl=(40, 80), bl=(0, 60))
GUARD = P(y=5, t=2, fa=(55, 115), ba=(70, 110), fl=ik(9), bl=ik(-10))
GUARD_HIT = P(x=-3, y=6, t=-6, fa=(50, 120), ba=(65, 115), fl=ik(6), bl=ik(-12))
HIT1 = P(x=-2, t=-14, fa=(-10, 30), ba=(-40, 30), fl=ik(9), bl=ik(-10))
HIT2 = P(x=-4, t=-24, fa=(-30, 20), ba=(-60, 20), fl=ik(10), bl=ik(-12))
HITLOW = P(y=6, t=30, fa=(30, 20), ba=(10, 20), fl=ik(8), bl=ik(-10))
CHIT = P(y=14, t=-5, fa=(10, 40), ba=(-20, 40), fl=ik(9), bl=ik(-9))
AIRHIT = P(y=-6, t=-35, fa=(-40, 20), ba=(-80, 20), fl=(50, 20), bl=(20, 30))
FALL = P(y=-6, t=-60, fa=(-70, 10), ba=(-110, 10), fl=(70, 10), bl=(45, 20))
TRIP = P(y=-4, t=50, fa=(120, 10), ba=(90, 10), fl=(-20, 10), bl=(-40, 10))
LIE = P(y=27, t=-88, fa=(-160, 0), ba=(-140, 0), fl=(92, 0), bl=(88, 5))
LIE_FACE = P(y=27, t=88, fa=(160, 0), ba=(140, 0), fl=(-92, 0), bl=(-88, 5))
BOUNCE = P(y=10, t=-70, fa=(-100, 10), ba=(-130, 10), fl=(80, 10), bl=(60, 20))
GETUP1 = P(y=20, t=-40, fa=(-60, 40), ba=(-90, 20), fl=(70, 60), bl=(40, 90))
WIN = P(t=-2, fa=(175, 5), ba=(-20, 40))
LOSE = P(y=8, t=30, fa=(5, 10), ba=(-5, 10), fl=ik(8), bl=ik(-8))
DIZZY = P(y=4, t=-8, fa=(-5, 10), ba=(5, 10))

def walk(k, back=False):
    s = math.sin(2 * math.pi * k / 6)
    c = abs(math.cos(2 * math.pi * k / 6))
    return P(y=2 + c * 1.5, t=6 if not back else -2,
             fa=(20 - 18 * s, 50), ba=(-15 + 18 * s, 40),
             fl=ik(3 + 11 * s, -2 - 3 * max(0, -s)), bl=ik(-3 - 11 * s, -2 - 3 * max(0, s)))

# ============================ ANIM CHUNG (0-199, 5000+) ============================
A(0, [F(STAND, 30), F(STAND2, 30)], loop=0, comment='Dung')
A(5, [F(P(t=0, fa=(0, 30), ba=(0, 30)), 4)], comment='Quay mat')
A(6, [F(lerp(CROUCH, P(t=0), 0.3), 4)], comment='Quay mat khi ngoi')
A(10, tween(STAND, CROUCH, 2, 2), comment='Dung -> ngoi')
A(11, [F(CROUCH, -1)], comment='Ngoi')
A(12, tween(CROUCH, STAND, 2, 2), comment='Ngoi -> dung')
A(20, [F(walk(k), 4) for k in range(6)], loop=0, comment='Di toi')
A(21, [F(walk(k, True), 4) for k in reversed(range(6))], loop=0, comment='Di lui')
A(40, [F(lerp(STAND, CROUCH, 0.5), 3)], comment='Bat dau nhay')
A(41, tween(lerp(STAND, CROUCH, .5), JUMP_UP, 2, 3) + [F(JUMP_UP, 12), F(JUMP_FALL, -1)], comment='Nhay thang')
A(42, tween(lerp(STAND, CROUCH, .5), JUMP_FWD, 2, 3) + [F(JUMP_FWD, 12), F(JUMP_FALL, -1)], comment='Nhay toi')
A(43, tween(lerp(STAND, CROUCH, .5), JUMP_BACK, 2, 3) + [F(JUMP_BACK, 12), F(JUMP_FALL, -1)], comment='Nhay lui')
A(44, [F(JUMP_FALL, -1)], comment='Roi')
A(47, [F(lerp(STAND, CROUCH, 0.6), 3)], comment='Tiep dat')
A(100, [F(P(t=28, fa=(-40, 60), ba=(60, 60), fl=ik(12), bl=ik(-14, -6)), 3), F(P(t=28, fa=(40, 60), ba=(-40, 60), fl=ik(-6, -6), bl=ik(10)), 3)], loop=0, comment='Chay (=luot)')
A(105, [F(P(y=-4, t=-14, fa=(30, 60), ba=(-50, 50), fl=(30, 60), bl=(-10, 40)), -1)], comment='Nhay lui ngan')
for n in (120, 130):
    A(n, [F(GUARD, -1 if n == 130 else 3)], comment='Do (dung)')
for n in (121, 131):  # game khong co cui: do ngoi = do dung
    A(n, [F(GUARD, -1 if n == 131 else 3)], comment='Do (ngoi) = do dung')
for n in (122, 132):
    A(n, [F(P(y=-6, fa=(55, 115), ba=(70, 110), fl=(40, 60), bl=(0, 50)), -1 if n == 132 else 3)], comment='Do (tren khong)')
A(140, [F(lerp(GUARD, STAND, .5), 3)], comment='Thoi do')
A(141, [F(lerp(GUARD, STAND, .5), 3)], comment='Thoi do ngoi = dung')
A(142, [F(P(y=-6, fa=(40, 60), ba=(10, 60), fl=(40, 60), bl=(0, 50)), 3)], comment='Thoi do tren khong')
A(150, [F(GUARD_HIT, 3), F(GUARD, 6)], comment='Do trung don')
A(151, [F(GUARD_HIT, 3), F(GUARD, 6)], comment='Do ngoi trung don = dung')
A(152, [F(P(y=-6, fa=(50, 120), ba=(65, 115), fl=(40, 60), bl=(0, 50)), 9)], comment='Do tren khong trung don')
A(170, [F(LOSE, -1)], comment='Thua')
A(180, [F(WIN, -1)], comment='Thang')
A(181, tween(STAND, WIN, 3, 4) + [F(WIN, -1)], comment='Thang (gio tay)')
A(190, [F(P(t=-6, fa=(120, 60), ba=(-30, 30)), 30), F(lerp(STAND, WIN, .3), 20), F(STAND, 10)], comment='Xuat hien')
A(195, [F(P(fa=(150, 40), ba=(-15, 40)), 8), F(P(fa=(130, 70), ba=(-15, 40)), 8)] * 3, comment='Khieu khich')
# bi danh dung
for base, hp in ((5000, HIT1), (5010, HITLOW)):
    A(base, [F(hp, 6), F(lerp(hp, STAND, .5), 6)], comment='Bi danh nhe')
    A(base + 1, [F(lerp(hp, HIT2, .5), 8), F(lerp(hp, STAND, .5), 8)], comment='Bi danh vua')
    A(base + 2, [F(HIT2, 10), F(lerp(HIT2, STAND, .5), 10)], comment='Bi danh manh')
    for k in (5, 6, 7):
        A(base + k, [F(lerp(hp, STAND, .5), 4), F(STAND, 4)], comment='Hoi phuc')
A(5020, [F(CHIT, 6), F(CROUCH, 6)], comment='Ngoi bi danh nhe')
A(5021, [F(CHIT, 8), F(CROUCH, 8)], comment='Ngoi bi danh vua')
A(5022, [F(CHIT, 10), F(CROUCH, 10)], comment='Ngoi bi danh manh')
for k in (5025, 5026, 5027):
    A(k, [F(CROUCH, 4)], comment='Ngoi hoi phuc')
A(5030, [F(AIRHIT, -1)], comment='Bi danh tren khong')
A(5035, [F(lerp(AIRHIT, FALL, .5), 4)], comment='Chuyen sang roi')
A(5040, [F(AIRHIT, -1)], comment='Hoi phuc tren khong (khong nga)')
A(5050, [F(FALL, -1)], comment='Roi nga ngua')
A(5051, [F(lerp(FALL, BOUNCE, .5), -1)], comment='Roi nga (xuong)')
A(5060, [F(FALL, -1)], comment='Roi')
A(5061, [F(lerp(FALL, BOUNCE, .5), -1)], comment='Roi xuong')
A(5070, [F(TRIP, 6), F(lerp(TRIP, LIE_FACE, .5), -1)], comment='Bi quet nga')
A(5080, [F(BOUNCE, -1)], comment='Cham dat')
A(5090, [F(BOUNCE, -1)], comment='Cham dat')
A(5100, [F(BOUNCE, 4), F(lerp(BOUNCE, LIE, .5), 4)], comment='Dap dat')
A(5101, [F(lerp(BOUNCE, FALL, .4), -1)], comment='Nay len')
A(5110, [F(LIE, -1)], comment='Nam')
A(5120, [F(LIE, 4), F(GETUP1, 8), F(CROUCH, 8), F(lerp(CROUCH, STAND, .5), 6)], comment='Dung day')
A(5150, [F(LIE, -1)], comment='Nam (thua)')
A(5160, [F(lerp(LIE, BOUNCE, .3), 6), F(LIE, -1)], comment='Bi danh khi nam')
A(5170, [F(lerp(LIE, BOUNCE, .3), 6), F(LIE, -1)], comment='Bi danh khi nam')
A(5200, [F(CROUCH, 6), F(lerp(CROUCH, STAND, .5), 6)], comment='Tiep dat hoi phuc')
spin = [P(y=-8, t=a, fa=(60, 90), ba=(20, 100), fl=(80, 120), bl=(50, 120)) for a in (0, 90, 180, 270)]
A(5210, [F(s, 3) for s in spin] + [F(JUMP_FALL, -1)], comment='Lon hoi phuc tren khong')
A(5300, [F(DIZZY, 10), F(lerp(DIZZY, HIT1, .4), 10)], loop=0, comment='Choang')

# ============================ ANIM BO CHIEU MAU ============================
PUNCH_F = P(t=10, fa=(88, 4), ba=(-20, 80), fl=ik(12), bl=ik(-10))
PUNCH_B = P(t=14, fa=(30, 90), ba=(86, 4), fl=ik(12), bl=ik(-12))
CHAMBER = P(t=-2, fa=(20, 110), ba=(-25, 90), fl=ik(7), bl=ik(-9))
KICK = P(t=-14, fa=(40, 70), ba=(-30, 60), fl=(88, 0), bl=ik(-6))
UPPER0 = P(y=8, t=10, fa=(40, 130), ba=(-20, 80), fl=ik(9), bl=ik(-11))
UPPER1 = P(y=-2, t=-8, fa=(172, 4), ba=(-30, 60), fl=ik(7), bl=ik(-10))
SWEEP = P(y=16, t=26, fa=(50, 40), ba=(10, 60), fl=(92, 0), bl=ik(-6))
AIRKICK = P(y=-6, t=-10, fa=(60, 70), ba=(-30, 60), fl=(60, 0), bl=(10, 70))
AIRPUNCH = P(y=-6, t=14, fa=(100, 4), ba=(-30, 70), fl=(50, 80), bl=(10, 70))
DASH = P(t=30, fa=(-50, 40), ba=(-70, 40), fl=ik(14, -4), bl=ik(-16, -6))
BDASH = P(y=-6, t=-18, fa=(30, 60), ba=(-50, 50), fl=(30, 60), bl=(-10, 40))
ADASH = P(y=-8, t=62, fa=(-80, 10), ba=(-95, 10), fl=(-110, 10), bl=(-120, 15))
DJUMP = P(y=-8, t=-6, fa=(150, 20), ba=(130, 20), fl=(50, 110), bl=(20, 110))
PUSH = P(t=8, fa=(86, 0), ba=(80, 0), fl=ik(12), bl=ik(-12))
CHARGE = P(y=6, t=-4, fa=(-60, 100), ba=(-70, 100), fl=ik(12), bl=ik(-12))
DIVE = P(y=-4, t=-34, fa=(40, 80), ba=(-30, 60), fl=(55, 0), bl=(0, 80))
SLAM = P(y=-6, t=30, fa=(120, 10), ba=(110, 10), fl=(40, 80), bl=(0, 80))
SLAM0 = P(y=-8, t=-10, fa=(200, 10), ba=(190, 10), fl=(40, 80), bl=(0, 80))

if WITH_MOVES:
    A(200, [F(CHAMBER, 2), F(PUNCH_F, 3, c1='fha'), F(PUNCH_F, 2), F(lerp(PUNCH_F, STAND, .5), 4)], comment='J1 - dam tay truoc')
    A(210, [F(CHAMBER, 3), F(PUNCH_B, 3, c1='bha'), F(PUNCH_B, 3), F(lerp(PUNCH_B, STAND, .5), 5)], comment='J2 - dam tay sau')
    A(220, [F(lerp(STAND, KICK, .4), 3), F(KICK, 4, c1='fft'), F(KICK, 3), F(lerp(KICK, STAND, .5), 6)], comment='J3 - da day lui')
    A(240, [F(UPPER0, 3), F(lerp(UPPER0, UPPER1, .5), 2, c1='fha'), F(UPPER1, 4, c1='fha'), F(UPPER1, 4), F(lerp(UPPER1, STAND, .5), 6)], comment='W+J - moc hat len')
    A(400, [F(lerp(STAND, SWEEP, .5), 3), F(SWEEP, 4, c1='fft'), F(SWEEP, 4), F(lerp(SWEEP, CROUCH, .5), 6)], comment='S+J - quet chan')
    A(600, [F(lerp(JUMP_FALL, AIRKICK, .5), 2), F(AIRKICK, 6, c1='fft'), F(AIRKICK, -1)], comment='J tren khong - da cheo')
    A(610, [F(lerp(JUMP_FALL, AIRPUNCH, .5), 2), F(AIRPUNCH, 5, c1='fha'), F(AIRPUNCH, -1)], comment='J tren khong lan 2 - dam')
    A(700, [F(DASH, 3), F(lerp(DASH, P(t=30, fa=(-40, 40), ba=(-60, 40), fl=ik(-4, -6), bl=ik(10)), 1), 3)], loop=0, comment='Luot toi')
    A(705, [F(BDASH, -1)], comment='Luot lui')
    A(710, [F(ADASH, -1)], comment='Luot tren khong')
    A(720, [F(DJUMP, 4)] + [F(s, 3) for s in spin[1:]] + [F(JUMP_FALL, -1)], comment='Nhay doi')
    A(800, [F(GUARD, -1)], comment='Giu S - the do')
    A(860, [F(P(hide=True), 1)] * 1, comment='Thoat combo - bien mat')
    A(865, [F(CROUCH, 4), F(lerp(CROUCH, STAND, .5), 4)], comment='Thoat combo - hien ra')
    A(1000, [F(CHARGE, 6), F(PUSH, 4), F(PUSH, 10), F(lerp(PUSH, STAND, .5), 6)], comment='U - phong cau nang luong (dan o 8100)')
    A(1100, [F(lerp(STAND, DASH, .5), 3), F(DASH, 6), F(PUNCH_F, 4, c1='fha', big=True), F(PUNCH_F, 4), F(lerp(PUNCH_F, STAND, .5), 6)], comment='S+U - luot chem dat')
    A(1200, [F(UPPER0, 3), F(UPPER1, 4, c1='fha', big=True), F(UPPER1, 6, c1='fha', big=True), F(JUMP_FALL, -1)], comment='W+U - moc bay len')
    A(1300, [F(lerp(JUMP_FALL, DIVE, .5), 3), F(DIVE, -1, c1='fft', big=True)], comment='U tren khong - lao xuong')
    A(1305, [F(lerp(STAND, CROUCH, .6), 6)], comment='U tren khong - tiep dat')
    # Tuyet chieu
    flurry = []
    for i in range(8):
        flurry += [F(CHAMBER, 1), F(PUNCH_F if i % 2 == 0 else PUNCH_B, 3, c1='fha' if i % 2 == 0 else 'bha', big=True)]
    A(3000, [F(CHARGE, 8)] + flurry + [F(UPPER0, 3), F(UPPER1, 4, c1='fha', big=True), F(UPPER1, 10), F(lerp(UPPER1, STAND, .5), 6)],
      comment='I - dam lien hoan 8 nhat + moc hat len')
    A(3500, [F(CHARGE, 20)], comment='W+I - tu luc')
    A(3510, [F(PUSH, 3, box=[20, -48, 330, -22])] * 1 + [F(lerp(PUSH, P(t=10, fa=(84, 0), ba=(78, 0), fl=ik(12), bl=ik(-12)), .5), 3, box=[20, -48, 330, -22])],
      loop=0, comment='W+I - ban tia (Clsn1 dai 310px)')
    A(3520, [F(lerp(PUSH, STAND, .5), 8)], comment='W+I - thu tay')
    A(4000, [F(lerp(STAND, DASH, .5), 3)] + [F(DASH, 3, box=[-5, -60, 30, -10])] * 1 + [F(lerp(DASH, PUNCH_F, .5), 3, box=[-5, -60, 30, -10])],
      loop=1, comment='S+I buoc 1 - lao toi')
    A(4010, [F(AIRPUNCH, 3, box=[-10, -60, 40, -10]), F(P(y=-6, t=10, fa=(30, 90), ba=(95, 4), fl=(50, 80), bl=(10, 70)), 3, box=[-10, -60, 40, -10])],
      loop=0, comment='S+I buoc 2 - dam lien hoan tren khong')
    A(4020, [F(SLAM0, 8), F(SLAM, 4, c1='fha', big=True), F(SLAM, -1)], comment='S+I buoc 3 - dap xuong')
    A(4030, [F(lerp(STAND, CROUCH, .6), 10), F(lerp(CROUCH, WIN, .4), 10), F(STAND, 6)], comment='S+I ket thuc')

# ============================ VE + DONG GOI ============================
pal_char = make_palette(main_c, acc_c)
ALT = [(main_c, acc_c), ((200, 60, 60), (240, 200, 60)), ((60, 90, 200), (240, 240, 240)),
       ((60, 160, 80), (230, 160, 40)), ((230, 200, 70), (60, 60, 70)), ((140, 70, 180), (90, 230, 220))]

sprites, info, air = [], [], []
air.append('; MODEL TEST - sinh bang tools/gen_model.py (khong sua tay)\n')
air.append('; So anim theo designs/KHUNG_CHUAN.md. Clsn2 tu dong theo than, Clsn1 theo tay/chan ra don.\n\n')
for no, frames, loop, comment in ANIMS:
    hits = []
    air.append('; %s\n[Begin Action %d]\n' % (comment, no))
    for i, (pose, t, o) in enumerate(frames):
        if loop is not None and i == loop:
            air.append('Loopstart\n')
        img, S = render(pose)
        sprites.append(dict(g=no, n=i, img=img))
        c2 = body_box(img)
        if c2:
            air.append('Clsn2: 1\n Clsn2[0] = %d, %d, %d, %d\n' % tuple(c2))
        c1 = None
        if 'c1' in o:
            c1 = tip_box(S, o['c1'], 22 if o.get('big') else 14, 18 if o.get('big') else 12)
        if 'box' in o:
            c1 = o['box']
        if c1:
            air.append('Clsn1: 1\n Clsn1[0] = %d, %d, %d, %d\n' % tuple(c1))
            hits.append(i + 1)
        air.append('%d,%d, 0,0, %d\n' % (no, i, t))
    air.append('\n')
    info.append((no, comment, hits, sum(max(0, f[1]) for f in frames)))

# ---- Anh dai dien: 9000,0 (nho, mat) va 9000,1 (lon, ca nguoi) ----
_im, _S = render(STAND)
hx, hy = int(_S['head'][0]), int(_S['head'][1])
face = _im.crop((hx - 12, hy - 11, hx + 12, hy + 13)).resize((72, 72), Image.NEAREST)
sprites.append(dict(g=9000, n=0, img=face, ax=(0, 0), portrait=True))
full = _im.crop((24, 20, 88, 104)).resize((192, 252), Image.NEAREST)
sprites.append(dict(g=9000, n=1, img=full, ax=(0, 0), portrait=True))

# ---- Hieu ung (nhom 8000+, bang mau rieng 8000,1, ve de dung trans = add) ----
FXPAL = [(0, 0, 0)] + [(int(20 + 60 * k), int(60 + 180 * k), int(140 + 115 * k)) for k in (i / 254 for i in range(255))]
FXPAL = [(0, 0, 0)] + [tuple(min(255, int(c + (255 - c) * max(0, (k - .6) / .4))) for c in FXPAL[i + 1])
                       for i, k in enumerate(i / 254 for i in range(255))]

def fx_img(w, h, drawfn):
    m = Image.new('L', (w * 4, h * 4), 0)
    drawfn(ImageDraw.Draw(m), w * 4, h * 4)
    m = m.resize((w, h), Image.LANCZOS)
    out = Image.new('P', (w, h), 0)
    out.putdata([0 if v < 10 else max(1, min(255, v)) for v in m.getdata()])
    return out

def arc(fr):
    def f(d, W, H):
        k = [0.5, 1, 1, 1][fr]; b = [255, 255, 170, 90][fr]; th = [10, 10, 7, 4][fr] * 4
        for i in range(30):
            u = i / 29
            if u > k: break
            a = math.radians(200 + 140 * u)
            x, y = W / 2 + math.cos(a) * W * .42, H * .75 + math.sin(a) * H * .62
            r = th * math.sin(math.pi * u) + 2
            d.ellipse([x - r, y - r, x + r, y + r], fill=int(b * (0.5 + 0.5 * u)))
    return fx_img(64, 40, f)

def burst(fr):
    def f(d, W, H):
        r = [8, 14, 18][fr] * 4; b = [255, 220, 120][fr]
        for a in range(0, 360, 45):
            x, y = W / 2 + math.cos(math.radians(a)) * r, H / 2 + math.sin(math.radians(a)) * r
            d.line([(W / 2, H / 2), (x, y)], fill=b, width=[10, 8, 5][fr])
        d.ellipse([W / 2 - r / 3, H / 2 - r / 3, W / 2 + r / 3, H / 2 + r / 3], fill=b)
    return fx_img(48, 48, f)

def dust(fr):
    def f(d, W, H):
        b = [200, 140, 80][fr]
        for i, (x, y, r) in enumerate([(.3, .7, .2), (.55, .6, .25), (.75, .72, .18)]):
            rr = (r + fr * .06) * W
            d.ellipse([x * W - rr, y * H - rr, x * W + rr, y * H + rr], fill=b)
    return fx_img(32, 20, f)

def ball(fr):
    def f(d, W, H):
        for i, (r, b) in enumerate([(.48, 90), (.36, 170), (.22, 255)]):
            rr = (r + (0.04 if fr else 0)) * W
            d.ellipse([W / 2 - rr, H / 2 - rr, W / 2 + rr, H / 2 + rr], fill=b)
    return fx_img(24, 24, f)

def beam(fr):
    def f(d, W, H):
        for r, b in ((.5, 90), (.32, 170), (.14, 255)):
            hh = H * (r + (0.05 if fr else 0))
            d.rectangle([0, H / 2 - hh, W, H / 2 + hh], fill=b)
    return fx_img(310, 26, f)

def smoke(fr):
    def f(d, W, H):
        b = [255, 200, 140, 70][fr]; r = [.2, .32, .42, .48][fr]
        d.ellipse([W * (.5 - r), H * (.5 - r), W * (.5 + r), H * (.5 + r)], outline=b, width=int(W * .08))
    return fx_img(48, 64, f)

def flash(fr):
    def f(d, W, H):
        r = [.2, .45, .3][fr]; b = [255, 200, 120][fr]
        d.ellipse([W * (.5 - r), H * (.5 - r), W * (.5 + r), H * (.5 + r)], fill=b)
    return fx_img(64, 64, f)

FX = {8000: [arc(i) for i in range(4)], 8010: [burst(i) for i in range(3)], 8020: [dust(i) for i in range(3)],
      8100: [ball(i) for i in range(2)], 8110: [burst(i) for i in range(3)], 8200: [beam(i) for i in range(2)],
      8300: [smoke(i) for i in range(4)], 8400: [flash(i) for i in range(3)]}
FX_T = {8000: [2, 2, 2, 2], 8010: [2, 3, 3], 8020: [3, 3, 3], 8100: [3, 3], 8110: [2, 3, 3], 8200: [2, 2], 8300: [2, 3, 3, 3], 8400: [2, 3, 3]}
FX_NAME = {8000: 'Vet chem', 8010: 'Tia va cham', 8020: 'Bui luot', 8100: 'Cau nang luong (loop)', 8110: 'Cau no',
           8200: 'Tia laser (loop)', 8300: 'Khoi bien mat', 8400: 'Chop tu luc'}
FX_AX = {8200: (0, 13)}
air.append(';=================== HIEU UNG (8000-8999) ===================\n')
for g, frames in FX.items():
    if not WITH_MOVES and g not in (8010,):
        continue
    air.append('; %s\n[Begin Action %d]\n' % (FX_NAME[g], g))
    if g in (8100, 8200):
        air.append('Loopstart\n')
    for i, im in enumerate(frames):
        sprites.append(dict(g=g, n=i, img=im, fx=True, ax=FX_AX.get(g)))
        air.append('%d,%d, 0,0, %d\n' % (g, i, FX_T[g][i]))
    air.append('\n')

# ---- SFF ----
base = read_sff('chars/kfm/kfm.sff')
sff = dict(header=base['header'], sprites=[], pals=[])
for i, (m, a) in enumerate(ALT):
    cols = make_palette(m, a)
    sff['pals'].append(dict(g=1, n=i + 1, ncol=256, link=0,
                            data=b''.join(bytes((r, g_, b, 0 if j == 0 else 255)) for j, (r, g_, b) in enumerate(cols))))
fx_pal = len(sff['pals'])
sff['pals'].append(dict(g=8000, n=1, ncol=256, link=0,
                        data=b''.join(bytes((r, g_, b, 0 if j == 0 else 255)) for j, (r, g_, b) in enumerate(FXPAL))))
flat_char = [c for rgb in pal_char for c in rgb]
flat_fx = [c for rgb in FXPAL for c in rgb]
for s in sprites:
    im = s['img']
    im.putpalette(flat_fx if s.get('fx') else flat_char)
    buf = io.BytesIO()
    im.save(buf, format='PNG', optimize=True)
    if s.get('fx'):
        ax = s['ax'] or (im.width // 2, im.height // 2)
    elif s.get('portrait'):
        ax = s['ax']
    else:
        ax = AXIS
    sff['sprites'].append(dict(g=s['g'], n=s['n'], w=im.width, h=im.height, ax=ax[0], ay=ax[1], link=0, fmt=10, depth=8,
                               data=struct.pack('<I', im.width * im.height) + buf.getvalue(),
                               pal=fx_pal if s.get('fx') else 0, flags=0))
os.makedirs(out_dir, exist_ok=True)
write_sff(os.path.join(out_dir, name + '.sff'), sff)
open(os.path.join(out_dir, name + '.air'), 'w', encoding='utf-8', newline='\r\n').write(''.join(air))
print('sprites %d, anims %d' % (len(sprites), len(ANIMS)))
for no, comment, hits, tt in info:
    if hits:
        print(no, 'Clsn1 elem', hits, 'tong', tt, '|', comment)
