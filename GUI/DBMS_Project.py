''' IMPORTING NECCESARY PACKAGES'''

from tkinter import *
from tkinter import ttk
import datetime
import time
import tkinter.messagebox
import sqlite3
from db import database

''' IMPORTING SUCCESSFUL'''

''' CREATING CLASS'''


class Window_user:
    db_name = 'lb.db'

    def __init__(self, root,DB):
        self.root = root
        self.DB=DB
        self.root.geometry('655x525+600+200')
        self.root.title('Students Data')

        '''Logo and Title'''

        self.photo = PhotoImage(file='icon.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='School Portal System', fg='dark blue')
        self.label1.grid(row=8, column=0)

        self.option = [
            "ID",
            "Name",
            "Type",
            "Author"
        ]   
        ''' New Books '''
        self.frame = LabelFrame(self.root, text='Book search')
        self.frame.grid(row=0, column=1)

        self.chosen = StringVar()
        self.chosen.set(self.option[0])
        self.drop = OptionMenu(self.frame, self.chosen, *self.option,command=self.fix)
        Label(self.frame, text='Search by:').grid(row=1, column=1, sticky=W)
        self.drop.grid(row=1, column=2)

        self.N_text=Label(self.frame, text='ID:')
        self.N_text.grid(row=2, column=1, sticky=W)
        self.S_text = Entry(self.frame)
        self.S_text.grid(row=2, column=2)

        '''Add Button'''
        self.search=Button(self.frame, text='Search book', command=self.view_book_ID)
        self.search.grid(row=3, column=2)

        '''Message Display'''
        self.message = Label(text='', fg='Red')
        self.message.grid(row=8, column=1)

        '''Database Table display box '''
        self.tree = ttk.Treeview(height=10, column=['', '', '', '', '', ''])
        self.tree.grid(row=9, column=0, columnspan=2)
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='Bookname')
        self.tree.column('#1', width=100)
        self.tree.heading('#2', text='Type')
        self.tree.column('#2', width=100)
        self.tree.heading('#3', text='Author')
        self.tree.column('#3', width=90)
        self.tree.heading('#4', text='Year')
        self.tree.column('#4', width=150)
        self.tree.heading('#5', text='Nation')
        self.tree.column('#5', width=120)
        self.tree.heading('#6', text='Rate')
        self.tree.column('#6', width=40, stretch=False)

        '''Time and Date'''

        def tick():
            d = datetime.datetime.now()
            today = '{:%B %d,%Y}'.format(d)

            mytime = time.strftime('%I:%M:%S%p')
            self.lblInfo.config(text=(mytime + '\t' + today))
            self.lblInfo.after(200, tick)

        self.lblInfo = Label(font=('arial', 10, 'bold'), fg='Dark green')
        self.lblInfo.grid(row=10, column=0, columnspan=2)
        tick()

        ''' Menu Bar '''
        Chooser = Menu()
        itemone = Menu()

        itemone.add_command(label='Add Book', command=self.add)
        itemone.add_command(label='Read Book', command=self.edit)
        itemone.add_command(label='Delete Book', command=self.delet)
        itemone.add_separator()
        itemone.add_command(label='Help', command=self.help)
        itemone.add_command(label='Exit', command=self.ex)

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_command(label='Add', command=self.add)
        Chooser.add_command(label='Read Book', command=self.edit)
        Chooser.add_command(label='Delete', command=self.delet)
        Chooser.add_command(label='Help', command=self.help)
        Chooser.add_command(label='Exit', command=self.ex)

        root.config(menu=Chooser)
        self.view_book()

    ''' View Database Table'''
    def fix(self,a):
        self.N_text.config(text=self.chosen.get()+':')
        if a==self.option[0]:
            self.search.config(command=self.view_book_ID)
        elif a==self.option[1]:
            self.search.config(command=self.view_book_name)
        elif a==self.option[2]:
            self.search.config(command=self.view_book_type)
        elif a==self.option[3]:
            self.search.config(command=self.view_book_author)

    def view_book(self):
        books = self.tree.get_children()
        for element in books:
            self.tree.delete(element)
        db_table = self.DB.Bview()
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:-1])
    def view_book_ID(self):
        books = self.tree.get_children()
        for element in books:
            self.tree.delete(element)
        db_table=self.DB.BSearch_ID(self.S_text.get())
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:-1])
    def view_book_name(self):
        books = self.tree.get_children()
        for element in books:
            self.tree.delete(element)
        print(self.S_text.get())
        db_table=self.DB.BSearch_name(self.S_text.get())
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:-1])
    def view_book_type(self):
        books = self.tree.get_children()
        for element in books:
            self.tree.delete(element)
        db_table=self.DB.BSearch_type(self.S_text.get())
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:-1])
    def view_book_author(self):
        books = self.tree.get_children()
        for element in books:
            self.tree.delete(element)
        ### 

        db_table=self.DB.BSearch_author(self.S_text.get())

        ###
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:-1])


    ''' Add New Book '''

    def add_book(self):
        try:
            query = 'INSERT INTO Book VALUES (?,?,?,?,?,?,?)'
            parameters = (int(self.ID.get()),self.bookname.get(), self.type.get(), self.Author.get(),
                          int(self.year.get()), self.nation.get(), float(self.rate.get()))
            print(self.run_query(query, parameters))
            self.message['text'] = 'Book {} {} added!'.format(self.bookname.get(), self.type.get())

            '''Empty the fields'''
            self.bookname.delete(0, END)
            self.type.delete(0, END)
            self.Author.delete(0, END)
            self.year.delete(0, END)
            self.nation.delete(0, END)
            self.rate.delete(0, END)

        except:
            self.message['text'] = 'Fields not completed! Complete all fields...'

        self.view_book()

    '''Function for using buttons'''

    def add(self):
        ad = tkinter.messagebox.askquestion('Add Book', 'Do you want to add a New Book?')
        if ad == 'yes':
            self.add_book()

    ''' Deleting a Book '''

    def delete_book(self):
        # To clear output
        self.message['text'] = ''

        try:
            # why 1? --Can be anything
            self.tree.item(self.tree.selection())['values'][1]

        except IndexError as e:
            self.message['text'] = 'Please select a book to delete!'
            return

        # Again clear output
        self.message['text'] = ''
        # ???why text
        number = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Book WHERE ID = ?'
        # Why comma
        self.run_query(query, (number,))
        self.message['text'] = 'Book {} deleted!'.format(number)

        # Printing new database

        self.view_book()

    # Function to add functionality in buttons

    def delet(self):
        de = tkinter.messagebox.askquestion('Delete Book', 'Are you sure you want to delete this book?')
        if de == 'yes':
            self.delete_book()

    '''EDIT RECORD'''

    '''CREATING A POP UP WINDOW FOR EDIT'''

    def edit_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            self.message['text'] = 'Please select a Book to Edit!'
            return

        ID = self.tree.item(self.tree.selection())['text']
        '''
        lname = self.tree.item(self.tree.selection())['values'][1]
        uname = self.tree.item(self.tree.selection())['values'][2]
        email = self.tree.item(self.tree.selection())['values'][3]
        subject = self.tree.item(self.tree.selection())['values'][4]
        age = self.tree.item(self.tree.selection())['values'][5]

        self.edit_root = Toplevel()
        self.edit_root.title('Edit Infomation')
        self.edit_root.geometry('305x355+600+200')

        Label(self.edit_root, text='Old Bookname').grid(row=0, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=fname), state='readonly').grid(row=0,
                                                                                                          column=2)
        Label(self.edit_root, text='New Bookname').grid(row=1, column=1, sticky=W)
        new_fname = Entry(self.edit_root , textvariable=StringVar(self.edit_root, value=fname))
        new_fname.grid(row=1, column=2)

        Label(self.edit_root, text='Old Type').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=lname), state='readonly').grid(row=2,
                                                                                                          column=2)
        Label(self.edit_root, text='New Type').grid(row=3, column=1, sticky=W)
        new_lname = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=lname))
        new_lname.grid(row=3, column=2)

        Label(self.edit_root, text='Old Author').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=uname), state='readonly').grid(row=4,
                                                                                                          column=2)
        Label(self.edit_root, text='New Author').grid(row=5, column=1, sticky=W)
        new_uname = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=uname))
        new_uname.grid(row=5, column=2)

        Label(self.edit_root, text='Old Year').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=email), state='readonly').grid(row=6,
                                                                                                          column=2)
        Label(self.edit_root, text='New Year').grid(row=7, column=1, sticky=W)
        new_email = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=email))
        new_email.grid(row=7, column=2)

        Label(self.edit_root, text='Old Nation').grid(row=8, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=subject), state='readonly').grid(row=8,
                                                                                                            column=2)
        Label(self.edit_root, text='New Nation').grid(row=9, column=1, sticky=W)
        new_subject = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=subject))
        new_subject.grid(row=9, column=2)

        Label(self.edit_root, text='Old Rate').grid(row=10, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=age), state='readonly').grid(row=10,
                                                                                                        column=2)
        Label(self.edit_root, text='New Rate').grid(row=11, column=1, sticky=W)
        new_age = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=age))
        new_age.grid(row=11, column=2)

        Button(self.edit_root, text='Save Changes', command=lambda: self.edit_book(new_fname.get(), fname, new_lname.get(), lname, new_uname.get(), uname, new_email.get(), email,new_subject.get(), subject, new_age.get(), age)).grid(row=12, column=2, sticky=W)

        self.edit_root.mainloop()'''
        self.DB.ReadBook(ID)

    def edit_book(self, new_bname, bname, new_btype, btype, new_author, author, new_year, year, new_nation, nation,
                    new_rate, rate):
        query = 'UPDATE Book SET name=?, Type=?, Author=?, Year=?, Nation=?, Rate=? WHERE ' \
                'name= ? AND Type=? AND Author=? AND Year=? AND Nation=? AND Rate=?'

        parameters = (new_bname, new_btype, new_author, int(new_year), new_nation, float(new_rate), bname, btype, author, int(year),nation, float(rate))
        self.run_query(query, parameters)
        self.edit_root.destroy()
        self.message['text'] = '{} details are changed to {}'.format(bname, new_bname)
        self.view_book()

    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit information', 'Want to Edit this book?')
        if ed == 'yes':
            self.edit_box()

    '''HELP'''
    def help(self):
        tkinter.messagebox.showinfo('Log','Report Sent!')

    '''EXIT'''
    def ex(self):
        exit = tkinter.messagebox.askquestion('Exit Application','Are you sure you want to close this application?')
        if exit == 'yes':
            self.root.destroy()


'''MAIN'''

if __name__ == '__main__':
    root = Tk()
    # root.geometry('585x515+500+200')
    application = School_Portal(root)
    root.mainloop()
