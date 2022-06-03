![CI/CD](https://github.com/avb15214yp/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Проект foodgram

```
Foodgram, «Продуктовый помощник». Это онлайн-сервис и API для него. Вы сможете публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд!
```

#### Стек разработки
```
React
django
nginx
postgres
```

### API

```
Описание в проекте: http://51.250.22.28/api/docs/
Основная страница: http://51.250.22.28
Доступ в админ. панель: http://51.250.22.28/admin/
admin
admin

Доступ на сайт
admin@ya.ru
admin
```

### Шаблон наполнения env-файла:
env-файл необходимо заполнить следующими значениями:
```
SECRET_KEY=
DB_ENGINE= django.db.backends.postgresql
DB_NAME= # имя базы данных
POSTGRES_USER= # логин для подключения к базе данных
POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
PAGE_SIZE=6 #Количество записей при пагинации

```

### Как запустить проект в контейнерах:


```
infra$docker-compose up -d --build

infra$docker-compose exec backend python manage.py migrate
infra$docker-compose exec backend python manage.py createsuperuser
infra$docker-compose exec backend python manage.py collectstatic --no-input 
```
### Как заполнить базу данных 

## ингредиентами
```
docker-compose exec backend python manage.py load_ingredients ingredients.csv
```
## тегами

```
через админ панель http://51.250.22.28/admin/
admin
admin
значениями: 
Завтрак #00ff00 breakfast 
Обед #0000ff dinner 
Ужин #ff0000 lunch 

```

##

Разработчики:

```
https://github.com/yandex-praktikum (Яндекс)
frontend, идея и постановка
```

```
https://github.com/avb15214yp (avb15214)
backend, CI/CD
```


Ссылка на сайт: http://51.250.22.28


### Отдельное спасибо
```
Жене и детям которые:
- мужественно терпели период подготовки и сдачи проекта
- кормили
```