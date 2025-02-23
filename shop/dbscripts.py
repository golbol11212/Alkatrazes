import sqlite3 as sql


# CREATE (создание таблиц, функций, схем и.т.д)
# INSERT (вставить новую запись в таблицу)
# UPDATE (обновить существующую(-ие) записи)
# DELETE (удалить из таблицы записи)
# SELECT (достать из таблиці записи)

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

        
        
        self.connection = None
        self.cursor = None
        
    def connect(self):
        self.connection = sql.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        
    def add_user(self, hashed_login, hashed_password, img):
        self.connect()
        
        self.cursor.execute(
            """
            INSERT INTO accounts (login, password, img) 
            VALUES (?, ?, ?)
            """, [hashed_login, hashed_password, img]
        ) # вставить в таблицу accounts (в ее колонки login и password) значения аргументов login и password
        self.connection.commit() # сохранить
        
        self.disconnect()

    def check_is_user_exists(self, login):
        self.connect()
        
        self.cursor.execute(
            """
            SELECT * FROM accounts WHERE login = ?
            """, [login]
        ) # достать из таблицы accounts все записи, у которых в колонке login написано значение аргумент login
        data = self.cursor.fetchone() # получаю 1 (!) результат предыдущего SQL запроса
        
        self.disconnect()
        
        return data is not None # возвращаю True либо False
    
    def check_is_right_userdata(self, login, hashed_password):
        self.connect()
        
        self.cursor.execute(
            """
            SELECT * FROM accounts WHERE login = ? AND password = ?
            """, [login, hashed_password]
        )
        data = self.cursor.fetchone()
        
        self.disconnect()
        
        return data is not None
    
    def get_user_data_by_login(self, login):
        self.connect()
        
        query = "SELECT * FROM accounts WHERE login = ?"
        self.cursor.execute(query, (login,))  # Выполнение запроса

        data = self.cursor.fetchone()  # Получаем одну строку

        self.disconnect()
        
        return data
    
    def get_user_data_by_login_self(self, login):
        self.connect()

        query = "SELECT password FROM accounts WHERE login = ?"  # Выбираем только пароль
        self.cursor.execute(query, (login,))

        data = self.cursor.fetchone()  # Получаем одну строку

        self.disconnect()
        
        return data[0] if data else None  # Возвращаем пароль или None


    
    def add_shop(self, login, name, inform, categories, prise, img, com):
        self.connect()
        
        self.cursor.execute(
            """
            INSERT INTO shop (login, name, inform, categories, prise, img, com) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [login, name, inform, categories, prise, img, com]
        )
        self.connection.commit()

    def sell(self):
        self.connect()
        
        self.cursor.execute(
            """
            SELECT * FROM shop
            """
        )
        data = self.cursor.fetchall()
        
        self.disconnect()
        
        return data
    
    def get_comments(self):
        self.connect()
        
        self.cursor.execute(
            """
            SELECT * FROM coments
            """
        )
        data = self.cursor.fetchall()
        
        self.disconnect()
        
        return data
    
    def add_comment(self, item_name, user_login, comment_text):
        self.connect()
        try:
            self.cursor.execute(
                """
                INSERT INTO coments (item, user, com)
                VALUES (?, ?, ?)
                """,
                (item_name, user_login, comment_text)
            )
            self.connection.commit()
        except sql.Error as e:
            print("Помилка додавання коментаря:", e)
        finally:
            self.disconnect()

    