#### 1. Создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
- Tаблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
- Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
- Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
* Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
* Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
* Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

#### 2. Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
#### 3. Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.