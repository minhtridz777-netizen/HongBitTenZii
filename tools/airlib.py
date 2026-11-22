"""Doc/ghi file .air cua Mugen: parse thanh danh sach frame co Clsn tuong minh."""
import re

def parse_air(path):
    text = open(path, encoding='utf-8-sig', errors='replace').read()
    actions = {}   # no -> dict(raw=str, frames=[...])
    cur = None
    raw_lines = []
    def finish():
        if cur is not None:
            actions[cur['no']]['raw'] = ''.join(raw_lines)
    pending = None  # ('clsn1'|'clsn2', default?, count, boxes)
    for line in text.splitlines(keepends=True):
        s = line.split(';')[0].strip()
        m = re.match(r'\[\s*Begin\s+Action\s+(-?\d+)\s*\]', s, re.I)
        if m:
            finish()
            no = int(m.group(1))
            cur = dict(no=no, frames=[], d1=[], d2=[], n1=None, n2=None, loop=None)
            actions[no] = cur
            raw_lines = [line]
            continue
        if cur is None:
            continue
        raw_lines.append(line)
        if not s:
            continue
        m = re.match(r'Clsn([12])(Default)?\s*:\s*(\d+)', s, re.I)
        if m:
            kind, dflt = m.group(1), bool(m.group(2))
            box = []
            if kind == '1':
                if dflt: cur['d1'] = box
                else: cur['n1'] = box
            else:
                if dflt: cur['d2'] = box
                else: cur['n2'] = box
            pending = box
            continue
        m = re.match(r'Clsn[12]\s*\[\s*\d+\s*\]\s*=\s*(.*)', s, re.I)
        if m:
            pending.append([int(float(v)) for v in m.group(1).split(',')[:4]])
            continue
        if re.match(r'loopstart', s, re.I):
            cur['loop'] = len(cur['frames'])
            continue
        parts = [p.strip() for p in s.split(',')]
        if len(parts) >= 5 and re.match(r'-?\d+$', parts[0]):
            fr = dict(fields=parts,
                      c1=cur['n1'] if cur['n1'] is not None else list(cur['d1']),
                      c2=cur['n2'] if cur['n2'] is not None else list(cur['d2']))
            cur['frames'].append(fr)
            cur['n1'] = None
            cur['n2'] = None
    finish()
    return actions


def frame_copy(fr, time_mul=None, c1_extend=0, add_c1=None, time=None, no_c1=False):
    f = dict(fields=list(fr['fields']), c1=[list(b) for b in fr['c1']], c2=[list(b) for b in fr['c2']])
    t = int(f['fields'][4])
    if time is not None:
        f['fields'][4] = str(time)
    elif time_mul is not None and t > 0:
        f['fields'][4] = str(max(1, round(t * time_mul)))
    if no_c1:
        f['c1'] = []
    if c1_extend and f['c1']:
        for b in f['c1']:
            # keo dai canh xa nhat ve phia truoc
            if b[2] >= b[0]: b[2] += c1_extend
            else: b[0] += c1_extend
    if add_c1:
        f['c1'] = f['c1'] + [list(b) for b in add_c1]
    return f


def render(no, frames, comment='', loop=None):
    out = []
    if comment:
        out.append('; ' + comment + '\n')
    out.append('[Begin Action %d]\n' % no)
    for i, fr in enumerate(frames):
        if loop is not None and i == loop:
            out.append('Loopstart\n')
        if fr['c2']:
            out.append('Clsn2: %d\n' % len(fr['c2']))
            for j, b in enumerate(fr['c2']):
                out.append(' Clsn2[%d] = %d, %d, %d, %d\n' % (j, *b))
        if fr['c1']:
            out.append('Clsn1: %d\n' % len(fr['c1']))
            for j, b in enumerate(fr['c1']):
                out.append(' Clsn1[%d] = %d, %d, %d, %d\n' % (j, *b))
        out.append(', '.join(fr['fields']) + '\n')
    out.append('\n')
    return ''.join(out)


def summary(frames):
    """Tra ve (danh sach chi so elem co Clsn1 (1-based), tong thoi gian, thoi diem bat dau tung elem)."""
    hits, starts, t = [], [], 0
    for i, fr in enumerate(frames):
        starts.append(t)
        if fr['c1']:
            hits.append(i + 1)
        tt = int(fr['fields'][4])
        t += tt if tt > 0 else 0
    return hits, t, starts
