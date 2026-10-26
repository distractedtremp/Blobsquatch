"""Cut the character art into site sprites with hand-drawn "line boil".

For each pose this writes img/sq/<key>-<n>.webp, n = 0..2. Each variant is the
same drawing pushed through a different smooth random displacement, so cycling
them a few times a second makes the outlines wobble like redrawn frames.

Sources (2026-10-26): the clean-meme set in art/candidates/clean-meme/, full-size
Canva downloads with a white background (see docs/ART_PIPELINE.md). Blobsquatch
and Barry are one drawing per pose; the scenery sheet is split into its pieces.

    pip install pillow numpy scipy
    python tools/boil.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'art', 'candidates', 'clean-meme')
OUT = os.path.join(ROOT, 'img', 'sq')
H = 640          # stored sprite height in px for the characters
AMP = 1.2        # boil strength in px at H (2.4 on the old thick-line art; the clean lines want less)
CELL = 22        # noise feature size in px at H
# key: (file, mirror). The site draws a pose by key; a missing key falls back to 'front'.
POSES = {
    'back': ('back.png', False),
    'backM': ('back.png', True),
    'look': ('look.png', False),
    'lookM': ('look.png', True),
    'front': ('front.png', False),
    'held': ('held.png', False),
    'danceA': ('dance.png', False),
    'danceB': ('dance.png', True),   # the other knee is a mirror; only the zipper pull swaps sides
    'squat': ('squat.png', False),
    'frozen': ('frozen.png', False),
    # Barry (the photographer). Site moods: squint/watch -> watch, aim/frenzy -> aim, elated, sleep.
    'barry-watch': ('barry-watch.png', False),
    'barry-aim': ('barry-aim.png', False),
    'barry-elated': ('barry-elated.png', False),
    'barry-sleep': ('barry-sleep.png', False),
}
HOLES = {'barry-sleep.png': 1500, 'scenery.png': 1500}   # files whose enclosed white is background
# The scenery sheet, split into connected pieces, named row by row, left to right. (name, stored height)
SCENERY_FILE = 'scenery.png'
SCENERY = [('pine1', 480), ('pine2', 480), ('pine3', 480), ('deadtree', 480),
           ('fern1', 240), ('fern2', 240), ('moon', 160), ('twig', 100),
           ('grass1', 110), ('grass2', 110), ('grass3', 110), ('chair', 260)]


def cutout(path, ground_line=False, holes=0):
    """Remove the flat white (or gray) background. Enclosed light areas (eyes, shirt) stay,
    unless holes > 0: then enclosed near-white patches bigger than that many px are cut too
    (the fern gaps and the chair frame on the sheet show background, not paint)."""
    im = Image.open(path).convert('RGB')
    a = np.array(im).astype(int)
    h = a.shape[0]
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    bg = (sat < 22) & (mx > 125)
    keep = bg
    if ground_line:  # the old gray-background art had a thin dark ground line to remove as well
        dark = (sat < 25) & (mx < 110)
        k = 9
        up = np.zeros_like(bg); up[k:] = bg[:-k]
        dn = np.zeros_like(bg); dn[:-k] = bg[k:]
        line = dark & up & dn
        line[:h - 200] = False
        keep = bg | line
    lab, _ = ndimage.label(keep)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(edge))
    if holes:
        white = (sat < 14) & (mx > 238)
        wl, n = ndimage.label(white & ~outside)
        sizes = ndimage.sum(np.ones_like(wl), wl, range(1, n + 1))
        big = [i + 1 for i, sz in enumerate(sizes) if sz > holes]
        outside = outside | np.isin(wl, big)
    alpha = Image.fromarray(((~outside) * 255).astype('uint8'))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(alpha)
    return im.crop(im.getbbox())


def boil(im, seed, amp=AMP):
    a = np.array(im).astype(np.float32)
    h, w = a.shape[:2]
    rng = np.random.default_rng(seed)
    gh, gw = h // CELL + 2, w // CELL + 2
    fields = []
    for _ in range(2):
        n = rng.standard_normal((gh, gw)).astype(np.float32)
        n = ndimage.zoom(n, (h / (gh - 1), w / (gw - 1)), order=3)[:h, :w]
        fields.append(n / (np.abs(n).max() + 1e-6) * amp)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    coords = [yy + fields[0], xx + fields[1]]
    out = np.stack([ndimage.map_coordinates(a[..., c], coords, order=1, mode='constant') for c in range(4)], -1)
    return Image.fromarray(np.clip(out, 0, 255).astype('uint8'), 'RGBA')


def fit(im, height):
    return im.resize((max(1, round(im.width * height / im.height)), height), Image.LANCZOS)


def write(name, im, built):
    pad = 4  # room for the wobble at the edges
    canvas = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    canvas.paste(im, (pad, pad))
    for i in range(3):
        boil(canvas, 100 + i * 17).save(os.path.join(OUT, f'{name}-{i}.webp'), quality=82, method=6)
    print(name, canvas.size)
    built.append(name)


def scenery_pieces(path):
    """Split the sheet into its drawings: label the alpha, drop specks, order by row then column."""
    sheet = cutout(path, holes=HOLES.get(SCENERY_FILE, 0))
    a = np.array(sheet)[..., 3] > 40
    lab, _ = ndimage.label(ndimage.binary_dilation(a, iterations=6))
    boxes = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if h * w < 2000:
            continue
        cy, cx = (sl[0].start + sl[0].stop) / 2, (sl[1].start + sl[1].stop) / 2
        boxes.append((round(cy / 300), cx, sl, i + 1))
    boxes.sort(key=lambda b: (b[0], b[1]))
    pieces = []
    for _, _, sl, idx in boxes:
        part = sheet.crop((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop))
        mask = Image.fromarray(((lab[sl] == idx) * 255).astype('uint8'))
        alpha = Image.fromarray(np.minimum(np.array(part)[..., 3], np.array(mask)).astype('uint8'))
        part.putalpha(alpha)
        pieces.append(part.crop(part.getbbox()))
    return pieces


def main():
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith('.webp'):
            os.remove(os.path.join(OUT, old))
    cache = {}
    built = []
    for name, (fn, mirror) in POSES.items():
        if not os.path.exists(os.path.join(SRC, fn)):
            print('skip', name, '(no', fn + ')')
            continue
        if fn not in cache:
            cache[fn] = fit(cutout(os.path.join(SRC, fn), holes=HOLES.get(fn, 0)), H)
        im = cache[fn]
        if mirror:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        write(name, im, built)
    sheet = os.path.join(SRC, SCENERY_FILE)
    if os.path.exists(sheet):
        pieces = scenery_pieces(sheet)
        if len(pieces) != len(SCENERY):
            raise SystemExit(f'scenery sheet split into {len(pieces)} pieces, expected {len(SCENERY)}')
        for (name, height), im in zip(SCENERY, pieces):
            write('sc-' + name, fit(im, height), built)
    # The site loads only the keys that exist, so a pose that hasn't been drawn yet falls back without 404s.
    with open(os.path.join(OUT, 'manifest.js'), 'w') as f:
        f.write('const SQ_POSES=' + str(built).replace("'", '"') + ';\n')


if __name__ == '__main__':
    main()
