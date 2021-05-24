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
            try:
                c = self.conn.cursor()
                c.execute(query,parameters)
                self.conn.commit()
                return c.fetchall()
            except Error as e:
                print("Query SQL Error!")
                raise e

    def log_in(self, username, password):
        query = 'SELECT * FROM account WHERE Username = ?'
        db_table = self.__query(query,(username,))
        for data in db_table:
            if data[1] == password:
                return 1
        return 0

    def sign_up(self, username, password):
        try:
            query = 'INSERT INTO account VALUES (?,?)'
            parameters = (username, password)
            self.__query(query, parameters)
            return 1
        except:
            return 0

    def view(self):
        query = 'SELECT * FROM Book'
        db_table = self.__query(query)
        return db_table

    def get_books_by_id(self,ID):
        query = 'SELECT * FROM Book WHERE ID = ?'
        db_table = self.__query(query,(ID,))
        return db_table

    def get_books_by_name(self,name):
        query = 'SELECT * FROM Book WHERE Name = ?'
        db_table = self.__query(query,(name,))
        return db_table

    def get_books_by_type(self,Type):
        query = 'SELECT * FROM Book WHERE Type = ?'
        db_table = self.__query(query,(Type,))
        return db_table

    def get_books_by_author(self,author):
        query = 'SELECT * FROM Book WHERE Author = ?'
        db_table = self.__query(query,(author,))
        return db_table

    def get_book_content(self,name):
        query = 'SELECT path FROM Book WHERE Name = ?'
        Dir = self.__query(query,(name,))
        data = b''
        if Dir != []:
            try:
                f = open("BOOK\\"+Dir[0][0], "rb")
                data = f.read()
            except: 
                pass
            f.close()
        return data