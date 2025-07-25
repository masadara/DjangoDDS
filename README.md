# Тестовое задание: Веб-сервис для управления движением денежных средств (ДДС)

## Описание:

ДДС (движение денежных средств) — это процесс учета, управления и анализа
поступлений и списаний денежных средств компании или частного лица.

https://drive.google.com/file/d/1vbPk2aiMe52pDFW57zMUDMaW7rqrHypc/view

## Как запустить проект:

Команды нужно выполнять из папки с проектом.

1. Клонируйте репозиторий:
```
    git clone https://github.com/masadara/DjangoDDS
```
2. Установите зависимости:
```
    pip install -r requirements.txt
```
3. Создайте и заполните данными файл <b>.env</b> по примеру <b>.env.sample</b>

4. Примените миграции

```
    python manage.py migrate
```

5. Если необходимо, загрузите следующие фикстуры:

```
    python manage.py loaddata big_data.json --format json
```
6. Чтобы запустить веб-приложение необхнодимо прописать:
```
    python manage.py runserver
```
7. Перейти по адресу: http://127.0.0.1:8000/cashflow/

