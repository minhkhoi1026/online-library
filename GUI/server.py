from tkinter import *
from PIL import ImageTk
from tkinter import filedialog
from tkinter import messagebox
class server(object):
    def __init__(self, master):
        self.master = master
        self.master.geometry("450x250")
        #self.master.resizable(width=False,height=False)
        self.my_frame1 = Frame(self.master)
        self.my_scrollbar = Scrollbar(self.my_frame1, orient=VERTICAL)
        self.my_text = Text(self.my_frame1,state="disabled", width=50, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_text.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        self.my_frame1.place(x=10,y=50,width=300,height=150)
        self.my_text.pack(pady=15)
        self.buttonSend = Button(self.master,text="Send",padx=40,pady=50)
        self.buttonSend.place(x=320,y=60)
        self.Print('hello')
    def Print(self,S):
        string=S
        ### START CODE HERE ###
        self.my_text.configure(state="normal")
        self.my_text.insert(END,string)
        self.my_text.configure(state="disabled")
        ### END CODE HERE ###
        return

if __name__ == "__main__":
    root = Tk()
    wd = server(root)
    root.mainloop()