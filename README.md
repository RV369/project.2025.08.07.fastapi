
# project.2025.08.07.fastapi

- Проект создан по материалам опубликованным в открытом доступе по адресу: 
- https://vlad1kudelko.github.io/posts/fastapi-jwt-authentication
- Официальная документация доступна по адресу:
- https://fastapi.tiangolo.com/ru/tutorial/security/oauth2-jwt/#token

```sh
py -3.12 -m venv venv
```
```sh
source venv/Scripts/activate
```
```sh
git@github.com:RV369/project.2025.08.07.fastapi.git
```

- Запустить Docker и запустить контейнер
```sh
docker compose up
```

Для развертывания необходимо:

- Скопировать файл docker-compose.production.yml
- Создать файл .env с содержимым указанным в файле .env.example
- Запустить Docker
- команда для запуска скачивания образа и сборки контейнера:
```sh
docker compose -f docker-compose.production.yml up
```

##  Документация доступна по адресам

- <http://127.0.0.1:8000/docs>

- <http://127.0.0.1:8000/redoc>
