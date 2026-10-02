"""Готовит картинки сайта из материалов ~/auto-china (запуск: python3 prep_assets.py)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

AC = Path.home() / "auto-china"
OUT = Path(__file__).resolve().parent / "docs" / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def save(im, name, w, q=80):
    im = im.convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(OUT / f"{name}.jpg", quality=q, optimize=True, progressive=True)
    im.save(OUT / f"{name}.webp", quality=q - 2, method=6)


# главное фото: автосалон с номерами YuraZol Auto
hall = Image.open(AC / "kp_v3/assets/choice_yurazol.jpg")
save(hall, "hall", 2200, 78)
save(hall, "hall_m", 1100, 78)
# превью ссылки (Telegram, MAX, WhatsApp): 1200x630
og = ImageOps.fit(hall, (1200, 630), Image.LANCZOS, centering=(0.5, 0.62))
og.convert("RGB").save(OUT / "og.jpg", quality=84, optimize=True)

# разделы каталога
for i in range(4):
    save(Image.open(AC / f"catalog/cars/hero_sec{i}.jpg"), f"sec{i}", 1000, 78)

# примеры выданных автомобилей
for k in ("xrv", "q05", "yaris", "coolray"):
    for n in (1, 2):
        save(Image.open(AC / f"catalog/deliveries/{k}_{n}.jpg"), f"d_{k}_{n}", 560, 84)

# логотип и иконки
logo = Image.open(AC / "assets/logo.png").convert("RGBA")
for s in (96, 192, 512):
    logo.resize((s, round(s * logo.height / logo.width)), Image.LANCZOS).save(OUT / f"logo{s}.png", optimize=True)
fav = ImageOps.pad(logo, (180, 180), Image.LANCZOS, color=(0, 0, 0, 0))
fav.save(OUT.parent / "apple-touch-icon.png")
ImageOps.pad(logo, (64, 64), Image.LANCZOS, color=(0, 0, 0, 0)).save(OUT.parent / "favicon.png")

# Юрий — круглое фото для контактов
yura = Image.open(AC / "assets/yura.jpg")
yura = ImageOps.fit(yura, (320, 320), Image.LANCZOS, centering=(0.5, 0.42))
save(yura, "yura", 320, 84)
print("ok")
