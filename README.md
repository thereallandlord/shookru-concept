# Шукру — исходники дизайн-концепции

Собранный сайт лежит в ветке `main` и публикуется на
https://thereallandlord.github.io/shookru-concept/

## Что здесь
- `src/v6-quiet.html` — исходник страницы с плейсхолдерами `{{IMG:имя}}`
- `src/v1..v5` — пять первых направлений (в прод не пошли, оставлены для истории)
- `build.py` — подставляет картинки как data-URI, кладёт в `dist/`
- `build_site.py` — собирает готовые страницы сайта (`index.html`, `sadaka.html`) с превью
- `data/` — выгрузка открытого API Шукру: сборы, суммы, фонды, описания
- `assets/web/` — оптимизированные фотографии и сгенерированный кадр героя

## Как пересобрать
```
python3 build_site.py     # → site/index.html и site/sadaka.html
```

## Откуда данные
Открытые эндпоинты платформы, без авторизации:
- `api.shookru.com/charity/api/fundraisers/feed?pageSize=60&page=N` — сборы, суммы, фото, фонды
- `api.shookru.com/charity/api/fundraisers?pagination[page]=N` — описания сборов
- `api.shookru.com/charity/api/showcases/config/charity.shookru.com` — фирменный цвет `#07BC8E`, флаги
