''' IMPORTING NECCESARY PACKAGES'''

from tkinter import *
from tkinter import ttk
import datetime
import time
import tkinter.messagebox
from tkinter import filedialog
import sqlite3
from db import database


''' CREATING CLASS'''
class Read:
    def __init__(self,root,string,name):
        self.root = Toplevel(root)
        self.root.geometry("1200x710")
        self.toolbar_frame = Frame(self.root)
        self.toolbar_frame.pack(fill=X)

        # Create Main Frame
        self.my_frame = Frame(self.root)
        self.my_frame.pack(pady=5)

        # Create our Scrollbar For the Text Box
        self.text_scroll = Scrollbar(self.my_frame)
        self.text_scroll.pack(side=RIGHT, fill=Y)

        # Horizontal Scrollbar
        self.hor_scroll = Scrollbar(self.my_frame, orient='horizontal')
        self.hor_scroll.pack(side=BOTTOM, fill=X)

        # Create Text Box
        self.my_text = Text(self.my_frame, width=97, height=25,state="disabled", font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=self.text_scroll.set, wrap="none", xscrollcommand=self.hor_scroll.set)
        self.my_text.pack()
        self.Print(string)
        # Configure our Scrollbar
        self.text_scroll.config(command=self.my_text.yview)
        self.hor_scroll.config(command=self.my_text.xview)

        # Create Menu
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        # Add File Menu
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Book", menu=self.file_menu)
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)



        # Add Options Menu
        self.options_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Night Mode On", command=self.night_on)
        self.options_menu.add_command(label="Night Mode Off", command=self.night_off)


        # Add Status Bar To Bottom Of App
        self.status_bar = Label(self.root, text=name+'          ', anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=15)

    def night_on(self):
        main_color = "#000000"
        second_color = "#373737"
        text_color = "green"

        self.root.config(bg=main_color)
        self.status_bar.config(bg=main_color, fg=text_color)
        self.my_text.config(bg=second_color,fg='white')
        self.toolbar_frame.config(bg=main_color)
        # toolbar buttons
        # file menu colors
        self.file_menu.config(bg=main_color, fg=text_color)

        self.options_menu.config(bg=main_color, fg=text_color)

    def save_as_file(self):
        text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if text_file:

            # Save the file
            text_file = open(text_file, 'w')
            text_file.write(self.my_text.get(1.0, END))
            # Close the file
            text_file.close()


    def night_off(self):
        main_color = "SystemButtonFace"
        second_color = "SystemButtonFace"
        text_color = "black"

        self.root.config(bg=main_color)
        self.status_bar.config(bg=main_color, fg=text_color)
        self.my_text.config(bg="white",fg='black')
        self.toolbar_frame.config(bg=main_color)
        # toolbar buttons

        # file menu colors
        self.file_menu.config(bg=main_color, fg=text_color)
        self.options_menu.config(bg=main_color, fg=text_color)
    def Print(self,S):
        string=S
        ### START CODE HERE ###
        self.my_text.configure(state="normal")
        self.my_text.insert(END,string)
        self.my_text.configure(state="disabled")
        ### END CODE HERE ###
        return

class Window_user:
    db_name = 'lb.db'

    def __init__(self, root,DB):
        self.root = root
        self.DB=DB
        self.root.geometry('530x460+600+200')
        self.root.title('Online library')

        '''Logo and Title'''

        self.photo = PhotoImage(file='icon.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='Welcome to online library', fg='dark blue')
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
        self.tree = ttk.Treeview(height=10, column=['', '', '', ''])
        self.tree.grid(row=9, column=0, columnspan=2)
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=100)
        self.tree.heading('#1', text='Bookname')
        self.tree.column('#1', width=225)
        self.tree.heading('#2', text='Type')
        self.tree.column('#2', width=75)
        self.tree.heading('#3', text='Author')
        self.tree.column('#3', width=50)
        self.tree.heading('#4', text='Year')
        self.tree.column('#4', width=50,stretch=False)

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
        self.B_read = Button(self.root, text="Read the book",command=self.read_box)
        self.B_read.place(x=405,y=420)
        self.B_download = Button(self.root, text="Download the book",command=self.download)
        self.B_download.place(x=10,y=420)

        ''' Menu Bar '''
        Chooser = Menu()
        itemone = Menu()


        itemone.add_command(label='Read Book', command=self.edit)
        itemone.add_separator()
        itemone.add_command(label='Exit', command=self.ex)

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_command(label='Read Book', command=self.edit)
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



    def read_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            self.message['text'] = 'Please select a Book to read!'
            return

        ID = self.tree.item(self.tree.selection())['text']

        string =self.DB.ReadBook(ID)

        if string != None:
            self.read_window=Read(self.root,string.decode("utf-8"),self.tree.item(self.tree.selection())['values'][0])


    def edit(self):
        ed = tkinter.messagebox.askquestion('Read information', 'Want to read this book?')
        if ed == 'yes':
            self.read_box()
    def download(self):
        text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if text_file:

            # Save the file
            text_file = open(text_file, 'wb')
            text_file.write(b'hello')
            # Close the file
            text_file.close()

    '''EXIT'''
    def ex(self):
        exit = tkinter.messagebox.askquestion('Exit Application','Are you sure you want to close this application?')
        if exit == 'yes':
            self.root.destroy()


