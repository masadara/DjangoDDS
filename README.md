# Тестовое задание: Веб-сервис для управления движением денежных средств (ДДС)

## Описание:

https://drive.google.com/file/d/1vbPk2aiMe52pDFW57zMUDMaW7rqrHypc/view

## Как запустить проект:

1. Клонируйте репозиторий:
```
git clone https://github.com/masadara/project2
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Создайте и заполните данными файл <b>.env</b> по примеру <b>.env.sample</b>

4. Создайте и примените миграции

```
python manage.py makemigrations
python manage.py migrate
```

5. Если необходимо, загрузите следующие фикстуры:

```
   python manage.py loaddata big_data.json --format json
```
6. Перейти по адресу: http://127.0.0.1:8000/cashflow/

