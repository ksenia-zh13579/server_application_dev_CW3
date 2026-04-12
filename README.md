# Разработка серверных приложений - Контрольная работа №2
--

## Заполнение переменных окружения

Для установки значений нужных переменных окружения нужно создать файл ".env", скопировать туда названия переменных из файла ".env.example" и дописать соответствующие значения каждой из них. Файл ".env" нужно добавить в .gitignore.
--

## Создание таблицы в базе данных PostgreSQL

Для создания таблицы, с которой должна вестись работа в задании 8.2, нужно:

 - создать базу данных в PostgreSQL c помощью pgadmin или терминала;
 - прописать путь до неё в переменную окружения "DATABASE_URL";
 - в терминале перейти в папку основного приложения и выполнить скрипт "python init_db_pg.py".
--

## Запуск приложения

Для запуска API нужно:
 - установить зависимости: pip install -r requirements.txt
 - запустить сервер: uvicorn app:app --reload
--

## Тестирование заданий

Для тестирования работы заданий необходимо раскомментировать код с соответствующими эндпойнтами в файле "app.py" (а также код в файле "database.py" для задания 6.1) и выполнить следующие запросы:

### Для задания 6.1:
 - Успешный логин: curl -u user1:pass1 http://localhost:8000/login

 - Неверный пароль: curl -u user1:wrongpass http://localhost:8000/login
--

### Для задания 6.2:
 - Регистрация: curl -X POST -H "Content-Type: application/json" -d '{"username":"user1" "password":"pass1"}' http://localhost:8000/register

 - Успешный логин: curl -u user1:pass1 http://localhost:8000/login

 - Неверный пароль: curl -u user1:wrongpass http://localhost:8000/login
--

### Для задания 6.3:
 - DEV-режим: curl -u valid_user:valid_password http://localhost:8000/docs
 - PROD-режим: curl http://localhost:8000/docs  # Должен вернуть 404
--

### Для задания 6.4:

#### Пример запроса:
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}

 #### Пример ответа (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}

 #### Пример ответа (401 Unauthorized):
{
  "detail": "Invalid credentials"
}
--

### Для задания 6.5:

 #### Регистрация:
POST /register  
Content-Type: application/json  

{ "username": "alice", "password": "qwerty123" }  

Ответ (201):  
{ "message": "New user created" }  

Ответ (409):  
{ "detail": "User already exists" }  

 #### Логин:
POST /login  
Content-Type: application/json  

{ "username": "alice", "password": "qwerty123" }  

Ответ (200):  
{ "access_token": "eyJhbGci...", "token_type": "bearer" }  

Ответ (404):  
{ "detail": "User not found" }  

Ответ (401):  
{ "detail": "Authorization failed" }  

 #### Protected Resource:
GET /protected_resource  
Authorization: Bearer eyJhbGci...  

Ответ (200):  
{ "message": "Access granted" }  
--

### Для задания 7.1:

 #### Авторизация:
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username":"special_user","password":"specialpass"}'

Результат:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

 #### Доступ к защищенному ресурсу:
curl -H "Authorization: Bearer {TOKEN}" http://localhost:8000/protected_resource

Результат (успешно):
{
  "message": f"Hello, {current_user.username}! This is a protected resource only for admins."
}

 #### Попытка добавления нового продукта:
  - успешно: 
 curl -X POST -H "Authorization: Bearer {TOKEN}" http://localhost:8000/products

 Результат:
 {
  "message": "New product successfully added"
 }

  - ошибка: 
 curl -X POST -H "Authorization: Bearer {TOKEN}" http://localhost:8000/products

 Результат:
 {
  "detail": "Недостаточно прав для доступа. Требуется одно из разрешений: write:products"
 }
--

### Для задания 8.1:

curl -X 'POST' 'http://127.0.0.1:8000/register' \
-H 'Content-Type: application/json' \
-d '{"username": "test_user", "password": "12345"}'
--

### Для задания 8.2:

 #### Пример POST-запроса create (Создать Todo):
POST /todos
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Пример ответа (201 Created):
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}

 #### Пример GET-запроса read (Получить Todo - ID: 1):
GET /todos/1

Пример ответа (200 OK):
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
--

## Сведения

Работу выполнила Жужлева Ксения Александровна, группа ЭФБО-05-24.