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

        toolbar = ttk.Frame(self, bootstyle='light')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        self.catalog_img = ttk.PhotoImage(file='img/catalog.png')
        btn_orders = ttk.Button(toolbar, text='Заказы', command=self.open_orders, image=self.catalog_img,
                               bootstyle="dark")
        btn_orders.pack(side=ttk.LEFT, padx=35, pady=5)

    def open_orders(self):
        Orders()

class Orders(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_orders()
        self.db = db
        self.view_orders()

    def init_orders(self):
        self.title('Заказы')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        def select_item(a):
            item = self.tree.focus()
            global id_order
            id_order = self.tree.item(item)['values'][0]
            SelectItem()
            self.destroy()

        self.tree = ttk.Treeview(self, columns=('id', 'user_id', 'fullname', 'full_price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('user_id', width=150, anchor=ttk.CENTER)
        self.tree.column('fullname', width=250, anchor=ttk.CENTER)
        self.tree.column('full_price', width=300, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('user_id', text='ID Клиента')
        self.tree.heading('fullname', text='ФИО')
        self.tree.heading('full_price', text='Стоимость заказа')
        self.tree.bind('<ButtonRelease-1>', select_item)
        self.tree.pack()


    def view_orders(self):
        self.db.cur.execute(
            '''SELECT id, user_id, fullname, full_price FROM orders'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class SelectItem(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_select_item()
        self.db = db

    def init_select_item(self):
        self.title(f'Заказ {id_order}')
        self.geometry('800x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_products = ttk.Label(self, text='Редактировать или удалить выбранный заказ?')
        label_products.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Редактировать', command=self.open_order_update,
                                bootstyle="dark")
        btn_yes.pack(side=ttk.LEFT, padx=35, pady=5)

        btn_delete = ttk.Button(self, text='Удалить', command=self.order_delete,
                             bootstyle="dark")
        btn_delete.pack(side=ttk.LEFT, padx=35, pady=5)

        btn_no = ttk.Button(self, text='Вернуться к заказам', command=self.no,
                                bootstyle="dark")
        btn_no.pack(side=ttk.LEFT, padx=35, pady=5)

    def no(self):
        self.destroy()

    def open_order_update(self):
        OrderUpdate()
        self.destroy()

    def order_delete(self):
        deleted = self.db.cur.execute(
            f'''DELETE FROM orders WHERE id = {id_order}'''
        )
        self.db.conn.commit()
        self.destroy()
        Orders()


class OrderUpdate(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_order_update()
        self.db = db
        self.view_order_details()

    def init_order_update(self):
        self.title(f'Редактирование заказа {id_order}')
        self.geometry('400x900')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        self.order = ()

        label_order_id = ttk.Label(self, text=f'ID заказа: {id_order}')
        label_order_id.pack(side=ttk.TOP, padx=35, pady=5)

        self.label_order_id_user = ttk.Label(self, text='ID пользователя:')
        self.label_order_id_user.pack(side=ttk.TOP, padx=35, pady=5)

        self.label_order_email = ttk.Label(self, text='E-Mail:')
        self.label_order_email.pack(side=ttk.TOP, padx=35, pady=5)

        self.entry_order_email = ttk.Entry(self, bootstyle='success')
        self.entry_order_email.pack(side=ttk.TOP, padx=35, pady=5)

        self.label_fullname = ttk.Label(self, text='ФИО:')
        self.label_fullname.pack(side=ttk.TOP, padx=35, pady=5)

        self.entry_fullname = ttk.Entry(self, bootstyle='success')
        self.entry_fullname.pack(side=ttk.TOP, padx=35, pady=5)

        self.label_phone = ttk.Label(self, text='Телефон:')
        self.label_phone.pack(side=ttk.TOP, padx=35, pady=5)

        self.entry_phone= ttk.Entry(self, bootstyle='success')
        self.entry_phone.pack(side=ttk.TOP, padx=35, pady=5)

        self.label_country = ttk.Label(self, text='Страна:')
        self.label_country.pack(side=ttk.TOP, padx=35, pady=5)

        self.entry_country = ttk.Entry(self, bootstyle='success')
        self.entry_country.pack(side=ttk.TOP, padx=35, pady=5)

        self.label_city = ttk.Label(self, text='Город:')
        self.label_city.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_city = ttk.Entry(self, bootstyle='success')
        self.entry_city.pack(side=ttk.TOP, padx=10, pady=5)

        self.label_street = ttk.Label(self, text='Улица:')
        self.label_street.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_street = ttk.Entry(self, bootstyle='success')
        self.entry_street.pack(side=ttk.TOP, padx=10, pady=5)

        self.label_house = ttk.Label(self, text='Дом:')
        self.label_house.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_house = ttk.Entry(self, bootstyle='success')
        self.entry_house.pack(side=ttk.TOP, padx=10, pady=5)

        self.label_comment = ttk.Label(self, text='Комментарий к заказу:')
        self.label_comment.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_comment = ttk.Entry(self, bootstyle='success')
        self.entry_comment.pack(side=ttk.TOP, padx=10, pady=5)

        self.label_delivery = ttk.Label(self, text='Доставка:')
        self.label_delivery.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_delivery = ttk.Entry(self, bootstyle='success')
        self.entry_delivery.pack(side=ttk.TOP, padx=10, pady=5)

        self.label_delivery_price = ttk.Label(self, text='Стоимость доставки:')
        self.label_delivery_price.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_delivery_price = ttk.Entry(self, bootstyle='success')
        self.entry_delivery_price.pack(side=ttk.TOP, padx=10, pady=5)

        self.label_fullprice = ttk.Label(self, text='Полная стоимость заказа:')
        self.label_fullprice.pack(side=ttk.TOP, padx=10, pady=5)

        btn_save = ttk.Button(self, text='Сохранить', command=self.save,
                            bootstyle="dark")
        btn_save.pack(side=ttk.TOP, padx=35, pady=5)

        btn_pio = ttk.Button(self, text='Товары в заказе', command=self.open_pio,
                              bootstyle="dark")
        btn_pio.pack(side=ttk.TOP, padx=35, pady=5)

    def save(self):
        if self.entry_fullname.get() == '':
            fio = self.order[3]
        elif self.entry_order_email == '':
            email = self.order[2]
        elif self.entry_phone.get() == '':
            phone = self.order[4]
        elif self.entry_country.get() == '':
            country = self.order[5]
        elif self.entry_city.get() == '':
            city = self.order[6]
        elif self.entry_street.get() == '':
            street = self.order[7]
        elif self.entry_house.get() == '':
            house = self.order[8]
        elif self.entry_comment.get() == '':
            comment = self.order[9]
        elif self.entry_delivery.get() == '':
            delivery = self.order[10]
        elif self.entry_delivery_price.get() == '':
            del_price = self.order[11]


        update = self.db.cur.execute(
            f'''UPDATE orders SET email == "{email}",
            fullname == "{fio}",
            phone_number == "{phone}",
            country == "{country}",
            city == "{city}",
            street == "{street}",
            house == "{house}",
            comment == "{comment}",
            delivery == "{delivery}",
            delivery_price == "{del_price}"
            WHERE id = {id_order}'''
        )
        self.db.conn.commit()

    def open_pio(self):
        self.destroy()
        Pio()

    def view_order_details(self):
        order = self.db.cur.execute(
            f'''SELECT * FROM orders WHERE id = "{id_order}"'''
        )
        self.order = self.db.cur.fetchone()
        self.label_order_id_user.config(text=f'ID пользователя: {self.order[1]}')
        self.label_order_email.config(text=f'E-Mail: {self.order[2]}')
        self.label_fullname.config(text=f'ФИО: {self.order[3]}')
        self.label_phone.config(text=f'Телефон: {self.order[4]}')
        self.label_country.config(text=f'Страна: {self.order[5]}')
        self.label_city.config(text=f'Город: {self.order[6]}')
        self.label_street.config(text=f'Улица: {self.order[7]}')
        self.label_house.config(text=f'Дом: {self.order[8]}')
        self.label_comment.config(text=f'Комментарий: {self.order[9]}')
        self.label_delivery.config(text=f'Доставка: {self.order[10]}')
        self.label_delivery_price.config(text=f'Стоимость доставки: {self.order[11]}')
        self.label_fullprice.config(text=f'Полная стоимость заказа: {self.order[12]}')

class Pio(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_pio()
        self.db = db
        self.view_pio()

    def init_pio(self):
        self.title(f'Товары в заказе {id_order}')
        self.geometry('1400x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        toolbar = ttk.Frame(self, bootstyle='secondary')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        def select_item(a):
            item = self.tree.focus()
            global id_product
            id_product = self.tree.item(item)['values'][0]
            self.destroy()
            SelectPio()

        self.tree = ttk.Treeview(self, columns=('id', 'order_id', 'product_id', 'product_price', 'service_id', 'service_price', 'amount'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('order_id', width=150, anchor=ttk.CENTER)
        self.tree.column('product_id', width=250, anchor=ttk.CENTER)
        self.tree.column('product_price', width=300, anchor=ttk.CENTER)
        self.tree.column('service_id', width=250, anchor=ttk.CENTER)
        self.tree.column('service_price', width=300, anchor=ttk.CENTER)
        self.tree.column('amount', width=300, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('order_id', text='ID заказа')
        self.tree.heading('product_id', text='ID товара')
        self.tree.heading('product_price', text='Стоимость товара')
        self.tree.heading('service_id', text='ID услуги')
        self.tree.heading('service_price', text='Стоимость услуги')
        self.tree.heading('amount', text='Кол-во')

        self.tree.bind('<ButtonRelease-1>', select_item)

        self.tree.pack()

    def view_pio(self):
        self.db.cur.execute(
            '''SELECT * FROM products_in_order'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class SelectPio(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_select_item()
        self.db = db

    def init_select_item(self):
        self.title(f'Товар {id_product}')
        self.geometry('400x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_products = ttk.Label(self, text='Удалить выбранный товар из заказа?')
        label_products.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Удалить', command=self.delete_col,
                                bootstyle="dark")
        btn_yes.pack(side=ttk.LEFT, padx=35, pady=5)

        btn_no = ttk.Button(self, text='Вернуться к заказу', command=self.no,
                                bootstyle="dark")
        btn_no.pack(side=ttk.LEFT, padx=35, pady=5)

    def no(self):
        self.destroy()

    def delete_col(self):
        deleted = self.db.cur.execute(
            f'''DELETE FROM products_in_order WHERE id = {id_product}'''
        )
        self.db.conn.commit()
        self.destroy()
        OrderUpdate()



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
