import sqlite3
from sqlite3 import Error
from datetime import datetime

class database():
    def __init__(self,db_name):
        self.conn = None;
        self.db_name=db_name
        try:
            self.conn = sqlite3.connect(db_name)
        except Error as e:
            print("SQL Connection Error!")

    def __Query(self, query,parameters=()):
        if self.conn is not None:
            try:
                c = self.conn.cursor()
                c.execute(query,parameters)
                self.conn.commit()
                return c.fetchall()
            except Error as e:
                print("Query SQL Error!")
                raise e;

    def Login(self, username, password):
        query = 'SELECT * FROM account WHERE Username = ?'
        db_table = self.__Query(query,(username,))
        for data in db_table:
            if data[1]==password:
                return 1
        return 0

    def Register(self, username, password):
        try:
            query = 'INSERT INTO account VALUES (?,?)'
            parameters = (username, password)
            self.__Query(query, parameters)
            return 1

        except:
            return 0

    def Bview(self):
        query = 'SELECT * FROM Book'
        db_table = self.__Query(query)
        return db_table
    def BSearch_ID(self,ID):
        query = 'SELECT * FROM Book WHERE ID = ?'
        db_table = self.__Query(query,(ID,))
        return db_table
    def BSearch_name(self,name):
        query = 'SELECT * FROM Book WHERE Name = ?'
        db_table = self.__Query(query,(name,))
        return db_table
    def BSearch_type(self,Type):
        query = 'SELECT * FROM Book WHERE Type = ?'
        db_table = self.__Query(query,(Type,))
        return db_table
    def BSearch_author(self,author):
        query = 'SELECT * FROM Book WHERE Author = ?'
        db_table = self.__Query(query,(author,))
        return db_table

    def ReadBook(self,name):
        query = 'SELECT path FROM Book WHERE Name = ?'
        Dir = self.__Query(query,(name,))
        if Dir != []:
            f = open("BOOK\\"+Dir[0][0], "rb")
            print(f.read())
            f.close()
        return