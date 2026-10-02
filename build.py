"""Сборка: src/index.html -> docs/index.html (ссылки, неразрывные пробелы). Запуск: python3 build.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAX_HREF = "https://max.ru/u/f9LHodD0cOLQzwPoUyWBoejqc5iq940FAYmSIsMAm8Hr1FcNu85zWG126zY"
SHORT = r"(?<![\wА-Яа-яЁё-])([вВкКсСоОуУиИаАяЯ]|на|На|по|По|до|До|от|От|из|Из|не|Не|за|За|для|Для|без|Без|при|При|или|под|Под|что|до|мы|Мы|их|её|он)( )"


def typo(text):
    text = re.sub(SHORT, r"\1&nbsp;", text)
    text = re.sub(r" (—|–)", r"&nbsp;\1", text)           # тире не в начале строки
    text = re.sub(r"(\d) (\d{3})", r"\1&nbsp;\2", text)     # 1 769 998
    text = re.sub(r"(\d) (₽|¥|л\.с\.|кВт|дней|лет|%)", r"\1&nbsp;\2", text)
    text = re.sub(r"(\d+–\d+)", r'<span class="nw">\1</span>', text)  # 45–60 не рвать
    return text


src = (ROOT / "src/index.html").read_text()
parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", src, flags=re.S)
out = "".join(p if p.startswith("<") else typo(p) for p in parts)
out = out.replace('href="MAX_HREF"', f'href="{MAX_HREF}"')
(ROOT / "docs/index.html").write_text(out)
print("index.html", len(out))
