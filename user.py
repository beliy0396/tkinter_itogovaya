import ttkbootstrap as ttk
import sqlite3
from tkinter import *
from ttkbootstrap.dialogs import Messagebox


class Main(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()


    def init_main(self):
        label_title = ttk.Label(self, text='Авторизация в системе/Пользователь')
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
        find_user = f"SELECT * FROM users WHERE login = '{login}' AND password = '{password}'"
        cur.execute(find_user)
        results = cur.fetchall()
        if results:
            success = Messagebox.show_info('Успешная авторизация!')
            root.withdraw()
            self.open_shop_index()
        else:
            dont_success = Messagebox.show_info('Неверный логин или пароль!')

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

        toolbar = ttk.Frame(self, bootstyle='light')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        self.catalog_img = ttk.PhotoImage(file='img/catalog.png')
        btn_goods_or_services = ttk.Menubutton(toolbar, text='Категории',
                                               bootstyle="light menubutton",
                                               image=self.catalog_img)
        btn_goods_or_services.grid()
        btn_goods_or_services.menu = Menu(btn_goods_or_services, tearoff=0)
        btn_goods_or_services["menu"] = btn_goods_or_services.menu

        goods = IntVar()
        services = IntVar()

        btn_goods_or_services.menu.add_checkbutton(label="Товары",
                                                   variable=goods,
                                                   command=self.open_goods_catalog)
        btn_goods_or_services.menu.add_checkbutton(label="Услуги",
                                                   variable=services,
                                                   command=self.open_services_catalog)
        btn_goods_or_services.pack(side=ttk.LEFT, padx=10, pady=5)

        self.cart_img = ttk.PhotoImage(file='img/cart.png')
        btn_cart = ttk.Button(toolbar, text='Категории',
                                               bootstyle="light",
                                               image=self.cart_img,
                              command=self.open_cart)

        btn_cart.pack(side=ttk.RIGHT, padx=10, pady=5)

    def open_goods_catalog(self):
        GoodsCatalog()

    def open_services_catalog(self):
        ServicesCatalog()

    def open_cart(self):
        Cart()

class Cart(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_cart()
        self.db = db
        self.view_cart_table()

    def init_cart(self):
        self.title('Корзина')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        self.tree = ttk.Treeview(self, columns=('id', 'products.title', 'services.title'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('products.title', width=150, anchor=ttk.CENTER)
        self.tree.column('services.title', width=250, anchor=ttk.CENTER)


        self.tree.heading('id', text='ID')
        self.tree.heading('products.title', text='Артикул')
        self.tree.heading('services.title', text='Название')
        self.tree.pack()

    def view_cart_table(self):
        self.db.cur.execute(
            '''SELECT cart.id, products.title, services.title FROM cart 
            INNER JOIN products on cart.product_id = products.id
            INNER JOIN services on cart.service_id = services.id WHERE user_id=1'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class GoodsCatalog(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_goods_catalog()
        self.db = db
        self.view_goods_table()

    def init_goods_catalog(self):
        self.title('Каталог товаров')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        label_filter = ttk.Label(toolbar, text='Фильтр:')
        label_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        combobox_values = ['Смартфоны', 'Ноутбуки', 'Наушники']
        self.combobox_filter = ttk.Combobox(toolbar, values=combobox_values, bootstyle="dark")
        self.combobox_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_filter = ttk.Button(toolbar, text='Поиск по фильтру', command=self.view_goods_filter, bootstyle="dark")
        button_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_drop_filter = ttk.Button(toolbar, text='Сбросить фильтр', command=self.view_goods_table, bootstyle="dark")
        button_drop_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_add = ttk.Button(toolbar, text='Добавить товар в корзину', command=self.open_add_products_to_cart, bootstyle="dark")
        button_add.pack(side=ttk.LEFT, padx=35, pady=5)

        self.tree = ttk.Treeview(self, columns=('id', 'number', 'title', 'description', 'category', 'price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('number', width=150, anchor=ttk.CENTER)
        self.tree.column('title', width=250, anchor=ttk.CENTER)
        self.tree.column('description', width=300, anchor=ttk.CENTER)
        self.tree.column('category', width=100, anchor=ttk.CENTER)
        self.tree.column('price', width=200, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('number', text='Артикул')
        self.tree.heading('title', text='Название')
        self.tree.heading('description', text='Описание')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')
        self.tree.pack()

    def open_add_products_to_cart(self):
        AddToCart()


    def view_goods_table(self):
        self.db.cur.execute(
            '''SELECT * FROM products'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_goods_filter(self, *args):
        value = self.combobox_filter.get()
        self.db.cur.execute(
            f'''SELECT * FROM products WHERE category = "{value}"'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]


class AddToCart(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add_to_cart()
        self.db = db

    def init_add_to_cart(self):
        self.title('Добавить товар в корзину')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()


        combobox_values = self.get_product
        self.combobox_products = ttk.Combobox(self, values=combobox_values)
        self.combobox_products.pack(side=ttk.LEFT, padx=35, pady=5)

        button_add = ttk.Button(self, text='Добавить товар в корзину', command=self.get_product,
                                bootstyle="dark")
        button_add.pack(side=ttk.LEFT, padx=35, pady=5)

    def get_product(self):
        dbb = self.db.cur.execute(
            '''SELECT title FROM products'''
        )
        products = []
        for i in dbb:
            products += i

class ServicesCatalog(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_services_catalog()
        self.db = db
        self.view_services_table()


    def init_services_catalog(self):
        self.title('Каталог услуг')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        combobox_values = ['Комплект приложений', 'Наклейка стекла на смартфон', 'Создание учётной записи']
        self.combobox_filter = ttk.Combobox(toolbar, values=combobox_values)
        self.combobox_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_filter = ttk.Button(toolbar, text='Поиск по фильтру', command=self.view_services_filter, bootstyle="dark")
        button_filter.pack(side=ttk.LEFT, padx=35, pady=5)

        button_drop_filter = ttk.Button(toolbar, text='Сбросить фильтр', command=self.view_services_table, bootstyle="dark")
        button_drop_filter.pack(side=ttk.LEFT, padx=35, pady=5)


        self.tree = ttk.Treeview(self, columns=('id', 'number', 'title', 'description', 'category', 'price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('number', width=150, anchor=ttk.CENTER)
        self.tree.column('title', width=250, anchor=ttk.CENTER)
        self.tree.column('description', width=300, anchor=ttk.CENTER)
        self.tree.column('category', width=100, anchor=ttk.CENTER)
        self.tree.column('price', width=200, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('number', text='Артикул')
        self.tree.heading('title', text='Название')
        self.tree.heading('description', text='Описание')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')
        self.tree.pack()

    def view_services_table(self):
        self.db.cur.execute(
            '''SELECT * FROM services'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def view_services_filter(self, *args):
        value = self.combobox_filter.get()
        self.db.cur.execute(
            f'''SELECT * FROM services WHERE category = "{value}"'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self.cur = self.conn.cursor()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        login VARCHAR,
                        password VARCHAR,
                        admin VARCHAR
                    );'''
        )
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY,
                        number VARCHAR,
                        title VARCHAR,
                        description VARCHAR,
                        category VARCHAR,
                        price VARCHAR
                    );'''
        )
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        number VARCHAR,
                        title VARCHAR,
                        description VARCHAR,
                        category VARCHAR,
                        price VARCHAR
                    );'''
        )
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS cart (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        product_id INTEGER,
                        service_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (product_id) REFERENCES products(id),
                        FOREIGN KEY (service_id) REFERENCES services(id)
                    );'''
        )
        self.conn.commit()

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
