"""Скриншоты для Юрия: python3 shot.py [палитра]"""
import sys
from pathlib import Path
if (Path.home() / "auto-china" / "NO_SERVER_BROWSER").exists():   # браузер на сервере запрещён (флаг группы «Авто», KATE 24.11.2026)
    sys.exit("Chromium на сервере запрещён (~/auto-china/NO_SERVER_BROWSER). Снимки страниц — через ПК «Рязань»: python3 ~/yurazol-sites/tools/pc_shot.py <адрес>")
from playwright.sync_api import sync_playwright
pal = sys.argv[1] if len(sys.argv) > 1 else ""
url = "file:///home/sergei/yurazol-sites/yurazol.ru/docs/index.html" + (f"?p={pal}" if pal else "")
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    for name, w, h, s in [("desk", 1440, 900, 1), ("mob", 390, 844, 2)]:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=s)
        pg.goto(url); pg.wait_for_timeout(700)
        H = pg.evaluate("document.documentElement.scrollHeight")
        for y in range(0, H, 500):
            pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(60)
        pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));document.querySelectorAll('.say .w').forEach(e=>e.classList.add('on'));document.querySelectorAll('.row').forEach(e=>e.style.animation='none')")
        pg.wait_for_timeout(1000)
        pg.screenshot(path=f"/tmp/yz/{name}{('_'+pal) if pal else ''}_first.png")
        pg.screenshot(path=f"/tmp/yz/{name}{('_'+pal) if pal else ''}_full.png", full_page=True)
        print(name, H)
    b.close()
