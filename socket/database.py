import sqlite3
from sqlite3 import Error
from datetime import datetime

class library_database():
    def __init__(self,db_name):
        self.conn = None
        self.db_name=db_name
        try:
            self.conn = sqlite3.connect(db_name)
        except Error as e:
            print("SQL Connection Error!")

    def __query(self, query,parameters=()):
        if self.conn is not None:
            '''try:
                c = self.conn.cursor()
                c.execute(query,parameters)
                self.conn.commit()
                return c.fetchall()
            except:
                raise Exception("Failed to executed query!")'''
            c = self.conn.cursor()
            c.execute(query,parameters)
            self.conn.commit()
            return c.fetchall()

    def create_tables(self):
        query = 'CREATE TABLE ACCOUNT (\
                USERNAME CHAR(64),\
                PASSWORD CHAR(64),\
                PRIMARY KEY (USERNAME)\
            )'
        self.__query(query)
        query = 'CREATE TABLE BOOK (\
                ID CHAR(8),\
                NAME CHAR(64),\
                TYPE CHAR(64),\
                AUTHOR CHAR(30),\
                PUBLISH_YEAR,\
                PATH CHAR(64),\
                PRIMARY KEY (ID)\
            )'
        self.__query(query)
    
    def add_book(self, id, name = 'NULL', type = 'NULL', author = 'NULL', publish_year = 'NULL', path = 'NULL'):
        query = 'INSERT INTO BOOK VALUES (?,?,?,?,?,?)'
        self.__query(query, parameters = (id, name, type, author, publish_year, path))

    def log_in(self, username, password):
        try:
            query = 'SELECT * FROM ACCOUNT WHERE USERNAME = ?'
            db_table = self.__query(query,(username,))
            if db_table[0][1] == password:
                return True
            raise Exception
        except:
            return False

    def is_exists(self, username):
        query = 'SELECT * FROM ACCOUNT WHERE USERNAME = ?'
        db_table = self.__query(query,(username,))
        return len(db_table) > 0

    def sign_up(self, username, password):
        try:
            if (self.is_exists(username)): #already sign up
                raise Exception
            query = 'INSERT INTO ACCOUNT VALUES (?,?)'
            parameters = (username, password)
            self.__query(query, parameters)
            return True
        except:
            return False

    def view(self):
        query = 'SELECT ID, NAME, AUTHOR, PUBLISH_YEAR FROM BOOK'
        db_table = self.__query(query)
        return db_table

    def get_books_by_id(self,ID):
        query = 'SELECT ID, NAME, AUTHOR, PUBLISH_YEAR FROM BOOK WHERE ID = ?'
        db_table = self.__query(query,(ID,))
        return db_table

    def get_books_by_name(self,name):
        query = 'SELECT ID, NAME, AUTHOR, PUBLISH_YEAR FROM BOOK WHERE NAME = ?'
        db_table = self.__query(query,(name,))
        return db_table

    def get_books_by_type(self,Type):
        query = 'SELECT ID, NAME, AUTHOR, PUBLISH_YEAR FROM BOOK WHERE TYPE = ?'
        db_table = self.__query(query,(Type,))
        return db_table

    def get_books_by_author(self,author):
        query = 'SELECT ID, NAME, AUTHOR, PUBLISH_YEAR FROM BOOK WHERE AUTHOR = ?'
        db_table = self.__query(query,(author,))
        return db_table

    def get_book_content(self, id):
        query = 'SELECT PATH FROM BOOK WHERE ID = ?'
        dir = self.__query(query,(id,))
        data = b' '
        ext = 'None'
        if (len(dir) > 0):
            path = dir[0][0]
            f = open(path, "rb")
            data = f.read()
            f.close()
            ext = path.split('.')[-1]
        return (ext, data)

'''db = library_database('library')
db.create_tables()
db.add_book('1', 'Mans search for meaning', 'A A', 'Viktor Frankl', '2001', 'D:\\Sách\\Mans search for meaning.pdf')
print(db.sign_up('bachtam22082001', 'bachtam'))
print(db.sign_up('bachtam22082001', '123456'))
print(db.log_in('bachtam22082001', 'bachtam'))
print(db.get_books_by_name('Mans search for meaning'))
with open("test1.pdf", "wb") as f:
    f.write(db.get_book_content('1'))'''