"""Cut the locked art into site sprites with hand-drawn "line boil".

For each pose this writes img/sq/<pose>-<n>.webp, n = 0..2. Each variant is the
same drawing pushed through a different smooth random displacement, so cycling
them a few times a second makes the outlines wobble like redrawn frames.

    pip install pillow numpy scipy
    python tools/boil.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'art', 'locked')
OUT = os.path.join(ROOT, 'img', 'sq')
H = 640          # stored sprite height in px
AMP = 2.4        # boil strength in px at H
CELL = 22        # noise feature size in px at H
POSES = {
    'back': ('03-back-walk.jpg', False),
    'backM': ('03-back-walk.jpg', True),
    'look': ('04-look-back.jpg', False),
    'lookM': ('04-look-back.jpg', True),
    'front': ('02-mask-on-front.jpg', False),
    'held': ('01-mask-held-front.png', False),
    # Pump dance and dump poses, generated in Canva from 02 (media ids MAHZD0yuaU0, MAHZD1UT4_c, MAHZD9Jkbcc, MAHZD7gQQTA).
    # Any file that is missing is skipped, and the site falls back to the plain front view for that pose.
    # Two generations came out with the same knee up, so the other side is a mirror of 05 (only the zipper pull swaps shoulders).
    'danceA': ('05-dance-knee-up.jpg', False),
    'danceB': ('05-dance-knee-up.jpg', True),
    'squat': ('07-dance-squat.jpg', False),
    'frozen': ('08-dump-frozen.jpg', False),
}


def cutout(path):
    """Remove the flat gray background and the gray ground line."""
    im = Image.open(path).convert('RGB')
    a = np.array(im).astype(int)
    h = a.shape[0]
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    bg = (sat < 22) & (mx > 125)
    dark = (sat < 25) & (mx < 110)
    k = 9
    up = np.zeros_like(bg); up[k:] = bg[:-k]
    dn = np.zeros_like(bg); dn[:-k] = bg[k:]
    line = dark & up & dn          # thin dark strokes with background above and below
    line[:h - 200] = False         # only the ground line near the bottom
    lab, _ = ndimage.label(bg | line)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(edge))
    alpha = Image.fromarray(((~outside) * 255).astype('uint8'))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(alpha)
    return im.crop(im.getbbox())


def boil(im, seed):
    a = np.array(im).astype(np.float32)
    h, w = a.shape[:2]
    rng = np.random.default_rng(seed)
    gh, gw = h // CELL + 2, w // CELL + 2
    fields = []
    for _ in range(2):
        n = rng.standard_normal((gh, gw)).astype(np.float32)
        n = ndimage.zoom(n, (h / (gh - 1), w / (gw - 1)), order=3)[:h, :w]
        fields.append(n / (np.abs(n).max() + 1e-6) * AMP)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    coords = [yy + fields[0], xx + fields[1]]
    out = np.stack([ndimage.map_coordinates(a[..., c], coords, order=1, mode='constant') for c in range(4)], -1)
    return Image.fromarray(np.clip(out, 0, 255).astype('uint8'), 'RGBA')


def main():
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    built = []
    for name, (fn, mirror) in POSES.items():
        if not os.path.exists(os.path.join(SRC, fn)):
            print('skip', name, '(no', fn + ')')
            continue
        if fn not in cache:
            im = cutout(os.path.join(SRC, fn))
            cache[fn] = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
        im = cache[fn]
        if mirror:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        pad = 4  # room for the wobble at the edges
        canvas = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
        canvas.paste(im, (pad, pad))
        for i in range(3):
            boil(canvas, 100 + i * 17).save(os.path.join(OUT, f'{name}-{i}.webp'), quality=82, method=6)
        print(name, canvas.size)
        built.append(name)
    # The site loads only the poses that exist, so a pose that hasn't been drawn yet falls back without 404s.
    with open(os.path.join(OUT, 'manifest.js'), 'w') as f:
        f.write('const SQ_POSES=' + str(built).replace("'", '"') + ';\n')


if __name__ == '__main__':
    main()
