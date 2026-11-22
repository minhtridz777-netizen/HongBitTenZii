"""Sinh nhan vat Bu Nhin (chars/bunhin) cho LAB tu sprite KFM, doi mau sang mau rom.
Chay: python tools/gen_bunhin.py
Tao: bunhin.sff (KFM doi mau), bunhin.air (chi anim chung), bunhin.snd (copy).
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sff2 import read_sff, write_sff
from airlib import parse_air

SRC = 'chars/kfm'
DST = 'chars/bunhin'
os.makedirs(DST, exist_ok=True)

# ---- Sprite: doi moi bang mau nhom 1 (palette nhan vat) sang tong rom/go ----
stops = [(0.0, (40, 22, 8)), (0.35, (120, 78, 30)), (0.7, (205, 165, 80)), (1.0, (250, 232, 170))]
def straw(l):
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if l <= b:
            k = (l - a) / (b - a)
            return tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3))
    return stops[-1][1]

sff = read_sff(os.path.join(SRC, 'kfm.sff'))
for p in sff['pals']:
    if p['g'] != 1 or not p['data']:
        continue
    d = bytearray(p['data'])
    for i in range(1, len(d) // 4):     # mau 0 = trong suot, giu nguyen
        r, g, b = d[i * 4], d[i * 4 + 1], d[i * 4 + 2]
        lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
        d[i * 4:i * 4 + 3] = bytes(straw(lum))
    p['data'] = bytes(d)
write_sff(os.path.join(DST, 'bunhin.sff'), sff)

# ---- Animation: chi giu anim chung (dung, di, nhay, do, bi danh...) ----
A = parse_air(os.path.join(SRC, 'kfm.air'))
keep = [n for n in A if n < 200 or n >= 5000]
with open(os.path.join(DST, 'bunhin.air'), 'w', encoding='utf-8', newline='\r\n') as f:
    f.write('; BU NHIN - anim chung copy tu KFM (khong co don danh)\n\n')
    for n in sorted(keep):
        f.write(A[n]['raw'].rstrip('\n') + '\n\n')

shutil.copyfile(os.path.join(SRC, 'kfm.snd'), os.path.join(DST, 'bunhin.snd'))
print('bunhin: %d sprite, %d anim' % (len(sff['sprites']), len(keep)))
