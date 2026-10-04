"""Сборка: src/index.html -> docs/index.html (ссылки, неразрывные пробелы). Запуск: python3 build.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHANNELS = {"tg": "https://t.me/yurazol_auto", "mx": None}   # каналы YuraZol Auto для «Получить каталог»; в MAX канала пока нет
MAX_HREF = "https://max.ru/u/f9LHodD0cOLQzwPoUyWBoejqc5iq940FAYmSIsMAm8Hr1FcNu85zWG126zY"
SHORT = r"(?<![\wА-Яа-яЁё/-])([вВкКсСоОуУиИаАяЯ]|на|На|по|По|до|До|от|От|из|Из|не|Не|за|За|для|Для|без|Без|при|При|или|под|Под|что|до|мы|Мы|их|её|он)( )"


def typo(text):
    text = re.sub(SHORT, r"\1&nbsp;", text)
    text = re.sub(r" (—|–)", r"&nbsp;\1", text)           # тире не в начале строки
    text = re.sub(r"(\d) (\d{3})", r"\1&nbsp;\2", text)     # 1 769 998
    text = re.sub(r"(\d) (₽|¥|л\.с\.|кВт|км|млн|дней|лет|%)", r"\1&nbsp;\2", text)
    text = re.sub(r"(\d+–\d+)", r'<span class="nw">\1</span>', text)  # 50–65 не рвать
    text = text.replace("б/у", '<span class="nw">б/у</span>')        # не рвать на косой черте
    return text


def render(src):
    """Исходник страницы -> готовый HTML (им же пользуется сборка mtk-vostok-avto.ru)."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<title.*?</title>|<[^>]+>)", src, flags=re.S)
    out = "".join(p if p.startswith("<") else typo(p) for p in parts)
    return out.replace('href="MAX_HREF"', f'href="{MAX_HREF}"')


def catalog(src, tg=None, mx=None):
    """Кнопка «Получить каталог» открывает окно со ссылками на каналы сайта (Telegram, MAX).
    Канала нет — его кнопки нет; нет ни одного — окна нет, кнопка ведёт к Юрию в Telegram."""
    if not (tg or mx):
        src = re.sub(r'\n<dialog class="dlg" id="getcat".*?</dialog>\n', "\n", src, flags=re.S)
        src = src.replace(' data-cat href="CAT_HREF"', ' href="https://t.me/YuraZol"')
        return src.replace("Полный каталог — в нашем канале.", "Каталог пришлём в Telegram, MAX или WhatsApp.")
    src = src.replace('href="CAT_HREF"', f'href="{tg or mx}"')
    for ph, href in (("CAT_TG_HREF", tg), ("CAT_MAX_HREF", mx)):
        if href:
            src = src.replace(f'href="{ph}"', f'href="{href}"')
        else:
            src = re.sub(rf'\n *<a [^>]*href="{ph}".*?</a>', "", src)
    return src.replace(" в Telegram или MAX.", " в Telegram." if tg and not mx else " в MAX." if mx and not tg else " в Telegram или MAX.")


if __name__ == "__main__":
    out = render(catalog((ROOT / "src/index.html").read_text(), **CHANNELS))
    (ROOT / "docs/index.html").write_text(out)
    print("index.html", len(out))
