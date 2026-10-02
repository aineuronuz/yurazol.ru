# yurazol.ru — сайт «YuraZol Авто»

Сайт публикуется GitHub Pages из папки `docs/` (ветка main), домен в `docs/CNAME`.

- `src/index.html` — исходник страницы; `python3 build.py` собирает `docs/index.html` (ссылка MAX, неразрывные пробелы).
- `prep_assets.py` — готовит картинки в `docs/assets/img` из материалов `~/auto-china` (на сервере).
- `shot.py` — скриншоты для согласования.

В репо нет персональных данных клиентов: репо публичное.

## Страницы фото для КП
`python3 foto.py <код>` — из `~/yurazol-sites/foto-inbox/<код>/` (1.jpg…N.jpg + title.txt) собирает `docs/foto/<код>/`.
Ссылка `https://yurazol.ru/foto/<код>/#N` открывает фото N (PhotoSwipe 5, MIT, в `docs/assets/vendor/photoswipe`). Страницы закрыты от поиска (noindex, robots.txt).
