# Music Project

Этот проект — веб-приложение на Django для работы с музыкой (загрузка, хранение, отображение треков и аватаров).

## Быстрый старт

1. **Клонируйте репозиторий:**
   ```sh
   git clone https://github.com/Georgy451/First-project.git

   ```

2. **Создайте и активируйте виртуальное окружение (рекомендуется):**
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**
   По умолчанию используется PostgreSQL. Убедитесь, что у вас установлен и запущен PostgreSQL, и параметры подключения указаны в `music/settings.py`.

5. **Примените миграции:**
   ```sh
   python manage.py migrate
   ```

6. **Запустите сервер разработки:**
   ```sh
   python manage.py runserver
   ```

7. **Откройте в браузере:**
   Перейдите по адресу http://127.0.0.1:8000/

## Зависимости

- Django==4.2.5
- psycopg2==2.9.9

## Docker (опционально)

Если хотите запустить проект в Docker:

1. Соберите образ:
   ```sh
   docker build -t music-app .
   ```
2. Запустите контейнер:
   ```sh
   docker run -p 8000:8000 music-app
   ```
