from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from DBMS_Project import *
from db import database
class Login:
  def __init__(self,root):
    self.root=root
    self.DB=database('lb.db')
    self.root.title('Login System')
    self.root.geometry('1200x580')
    self.root.resizable(False,False)
    # BG
    self.bg=ImageTk.PhotoImage(file="images/login.jpg")
    self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
    #=== Login
    Frame_login=Frame(self.root,bg='white')
    Frame_login.place(x=250,y=190,height=250,width=420)

    title=Label(Frame_login,text="Login Here",font=("Impact",35,"bold"),bg="white").place(x=120,y=0)

    self.User=Label(Frame_login,text="Username ",font=("Goudy old style",15,"bold"),bg="white")
    self.User.place(x=20,y=50)
    self.Pass=Label(Frame_login,text="Password",font=("Goudy old style",15,"bold"),bg="white")
    self.Pass.place(x=20,y=115)

    self.txt_user=Entry(Frame_login,font=("times new roman",15,"bold"),bg="white")
    self.txt_user.place(x=20,y=80,width=350,height=35)
    self.txt_pass=Entry(Frame_login,show='*',font=("times new roman",15,"bold"),bg="white")
    self.txt_pass.place(x=20,y=150,width=350,height=35)

    self.checkbox=Checkbutton(Frame_login,text="Show password",bg='white',command=self.showPW)
    self.checkbox.place(x=20,y=190)
    self.reg=Button(Frame_login,text='Register an account ?',bg='white',bd=0,command=self.Register,font=('times new roman',12))
    self.reg.place(x=20,y=220)
    self.confirm=Button(Frame_login,text='Sign in',bg='#344fa1',fg='white',bd=0,command=self.Login,font=('times new roman',12))
    self.confirm.place(x=330,y=220)

  def showPW(self):
    if self.txt_pass['show']=='*':
        self.txt_pass.config(show='')
        return
    self.txt_pass['show']='*'
  def Register(self):
    self.reg.config(text="Go back",command=self.goback)
    self.confirm.config(text="Sign up",command=self.SignUp)
    return
  def goback(self):
    self.reg.config(text="Register an account ?",command=self.Register)
    self.confirm.config(text="Sign in",command=self.Login)
    return
  def Login(self):
    if self.DB.Login(self.txt_user.get(),self.txt_pass.get()):
        root.destroy()
        #Open new window
        newroot = Tk()
        application = Window_user(newroot,self.DB)
        newroot.mainloop()
        return
    messagebox.showinfo("Notification","Incorrect Username or password")
    return
  def run_query(self, query, parameters=()):
        with sqlite3.connect('lb.db') as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result.fetchall()  
  def SignUp(self):

    if self.DB.Register(self.txt_user.get(),self.txt_pass.get()):
        messagebox.showinfo("Notification","Sign Up in successfully")
        self.goback()
    else:
        messagebox.showinfo("Notification",'Account already exists..') 

root=Tk()
obj=Login(root)
root.mainloop()