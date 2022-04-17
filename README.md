# Демо проект 'Частная библиотека'

### Описание
Разработанное API для частной библиотеки

### Проект разработан с соблюдением следующих требований:

- Clean architecture
- Использование фреймворка Falcon + набор библиотек Classic
- Наличие документации
- Наличие интеграционных и unit тестов

#### Основные технологии
- Falcon
- PostgreSQL
- SQLAlchemy
- Docker
- Nginx

##### Сторонние сервисы
- https://api.itbook.store/

#### Установка и запуск
1. Склонируйте проект к себе локально на устройство
2. Задайте переменные окружения по аналогии с файлом 'ci.env' в директории 'deployment'
3. В корневой директории проекта выполните приведенную ниже команду, чтобы создать образы и контейнер докера:

```
docker-compose up
```

4. Для заполнение библиотеки необходимо находясь в коренной директории в консоли прописать команду ниже:

```
docker-compose run --rm backend_module_project_3 private_library library-filling <our_tag1> <our_tag2>
```

#### Примеры использования
Примеры использования находятся в отдельной директории "docs"

#### Автор
Vurgul: https://github.com/Vurgul