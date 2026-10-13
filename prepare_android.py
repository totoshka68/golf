"""Готовит созданный Capacitor-проект android/: иконки клуба, заставка, подпись релиза, запрет облачных копий.
Запускается в облачной сборке после `npx cap add android`. Требует: pip install pillow."""
import glob, re, sys
from PIL import Image, ImageDraw

GREEN = (27, 77, 46); GOLD = (212, 160, 84); CREAM = (246, 242, 227)

def art(size, scale=1.0, bg=True, round_=False):
    S = size * 4
    im = Image.new('RGBA', (S, S), GREEN + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = S * scale / 100.0; ox = (S - S * scale) / 2
    X = lambda x: ox + x * u
    Y = lambda y: ox + y * u
    d.rounded_rectangle([X(47), Y(18), X(51), Y(76)], radius=u * 2, fill=CREAM)
    d.polygon([(X(51), Y(18)), (X(76), Y(30)), (X(51), Y(42))], fill=GOLD)
    d.ellipse([X(35), Y(72), X(65), Y(82)], fill=CREAM)
    d.ellipse([X(41), Y(74), X(59), Y(80)], fill=GREEN)
    im = im.resize((size, size), Image.LANCZOS)
    if round_:
        m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
        out = Image.new('RGBA', (size, size), (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out
    return im

res = 'android/app/src/main/res/'
n = 0
for f in glob.glob(res + 'mipmap-*/ic_launcher.png'):
    art(Image.open(f).size[0], 1.0).save(f); n += 1
for f in glob.glob(res + 'mipmap-*/ic_launcher_round.png'):
    art(Image.open(f).size[0], 1.0, round_=True).save(f); n += 1
for f in glob.glob(res + 'mipmap-*/ic_launcher_foreground.png'):
    art(Image.open(f).size[0], 0.62, bg=False).save(f); n += 1
for f in glob.glob(res + 'drawable*/splash.png'):
    w, h = Image.open(f).size
    im = Image.new('RGB', (w, h), GREEN); a = art(min(w, h) // 3, 1.0, bg=False)
    im.paste(a, ((w - a.size[0]) // 2, (h - a.size[1]) // 2), a); im.save(f); n += 1
if n < 10: sys.exit('Не нашла иконки шаблона, проверьте версию Capacitor')

def patch(path, fn):
    s = open(path, encoding='utf8').read(); t = fn(s)
    if t == s: sys.exit('Не удалось изменить ' + path)
    open(path, 'w', encoding='utf8').write(t)

patch(res + 'values/ic_launcher_background.xml', lambda s: s.replace('#FFFFFF', '#1B4D2E'))
patch('android/app/src/main/AndroidManifest.xml', lambda s: s.replace('android:allowBackup="true"', 'android:allowBackup="false"'))
SIGN = """    signingConfigs {
        release {
            def ks = System.getenv('KEYSTORE_PATH')
            if (ks) {
                storeFile file(ks)
                storePassword System.getenv('KEYSTORE_PASSWORD')
                keyAlias System.getenv('KEY_ALIAS')
                keyPassword System.getenv('KEY_PASSWORD')
            }
        }
    }
    buildTypes {
        release {
            if (System.getenv('KEYSTORE_PATH')) { signingConfig signingConfigs.release }
"""
patch('android/app/build.gradle', lambda s: s.replace("    buildTypes {\n        release {\n", SIGN, 1))
print('Готово: иконок и заставок', n)
