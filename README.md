# [МВФ «Каскад-Комплекс»](https://kaskadkompleks.ru/)

Каскад-Комплекс — это информационный сайт, посвящённый вопросам противопожарной безопасности.
Администрация сайта публикует новости и статьи по данной тематике.
Все анонимные пользователи могут ознакомиться с опубликованным контентом.
Кроме того, пользователи могут связаться с компанией «Каскад-Комплекс» через форму на странице «Контакты».

## Технологии

### Бекенд:
- Django
- SQLite
- Nginx + Gunicorn

### Фронтенд:
- HTML, CSS (Bootstrap 5)
- JS

## Доступ

Проект доступен на [https://kaskadkompleks.ru/](https://kaskadkompleks.ru/)

## Как развернуть проект на сервере

1. Клонируйте репозиторий:

    ```shell
    git clone git@github.com:PchelaR/kaskad-complex.git
    ```

2. Установите соединение с сервером:

    ```shell
    ssh username@server_address
    ```

3. Обновите индекс пакетов APT:

    ```shell
    sudo apt update
    ```

4. Отредактируйте файл `nginx/default.conf`:

    - В строках `server_name` укажите IP виртуальной машины (сервера).
    - Убедитесь, что у вас имеются SSL сертификаты.
    - В строках `ssl_certificate` и `ssl_certificate_key` укажите пути к вашим SSL сертификатам.

5. Проверьте наличие SSL сертификатов:

    Проверьте директорию, где хранятся сертификаты:

    ```shell
    ls /path/to/your/ssl/certificates/
    ```

    Просмотрите содержимое сертификатов:

    ```shell
    cat /path/to/your/ssl/certificates/cert.pem
    ```

    Проверьте детали сертификата с помощью OpenSSL:

    ```shell
    openssl x509 -in /path/to/your/ssl/certificates/cert.pem -text -noout
    ```

6. Отредактируйте файл `settings.py`:

    Замените `yourdomain.com` на ваш домен:

    ```python
    ALLOWED_HOSTS = ['yourdomain.com', 'localhost', '127.0.0.1']

    CSRF_TRUSTED_ORIGINS = [
        'https://yourdomain.com',
        'https://www.yourdomain.com',
    ]
    ```

7. В директории `kaskad_project` создайте файл `.env` и заполните его по аналогии:

    ```plaintext
    SECRET_KEY=secret_key

    EMAIL_HOST_USER=email@yandex.ru
    EMAIL_HOST_PASSWORD=password
    DEFAULT_FROM_EMAIL=email2@yandex.ru
    ```

8. Отредактируйте шаблоны со статической информацией:
    - `includes/header.html`
    - `includes/feature.html`
    - `includes/footer.html`
    - `contactspage.html`

9. Примените миграции:

    ```shell
    python3 manage.py makemigrations
    ```

    ```shell
    python3 manage.py migrate
    ```

10. Соберите и запустите проект с помощью Docker Compose:

    ```shell
    sudo docker-compose up -d --build
    ```

## Завершение

Проверьте, что все службы работают корректно и проверьте доступность вашего сайта по указанному URL.
