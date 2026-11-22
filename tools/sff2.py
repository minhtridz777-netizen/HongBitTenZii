"""Doc / ghi SFF v2 (Elecbyte) - du de copy sprite cu va them sprite PNG moi."""
import struct

def read_sff(path):
    d = open(path, 'rb').read()
    assert d[:12] == b'ElecbyteSpr\x00'
    ver = tuple(d[12:16])
    (spr_off, nspr, pal_off, npal, l_off, l_len, t_off, t_len) = struct.unpack_from('<8I', d, 36)
    sprites = []
    for i in range(nspr):
        g, n, w, h, ax, ay, link, fmt, depth, off, ln, pal, flags = struct.unpack_from(
            '<HHHHhhHBBIIHH', d, spr_off + i * 28)
        base = t_off if flags & 1 else l_off
        data = d[base + off: base + off + ln] if ln else b''
        sprites.append(dict(g=g, n=n, w=w, h=h, ax=ax, ay=ay, link=link, fmt=fmt,
                            depth=depth, data=data, pal=pal, flags=flags))
    pals = []
    for i in range(npal):
        g, n, ncol, link, off, ln = struct.unpack_from('<HHHHII', d, pal_off + i * 16)
        pals.append(dict(g=g, n=n, ncol=ncol, link=link, data=d[l_off + off: l_off + off + ln]))
    return dict(ver=ver, header=d[:512], sprites=sprites, pals=pals)


def write_sff(path, sff):
    sprites, pals = sff['sprites'], sff['pals']
    nspr, npal = len(sprites), len(pals)
    spr_off = 512
    pal_off = spr_off + nspr * 28
    l_off = pal_off + npal * 16
    ldata = bytearray()
    pal_nodes = bytearray()
    for p in pals:
        if p['link'] and not p['data']:
            off, ln = 0, 0
        else:
            off, ln = len(ldata), len(p['data'])
            ldata += p['data']
        pal_nodes += struct.pack('<HHHHII', p['g'], p['n'], p['ncol'], p['link'], off, ln)
    spr_nodes = bytearray()
    for s in sprites:
        if s['data']:
            off, ln = len(ldata), len(s['data'])
            ldata += s['data']
        else:
            off, ln = 0, 0
        spr_nodes += struct.pack('<HHHHhhHBBIIHH', s['g'], s['n'], s['w'], s['h'], s['ax'], s['ay'],
                                 s['link'], s['fmt'], s['depth'], off, ln, s['pal'], 0)
    hdr = bytearray(sff['header'])
    struct.pack_into('<8I', hdr, 36, spr_off, nspr, pal_off, npal, l_off, len(ldata), l_off + len(ldata), 0)
    open(path, 'wb').write(bytes(hdr) + spr_nodes + pal_nodes + ldata)
