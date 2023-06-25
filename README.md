# Book Catalog

### Разработан через **DjangoRestFramework, PostgreSQL, Celery, Redis** 
![DjangoRestFramework Version](https://img.shields.io/badge/djangorestframework-3.0.0-orange)
![PostgreSQL Version](https://img.shields.io/badge/postgre-3.0.0-blue.svg)
![Celery Version](https://img.shields.io/badge/celery-3.0.0-green.svg)
![Redis Version](https://img.shields.io/badge/redis-3.0.0-red.svg)

| Таблица: BOOK           |                            |
|-------------------------|----------------------------|
| Поле                    | Тип данных                 |
| id                      | Уникальный идентификатор    |
| title                   | Str   |
| opublication_date       | Date     |
| authors                 | FK   |
| genres                  | FK |

| Таблица: Genre          |                            |
|-------------------------|----------------------------|
| Поле                    | Тип данных                 |
| id                      | Уникальный идентификатор    |
| name                    | Str                |

| Таблица: Author         |                            |
|-------------------------|----------------------------|
| Поле                    | Тип данных                 |
| id                      | Уникальный идентификатор    |
| first_name              | Str                |
| last_name               | Str        |

| Таблица: Review         |                            |
|-------------------------|----------------------------|
| Поле                    | Тип данных                 |
| id                      | Уникальный идентификатор    |
| user                    | FK                          |
| book                    | FK                          |
| text                    | Str            |
| rating                  | int                     |


### URL pattern endpoints:
```python
urlpatterns = [
    'api/register/',
    'api/email-verify/<str:uid>/<str:token>/',
    'api/login/',
    'main/books/', # + filters 
    'main/books/<int:pk>',
    'main/favorites/', # POST, GET methods
]
```

## Запуск проекта

#### Clone the repository to your local machine:
>`git clone https://github.com/DauletKalesh/Elefanto_book_catalog.git`

#### To run the project:

>`docker-compose up --build`

#### For questions and support, feel free to contact me: dauka_0202@mail.ru