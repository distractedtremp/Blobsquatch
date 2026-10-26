"""Brand assets from the clean-meme set: token logo / X profile picture, stickers, X banner, meme templates.

    python tools/brand.py
Writes into brand/. Sources are the cut-outs from art/candidates/clean-meme (same cut as the sprites).
"""
import os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boil import cutout, SRC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'brand')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F = lambda s: ImageFont.truetype(FONT, s)
GREEN = (0, 236, 151, 255)


def fig(name):
    return cutout(os.path.join(SRC, name + '.png'))


def disc(im, frac, yoff, name, size=1024, bg=(12, 26, 28)):
    """Head-and-shoulders crop (top `frac` of the figure) on a flat night disc with a NEAR-green ring."""
    c = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(c).ellipse((0, 0, size - 1, size - 1), fill=bg + (255,))
    crop = im.crop((0, 0, im.width, int(im.height * frac)))
    s = size * .92 / crop.width if crop.width / crop.height > 1 else size * .86 / crop.height
    crop = crop.resize((int(crop.width * s), int(crop.height * s)), Image.LANCZOS)
    layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    layer.alpha_composite(crop, ((size - crop.width) // 2, int(size * yoff)))
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    layer.putalpha(Image.fromarray(np.minimum(np.array(layer.split()[3]), np.array(mask))))
    c.alpha_composite(layer)
    ImageDraw.Draw(c).ellipse((6, 6, size - 7, size - 7), outline=GREEN, width=22)
    c.save(os.path.join(OUT, name + '.png'))
    c.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, name + '-512.png'))


def forest(w, h, seed=3):
    im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h; d.line([(0, y), (w, y)], fill=(int(8 + 12 * t), int(18 + 30 * t), int(38 - 12 * t)))
    random.seed(seed)
    for _ in range(18):
        x = random.randint(0, w); d.rectangle((x, 0, x + random.randint(10, 40), h), fill=(14, 22, 20))
    d.rectangle((0, h - int(h * .12), w, h), fill=(16, 36, 28))
    return im


def panel(figure, hfrac, blur, w=600, h=600):
    im = forest(w, h)
    f = figure.resize((int(figure.width * h * hfrac / figure.height), int(h * hfrac)), Image.LANCZOS)
    if blur:
        f = f.filter(ImageFilter.GaussianBlur(blur))
    im.paste(f, ((w - f.width) // 2, h - int(h * .12) - f.height + 10), f)
    return im


def caption(im, top, bottom=None):
    d = ImageDraw.Draw(im); f = F(44)
    def t(txt, y):
        x = (im.width - d.textlength(txt, font=f)) / 2
        for dx in (-3, 3):
            for dy in (-3, 3):
                d.text((x + dx, y + dy), txt, font=f, fill='black')
        d.text((x, y), txt, font=f, fill='white')
    t(top, 20)
    if bottom:
        t(bottom, im.height - 70)
    return im


def pair(a, b, name):
    m = Image.new('RGB', (1210, 600), 'black'); m.paste(a, (0, 0)); m.paste(b, (610, 0))
    m.save(os.path.join(OUT, name), quality=88)


def banner(back, look):
    W, H = 1500, 500
    b = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(b)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(8 + 10 * t), int(18 + 22 * t), int(38 - 10 * t), 255))
    random.seed(7)
    for _ in range(26):
        x = random.randint(0, W); w = random.randint(14, 60); d.rectangle((x, 0, x + w, H), fill=(14, 22, 20, 255))
    d.rectangle((0, H - 60, W, H), fill=(16, 36, 28, 255))
    far = back.resize((int(back.width * 200 / back.height), 200), Image.LANCZOS).filter(ImageFilter.GaussianBlur(5))
    b.alpha_composite(far, (300, H - 60 - 200 + 10))
    near = look.resize((int(look.width * 600 / look.height), 600), Image.LANCZOS).crop((0, 0, 0, 0) if False else (0, 0, int(look.width * 600 / look.height), H - 12))  # head in frame, legs run off the bottom
    b.alpha_composite(near, (W - near.width - 60, 12))
    f, f2 = F(96), F(34); d = ImageDraw.Draw(b)
    d.text((60, 120), 'BLOB', font=f, fill=(200, 135, 78, 255))
    bw = d.textlength('BLOB', font=f); d.text((60 + bw, 120), 'SQUATCH', font=f, fill=(232, 240, 234, 255))
    d.text((64, 240), '$BLOBSQUATCH on NEAR', font=f2, fill=GREEN)
    d.text((64, 290), "NEAR's mascot nobody believes in.", font=f2, fill=(159, 184, 176, 255))
    blob = b.crop((50, 100, 60 + int(bw) + 10, 230)).filter(ImageFilter.GaussianBlur(2.2)); b.paste(blob, (50, 100))
    b.convert('RGB').save(os.path.join(OUT, 'x-banner-1500x500.png'))


def main():
    os.makedirs(OUT, exist_ok=True)
    front, held, look, back = fig('front'), fig('held'), fig('look'), fig('back')
    disc(front, .34, .05, 'logo-masked')      # the token logo and X profile picture
    disc(held, .40, .06, 'logo-unmasked')
    disc(look, .34, .05, 'logo-lookback')
    for n, im in [('sticker-held', held), ('sticker-back', back), ('sticker-look', look), ('sticker-front', front)]:
        im.resize((int(im.width * 512 / im.height), 512), Image.LANCZOS).save(os.path.join(OUT, n + '.png'))
    pair(caption(panel(back, .45, 6), 'EXPECTATION'), caption(panel(held, .95, 0), 'REALITY'), 'meme-expectation-reality.jpg')
    pair(caption(panel(back, .35, 7), 'HOW IT STARTED', '1967'), caption(panel(back, .35, 7), "HOW IT'S GOING", '2026'), 'meme-started-going.jpg')
    pair(caption(panel(back, .3, 8), 'FROM FAR AWAY'), caption(panel(look, 1.0, 0), 'YOU HAD TO BE NEAR'), 'meme-you-had-to-be-near.jpg')
    banner(back, look)
    print(sorted(os.listdir(OUT)))


if __name__ == '__main__':
    main()
