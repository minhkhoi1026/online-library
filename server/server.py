import datetime
import queue
import logging
import signal
import time
import threading
from tkinter import messagebox
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, N, S, E, W
from library_server import *
from utils import stoppabe_thread

logger = logging.getLogger(__name__)

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class App:
    def __init__(self, root, host = HOST, port = PORT, db_name = DB_NAME, max_conn = MAX_CONN):
        print(max_conn)
        self.root = root
        root.title('Logging Handler')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        console_frame = ttk.Frame(root)
        console_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        self.console = ConsoleUi(console_frame)
        self.server_obj = library_server(logger = logger, host = host, port = port, db_name = db_name, max_conn = max_conn)
        self.server = stoppabe_thread(target = self.server_obj.run, daemon = True)
        self.server.start()
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

        Chooser = tk.Menu()
        itemone = tk.Menu()
        itemone.add_command(label='Close all connect', command=self.server_obj.close_all_connect)
        itemone.add_separator()
        itemone.add_command(label='Exit', command=self.quit)

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_command(label='Close all connect', command=self.server_obj.close_all_connect)
        Chooser.add_command(label='Exit', command=self.quit)
        self.root.config(menu=Chooser)

    def quit(self, *args):
        self.server.stop()
        self.root.destroy()

def openSV(Entry_num,root):
    num=Entry_num.get()
    try:
        num=int(num)
    except:
        messagebox.showinfo("Notification",'Invalid input number')
        return
    if num >0:
        root2 = tk.Tk()
        app = App(root2,max_conn=num)
        root.destroy()
        app.root.mainloop()
        return
    else:
        messagebox.showinfo("Notification",'Negative input number')
        return




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    tk.Label(root, text='Max client:').grid(row=2, column=1, sticky=W)
    number = tk.Entry(root)
    number.grid(row=2, column=2)
    '''Add Button'''
    ok=tk.Button(root, text='Ok',padx=30, command=lambda x=number, y=root: openSV(x,y))
    ok.grid(row=3, column=2)
    root.mainloop()