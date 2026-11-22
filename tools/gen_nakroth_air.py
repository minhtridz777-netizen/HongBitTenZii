"""Sinh chars/nakroth/nakroth.air tu kfm.air (hinh tam).
Chay: python gen_nakroth_air.py <kfm.air> <nakroth.air>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from airlib import parse_air, frame_copy, render, summary

src, dst = sys.argv[1], sys.argv[2]
A = parse_air(src)

def fr(no, a=None, b=None, **kw):
    """Lay frame tu action KFM `no`, elem a..b (1-based, bao gom)."""
    frames = A[no]['frames']
    a = 1 if a is None else a
    b = len(frames) if b is None else b
    return [frame_copy(f, **kw) for f in frames[a - 1:b]]

out = []
out.append('; NAKROTH - file animation (HINH TAM: muon sprite Kung Fu Man)\n')
out.append('; File nay duoc sinh tu kfm.air. So animation theo quy uoc trong CLAUDE.md,\n')
out.append('; khi co sprite that chi can thay noi dung tung [Begin Action], giu nguyen so.\n')
out.append('; Luu y: logic trong nakroth.cns dua vao SO THU TU elem co Clsn1 (ghi o tung anim).\n\n')

# ---- 1. Anim chung (0-199, do do, bi danh 5000+) copy nguyen tu KFM ----
common = [0, 5, 6, 10, 11, 12, 20, 21, 40, 41, 42, 43, 47, 100, 105,
          120, 121, 122, 130, 131, 132, 140, 141, 142, 150, 151, 152,
          170, 181, 190, 195]
common += sorted(n for n in A if n >= 5000)
out.append(';=================== ANIM CHUNG (copy KFM) ===================\n')
for n in common:
    out.append(A[n]['raw'].rstrip('\n') + '\n\n')

info = []
def add(no, frames, comment, loop=None):
    h, t, st = summary(frames)
    info.append((no, comment, h, t, len(frames)))
    out.append(render(no, frames, '%s | elem Clsn1: %s | tong %d tick' % (comment, h, t), loop))

FAST = 0.6  # noi tai Tham Phan: J nhanh hon (~+60% toc danh)

# Nguon hinh: chi dung dong tac dam/chuong/vay tay cua KFM (dang gan voi chem), BO het dong tac da.
J3 = fr(1200, time_mul=0.6)
out.append(';=================== DANH THUONG (200-699) ===================\n')
add(200, fr(200, c1_extend=10), 'J1 - chem ngang dao phai (src KFM 200)')
add(210, fr(210, c1_extend=10), 'J2 - chem ngang dao trai (src KFM 210)')
add(220, [frame_copy(f, c1_extend=10) for f in J3], 'J3 - chem cheo hai dao (src KFM 1200)')
add(230, fr(1100, time_mul=0.8), 'J4 - hai dao vay len (src KFM 1100)')
add(240, fr(410), 'W+J - vay dao hat tung (src KFM 410)')
add(250, fr(1010, c1_extend=40), 'J cuong hoa (sau S+U) - chem quet ngang tam xa (src KFM 1010)')
add(280, fr(200, time_mul=FAST, c1_extend=10), 'J1 ban nhanh (noi tai)')
add(281, fr(210, time_mul=FAST, c1_extend=10), 'J2 ban nhanh (noi tai)')
add(282, [frame_copy(f, time_mul=FAST, c1_extend=10) for f in J3], 'J3 ban nhanh (noi tai)')
add(283, fr(1100, time_mul=0.8 * FAST), 'J4 ban nhanh (noi tai)')
add(284, fr(410, time_mul=FAST), 'W+J ban nhanh (noi tai)')
add(400, fr(400, c1_extend=20), 'S+J - quet dao thap (src KFM 400)')
add(480, fr(400, time_mul=FAST, c1_extend=20), 'S+J ban nhanh (noi tai)')
add(600, fr(610, c1_extend=10), 'J tren khong - bo dao cheo xuong (src KFM 610)')
add(680, fr(610, time_mul=FAST, c1_extend=10), 'J tren khong ban nhanh (noi tai)')

out.append(';=================== LUOT (700-799) ===================\n')
add(700, fr(100, time_mul=0.6), 'Luot toi (src KFM 100)', loop=0)
add(705, fr(105), 'Luot lui (src KFM 105)')

out.append(';=================== CHIEU U (1000-1999) ===================\n')
add(1000, fr(1000, c1_extend=10), 'U lan 1 - Boi Tham Doan, lao toi hat tung (src KFM 1000)')
add(1010, fr(1000, time_mul=0.85, c1_extend=10), 'U lan 2 - lao toi (src KFM 1000)')
add(1015, fr(105), 'U lan 2 - giu A: luot lui thoat than (src KFM 105)')
add(1020, fr(610, c1_extend=15), 'U lan 2 tren khong - lao ngang (src KFM 610)')
add(1025, fr(43), 'U lan 2 tren khong - giu A: lui (src KFM 43)', loop=A[43]['loop'])
add(1100, fr(43), 'S+U - Nguon Con Rac Roi: lon nguoc (src KFM 43)', loop=A[43]['loop'])
add(1200, fr(1110), 'W+U - Boi Tham Doan cheo len (src KFM 1110)')
add(1300, fr(610, c1_extend=10), 'U tren khong - Boi Tham Doan cheo xuong (src KFM 610)')
add(1305, fr(47, time=6), 'U tren khong - tiep dat')

out.append(';=================== TUYET CHIEU (3000-4999) ===================\n')
# I: khoi dong 4 elem + 7 nhat chem xen ke 2 tay + nhat cuoi vay len hat tung
sup = fr(3000, 1, 4)
for i in range(7):
    if i % 2 == 0:
        sup += fr(200, 2, 2, time=1) + fr(200, 3, 3, time=3, c1_extend=25) + fr(200, 4, 4, time=2)
    else:
        sup += fr(210, 4, 4, time=1) + fr(210, 5, 5, time=3, c1_extend=15) + fr(210, 6, 6, time=2)
sup += fr(1100, 2, 11, c1_extend=15)
add(3000, sup, 'I - Guom Hanh Quyet: dung yen, 7 nhat + nhat cuoi hat tung')

body_box = [[-5, -85, 45, -15]]
add(4000, fr(1000, 1, 2) + fr(100, time=3, add_c1=body_box), 'S+I buoc 1 - Boi Tham Doan lao hat tung')
flurry = fr(610, 2, 2, time=2, no_c1=True) + fr(610, 3, 3, time=3, c1_extend=25, add_c1=[[-10, -90, 50, -10]]) + fr(610, 2, 2, time=1, no_c1=True)
add(4010, flurry, 'S+I buoc 2 - Guom Hanh Quyet tren khong (vong 6 tick, lap)', loop=0)
add(4020, fr(43), 'S+I buoc 3 - Nguon Con Rac Roi lon nguoc', loop=A[43]['loop'])
add(4030, fr(1010, c1_extend=70), 'S+I buoc 4 - chem quet ket thuc')

out.append(';=================== HIEU UNG VET CHEM (8000-8099, sprite tu ve) ===================\n')
def fx(no, n, times, comment):
    out.append('; %s\n[Begin Action %d]\n' % (comment, no))
    for i in range(n):
        out.append('%d,%d, 0,0, %d\n' % (no, i, times[i]))
    out.append('\n')
fx(8000, 4, [2, 3, 3, 3], 'Vet chem ngang')
fx(8010, 4, [2, 3, 3, 3], 'Vet chem cheo xuong')
fx(8020, 4, [2, 3, 3, 3], 'Vet vay len')
fx(8030, 4, [2, 4, 4, 4], 'Vet chem quet lon')
fx(8040, 4, [2, 2, 2, 2], 'Vet cheo phai (nhanh, cho tuyet chieu)')
fx(8045, 4, [2, 2, 2, 2], 'Vet cheo trai (nhanh, cho tuyet chieu)')
fx(8050, 3, [2, 3, 2], 'Loe dao (bao don thu 4)')
fx(8060, 3, [3, 3, 3], 'Vet luot')

open(dst, 'w', encoding='utf-8', newline='\r\n').write(''.join(out))
for i in info:
    print(i)
