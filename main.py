import ttkbootstrap as ttk
import os
from tkinter import *

class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()


    def init_main(self):
        label_title = ttk.Label(self, text='Авторизация в системе')
        label_title.pack()

        self.user_img = ttk.PhotoImage(file='img/user.png')
        btn_user = ttk.Button(self, text='Пользователь', image=self.user_img, command=self.user)
        btn_user.place(relx=0.5, rely=0.5, anchor=CENTER)
        btn_user.pack()

        label_user = ttk.Label(self, text='Пользователь')
        label_user.pack()

        self.admin_img = ttk.PhotoImage(file='img/admin.png')
        btn_admin = ttk.Button(self, text='Администратор', image=self.admin_img, command=self.admin)
        btn_admin.place(relx=1, rely=1, anchor=CENTER)
        btn_admin.pack()

        label_admin = ttk.Label(self, text='Администратор')
        label_admin.pack()

    def user(self):
        root.withdraw()
        os.system("python user.py")
        root.destroy()

    def admin(self):
        root.withdraw()
        os.system("python admin.py")
        root.destroy()


if __name__ == "__main__":
    root = ttk.Window(themename='minty')
    app = Main(root)
    app.pack()
    root.title('Авторизация')
    root.iconbitmap('')
    root.geometry('800x500')
    root.resizable(False, False)
    root.mainloop()