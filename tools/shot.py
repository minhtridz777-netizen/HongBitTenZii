"""Chay IKEMEN voi tham so, chup man hinh cua so game sau vai giay, roi tat.
python shot.py <out_prefix> <delay1,delay2,...> -- <ikemen args...>"""
import os, sys, time, subprocess, ctypes, ctypes.wintypes as wt
from PIL import ImageGrab

out = sys.argv[1]
delays = [float(x) for x in sys.argv[2].split(',')]
args = sys.argv[sys.argv.index('--') + 1:]
p = subprocess.Popen([os.path.abspath('Ikemen_GO.exe')] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
user32 = ctypes.windll.user32
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

def find_window(pid):
    res = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(h, l):
        wpid = wt.DWORD()
        user32.GetWindowThreadProcessId(h, ctypes.byref(wpid))
        if wpid.value == pid and user32.IsWindowVisible(h):
            res.append(h)
        return True
    user32.EnumWindows(cb, 0)
    return res[0] if res else None

def capture(h):
    """Chup noi dung cua so (ke ca khi bi che) bang PrintWindow PW_RENDERFULLCONTENT."""
    from PIL import Image
    gdi32 = ctypes.windll.gdi32
    r = wt.RECT()
    user32.GetClientRect(h, ctypes.byref(r))
    w, hh = r.right, r.bottom
    hdc = user32.GetDC(h)
    mdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, hh)
    gdi32.SelectObject(mdc, bmp)
    user32.PrintWindow(h, mdc, 3)  # PW_CLIENTONLY | PW_RENDERFULLCONTENT
    class BIH(ctypes.Structure):
        _fields_ = [('biSize', wt.DWORD), ('biWidth', ctypes.c_long), ('biHeight', ctypes.c_long),
                    ('biPlanes', wt.WORD), ('biBitCount', wt.WORD), ('biCompression', wt.DWORD),
                    ('biSizeImage', wt.DWORD), ('biXPelsPerMeter', ctypes.c_long), ('biYPelsPerMeter', ctypes.c_long),
                    ('biClrUsed', wt.DWORD), ('biClrImportant', wt.DWORD)]
    bih = BIH(ctypes.sizeof(BIH), w, -hh, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * hh * 4)
    gdi32.GetDIBits(mdc, bmp, 0, hh, buf, ctypes.byref(bih), 0)
    gdi32.DeleteObject(bmp); gdi32.DeleteDC(mdc); user32.ReleaseDC(h, hdc)
    return Image.frombuffer('RGB', (w, hh), buf, 'raw', 'BGRX', 0, 1)

KEYS = [(float(a), b) for a, b in (k.split(':') for k in os.environ.get('SHOT_KEYS', '').split(',') if k)]
VK = {'J': (0x4A, 0x24), 'ENTER': (0x0D, 0x1C), 'ESC': (0x1B, 0x01)}
def press(h, name):
    vk, sc = VK[name]
    user32.PostMessageW(h, 0x0100, vk, 1 | (sc << 16))
    time.sleep(0.12)
    user32.PostMessageW(h, 0x0101, vk, 1 | (sc << 16) | (3 << 30))

t0 = time.time()
events = sorted([(d, 'shot', i) for i, d in enumerate(delays)] + [(d, 'key', k) for d, k in KEYS])
for d, kind, arg in events:
    while time.time() - t0 < d:
        time.sleep(0.05)
    if kind == 'key':
        h = find_window(p.pid)
        if h: press(h, arg); print('key', arg, 'at', d)
        continue
    i = arg
    while time.time() - t0 < d:
        time.sleep(0.05)
    if p.poll() is not None:
        print('process exited early', p.returncode)
        break
    h = find_window(p.pid)
    if not h:
        print('no window'); continue
    img = capture(h)
    img.save('%s_%d.png' % (out, i))
    print('saved', '%s_%d.png' % (out, i), img.size)
if p.poll() is None:
    p.kill()
outp = p.communicate()[0].decode('utf-8', 'replace')
print('--- output ---')
print('\n'.join(l for l in outp.splitlines() if not l.startswith(('\t', 'goroutine', 'runtime'))))
