"""Страница оригиналов фото для КП: python3 foto.py <код>

Берёт ~/yurazol-sites/foto-inbox/<код>/ (1.jpg…N.jpg + title.txt) и собирает
docs/foto/<код>/ — оригиналы (до 2560 px), превью t/N.jpg и index.html.
Ссылка для КП: https://yurazol.ru/foto/<код>/#N — сразу открывает фото N.
"""
import html
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
INBOX = ROOT.parent / "foto-inbox"
MAX_SIDE = 2560
MAX_HREF = "https://max.ru/u/f9LHodD0cOLQzwPoUyWBoejqc5iq940FAYmSIsMAm8Hr1FcNu85zWG126zY"


def photos(src):
    files = [f for f in src.iterdir() if re.fullmatch(r"\d+\.jpe?g", f.name.lower())]
    files.sort(key=lambda f: int(f.stem))
    nums = [int(f.stem) for f in files]
    if nums != list(range(1, len(files) + 1)):
        sys.exit(f"нумерация фото должна идти подряд с 1, а сейчас: {nums}")
    return files


def build(code):
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", code):
        sys.exit("код: строчная латиница, цифры и дефис")
    src = INBOX / code
    title = (src / "title.txt").read_text(encoding="utf-8").strip()
    out = ROOT / "docs" / "foto" / code
    if out.exists():
        shutil.rmtree(out)
    (out / "t").mkdir(parents=True)

    items = []
    for f in photos(src):
        n = int(f.stem)
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        if max(im.size) > MAX_SIDE:
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            im.save(out / f"{n}.jpg", quality=86, optimize=True, progressive=True)
        else:   # уже в пределах — копируем как есть, без пережатия (метаданные снимаем)
            Image.open(f).save(out / f"{n}.jpg", quality="keep", optimize=True, progressive=True, exif=b"")
        th = im.copy()
        th.thumbnail((640, 640), Image.LANCZOS)
        th.save(out / "t" / f"{n}.jpg", quality=80, optimize=True, progressive=True)
        items.append((n, im.width, im.height))

    t = html.escape(title)
    cards = "\n".join(
        f'<a href="{n}.jpg" data-pswp-width="{w}" data-pswp-height="{h}" aria-label="Фото {n}">'
        f'<img src="t/{n}.jpg" alt="{t}, фото {n}" width="{w}" height="{h}" loading="{"eager" if n <= 6 else "lazy"}"><span>{n}</span></a>'
        for n, w, h in items)
    page = TEMPLATE.replace("{TITLE}", t).replace("{COUNT}", str(len(items))).replace("{CARDS}", cards) \
                   .replace("{MAX}", MAX_HREF).replace("{WORD}", word(len(items)))
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"docs/foto/{code}/: {len(items)} фото — https://yurazol.ru/foto/{code}/#1")


def word(n):
    k = n % 100
    if 11 <= k <= 14:
        return "фотографий"
    return {1: "фотография", 2: "фотографии", 3: "фотографии", 4: "фотографии"}.get(n % 10, "фотографий")


TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>{TITLE} — фото | YuraZol Авто</title>
<meta name="theme-color" content="#f5f7fb">
<link rel="icon" type="image/png" href="../../assets/favicon.png">
<link rel="stylesheet" href="../../assets/vendor/photoswipe/photoswipe.css">
<style>
@font-face{font-family:'Unbounded';src:url('../../assets/fonts/Unbounded-cyrillic.woff2') format('woff2');font-weight:200 900;font-display:swap;unicode-range:U+0400-045F}
@font-face{font-family:'Unbounded';src:url('../../assets/fonts/Unbounded-latin.woff2') format('woff2');font-weight:200 900;font-display:swap;unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:'Roboto Flex';src:url('../../assets/fonts/RobotoFlex-cyrillic.woff2') format('woff2');font-weight:100 1000;font-display:swap;unicode-range:U+0400-045F}
@font-face{font-family:'Roboto Flex';src:url('../../assets/fonts/RobotoFlex-latin.woff2') format('woff2');font-weight:100 1000;font-display:swap;unicode-range:U+0000-00FF,U+2000-206F}
*{box-sizing:border-box}
body{margin:0;background:#f5f7fb;color:#0e1b2e;font:16px/1.55 'Roboto Flex',-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:0 18px}
header{display:flex;align-items:center;gap:12px;padding:18px 0 6px}
header img{width:40px;height:39px}
header b{font-family:'Unbounded',sans-serif;font-weight:700;font-size:15px}
header small{display:block;color:rgba(14,27,46,.6);font-size:12px;margin-top:2px}
h1{font-family:'Unbounded',sans-serif;font-weight:700;font-size:clamp(22px,3.4vw,36px);line-height:1.15;margin:26px 0 8px}
.sub{color:rgba(14,27,46,.66);margin:0 0 22px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.g a{position:relative;display:block;border-radius:14px;overflow:hidden;background:#e6edf7;box-shadow:0 10px 26px -16px rgba(29,61,107,.45)}
.g img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;transition:transform .4s}
.g a:hover img{transform:scale(1.03)}
.g span{position:absolute;left:10px;top:10px;min-width:30px;height:30px;padding:0 8px;border-radius:15px;background:rgba(255,255,255,.9);
font:600 13px/30px 'Unbounded',sans-serif;text-align:center;color:#1d3d6b}
footer{margin:34px 0 40px;padding-top:22px;border-top:1px solid rgba(29,61,107,.14);display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center}
footer p{margin:0 10px 0 0;color:rgba(14,27,46,.66)}
.btn{display:inline-flex;align-items:center;height:42px;padding:0 18px;border-radius:21px;text-decoration:none;font:600 13px 'Unbounded',sans-serif;
background:#fff;color:#1d3d6b;border:1px solid rgba(29,61,107,.2)}
.btn.g1{background:linear-gradient(100deg,#efd27a,#c9a227);color:#1a1405;border:0}
.pswp__counter{font-family:'Unbounded',sans-serif;font-size:13px}
@media (max-width:560px){.g{grid-template-columns:1fr 1fr;gap:8px}.g a{border-radius:10px}.g span{left:6px;top:6px;height:24px;min-width:24px;font-size:11px;line-height:24px}}
</style>
</head>
<body>
<div class="wrap">
  <header><img src="../../assets/img/logo96.png" alt="" width="40" height="39"><span><b>YuraZol Авто</b><small>автомобили из Китая под ключ</small></span></header>
  <h1>{TITLE}</h1>
  <p class="sub">{COUNT} {WORD} автомобиля. Нажмите на фото — откроется в полном размере: листайте пальцем, приближайте двумя пальцами.</p>
  <div class="g" id="g">
{CARDS}
  </div>
  <footer><p>Вопросы по автомобилю — Юрию:</p>
    <a class="btn g1" href="https://t.me/YuraZol">Telegram</a><a class="btn" href="{MAX}">MAX</a><a class="btn" href="https://wa.me/79119261617">WhatsApp</a></footer>
</div>
<script type="module">
import PhotoSwipeLightbox from '../../assets/vendor/photoswipe/photoswipe-lightbox.esm.min.js';
const COUNT = {COUNT};
const lb = new PhotoSwipeLightbox({
  gallery: '#g', children: 'a',
  pswpModule: () => import('../../assets/vendor/photoswipe/photoswipe.esm.min.js'),
  initialZoomLevel: 'fit', secondaryZoomLevel: 2, maxZoomLevel: 4,
  bgOpacity: 0.96, showHideAnimationType: 'fade', preload: [1, 2],
  closeTitle: 'Закрыть', zoomTitle: 'Приблизить', arrowPrevTitle: 'Назад', arrowNextTitle: 'Вперёд',
  indexIndicatorSep: ' из ', errorMsg: 'Фото не загрузилось'
});
lb.on('change', () => history.replaceState(null, '', '#' + (lb.pswp.currIndex + 1)));
lb.on('close', () => history.replaceState(null, '', location.pathname));
lb.init();
function openHash() {
  const n = parseInt(location.hash.slice(1), 10);
  if (n >= 1 && n <= COUNT && !(lb.pswp && lb.pswp.isOpen)) lb.loadAndOpen(n - 1);
}
addEventListener('hashchange', openHash);
openHash();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
