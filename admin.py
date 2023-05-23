import ttkbootstrap as ttk
import sqlite3
from tkinter import *
from ttkbootstrap.dialogs import Messagebox

class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()


    def init_main(self):
        label_title = ttk.Label(self, text='Авторизация в системе/Администратор')
        label_title.pack()

        label_login = ttk.Label(self, text='Введите логин')
        label_login.pack()
        self.entry_login = ttk.Entry(self, bootstyle="success")
        self.entry_login.pack(pady=5)

        label_password = ttk.Label(self, text='Введите пароль')
        label_password.pack()
        self.entry_password = ttk.Entry(self, bootstyle="success")
        self.entry_password.pack(pady=5)

        btn_authorization = ttk.Button(self, text='Авторизация', command=self.check_login_and_password)
        btn_authorization.pack()

    def check_login_and_password(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        with sqlite3.connect("database/database.db") as file_db:
            cur = file_db.cursor()
        find_user = f"SELECT id FROM users WHERE login = '{login}' AND password = '{password}' AND admin = '1'"
        cur.execute(find_user)
        results = cur.fetchall()
        global id
        id = []
        for i in results:
            id += i
        if results:
            success = Messagebox.show_info('Успешная авторизация!')
            root.withdraw()
            self.open_shop_index()
        else:
            dont_success = Messagebox.show_info('Нет прав доступа!')

    def open_shop_index(self):
        ShopIndex()

class ShopIndex(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_shop_index()

    def init_shop_index(self):
        self.title('Главная страница')
        self.geometry('1200x800')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self.cur = self.conn.cursor()


if __name__ == "__main__":
    root = ttk.Window(themename='minty')
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Авторизация')
    root.iconbitmap('')
    root.geometry('800x500')
    root.resizable(False, False)
    root.mainloop()
