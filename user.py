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
        find_user = f"SELECT id FROM users WHERE login = '{login}' AND password = '{password}'"
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
        self.geometry('1000x800')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        def select_item(a):
            item = self.tree.focus()
            global id_product_delete
            id_product_delete = self.tree.item(item)['values'][0]
            DeleteCart()
            self.destroy()

        self.tree = ttk.Treeview(self, columns=('id', 'products.title', 'services.title', 'amount', 'products.price'),
                                 height=35,
                                 show='headings')
        self.tree.column('id', width=50, anchor=ttk.CENTER)
        self.tree.column('products.title', width=150, anchor=ttk.CENTER)
        self.tree.column('services.title', width=250, anchor=ttk.CENTER)
        self.tree.column('amount', width=250, anchor=ttk.CENTER)
        self.tree.column('products.price', width=250, anchor=ttk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('products.title', text='Артикул')
        self.tree.heading('services.title', text='Название')
        self.tree.heading('amount', text='Количество')
        self.tree.heading('products.price', text='Цена')
        self.tree.bind('<ButtonRelease-1>', select_item)
        self.tree.pack()

        toolbar = ttk.Frame(self, bootstyle='light')
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        btn_order = ttk.Button(toolbar, text='Оформить заказ', command=self.check,
                                bootstyle="dark")
        btn_order.pack(side=ttk.LEFT, padx=35, pady=5)

    def check(self, *args):
        a = self.tree.get_children()
        if len(a) > 0:
            Order()
        else:
            CartNot()

    def view_cart_table(self):
        self.db.cur.execute(
            f'''SELECT cart.id, products.title, services.title, cart.amount, products.price FROM cart 
            INNER JOIN products on cart.product_id = products.id
            INNER JOIN services on cart.service_id = services.id WHERE user_id={int(id[0])}'''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class CartNot(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_cart_not()

    def init_cart_not(self):
        self.title('Пустая корзина')
        self.geometry('200x100')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_delete = ttk.Label(self, text='Ваша корзина пустая!')
        label_delete.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Ок', command=self.close,
                             bootstyle="dark")
        btn_yes.pack(side=ttk.TOP, padx=35, pady=5)

    def close(self):
        self.destroy()

class DeleteCart(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_card_and_delivery()
        self.db = db

    def init_card_and_delivery(self):
        self.title('Удалить товар из корзины')
        self.geometry('200x800')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_delete = ttk.Label(self, text='Вы действительно хотите удалить товар из корзины?')
        label_delete.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Да', command=self.delete_col,
                             bootstyle="dark")
        btn_yes.pack(side=ttk.LEFT, padx=35, pady=5)

        btn_no = ttk.Button(self, text='Нет', command=self.no,
                            bootstyle="dark")
        btn_no.pack(side=ttk.LEFT, padx=35, pady=5)

    def no(self):
        self.destroy()

    def delete_col(self):
        deleted = self.db.cur.execute(
            f'''DELETE FROM cart WHERE id = {id_product_delete}'''
        )
        self.db.conn.commit()
        self.destroy()
        Cart()


class Order(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_card_and_delivery()

    def init_card_and_delivery(self):
        self.title('Оформление заказа')
        self.geometry('250x600')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_email = ttk.Label(self, text='E-Mail:')
        label_email.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_email = ttk.Entry(self, bootstyle='success')
        self.entry_email.pack(side=ttk.TOP, padx=10, pady=5)

        label_fullname = ttk.Label(self, text='ФИО:')
        label_fullname.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_fullname = ttk.Entry(self, bootstyle='success')
        self.entry_fullname.pack(side=ttk.TOP, padx=10, pady=5)

        label_phone_number = ttk.Label(self, text='Телефон:')
        label_phone_number.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_phone_number = ttk.Entry(self, bootstyle='success')
        self.entry_phone_number.pack(side=ttk.TOP, padx=10, pady=5)

        label_country = ttk.Label(self, text='Страна:')
        label_country.pack(side=ttk.TOP, padx=10, pady=5)

        self.combobox_country = ttk.Combobox(self, values=['Россия', 'Не Россия'])
        self.combobox_country.pack(side=ttk.TOP, padx=10, pady=5)

        label_city = ttk.Label(self, text='Город:')
        label_city.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_city = ttk.Entry(self, bootstyle='success')
        self.entry_city.pack(side=ttk.TOP, padx=10, pady=5)

        label_street = ttk.Label(self, text='Улица:')
        label_street.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_street = ttk.Entry(self, bootstyle='success')
        self.entry_street.pack(side=ttk.TOP, padx=10, pady=5)

        label_house = ttk.Label(self, text='Дом:')
        label_house.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_house = ttk.Entry(self, bootstyle='success')
        self.entry_house.pack(side=ttk.TOP, padx=10, pady=5)

        label_comment = ttk.Label(self, text='Комментарий к заказу:')
        label_comment.pack(side=ttk.TOP, padx=10, pady=5)

        self.entry_comment = ttk.Entry(self, bootstyle='success')
        self.entry_comment.pack(side=ttk.TOP, padx=10, pady=5)

        btn_order = ttk.Button(self, text='Выбрать способ доставки', command=self.open_delivery,
                               bootstyle="dark")
        btn_order.pack(side=ttk.LEFT, padx=35, pady=5)

    def open_delivery(self):
        if (self.entry_email.get() == '') or (self.entry_fullname.get() == '') or (self.combobox_country.get() == '')\
                or (self.entry_city.get() == '')\
                or (self.entry_street.get() == '')\
                or (self.entry_house.get() == '')\
                or (self.entry_phone_number.get() == ''):
            EntryNull()
        else:
            global email, fullname, phone, country, city, street, house, comment
            email = self.entry_email.get()
            fullname = self.entry_fullname.get()
            phone = self.entry_phone_number.get()
            country = self.combobox_country.get()
            city = self.entry_city.get()
            street = self.entry_street.get()
            house = self.entry_house.get()
            comment = self.entry_comment.get()
            Delivery()
            self.destroy()

class EntryNull(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_entry_null()

    def init_entry_null(self):
        self.title('Ошибка')
        self.geometry('300x100')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_delete = ttk.Label(self, text='Введены не все данные!')
        label_delete.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Ок', command=self.close,
                             bootstyle="dark")
        btn_yes.pack(side=ttk.TOP, padx=35, pady=5)

    def close(self):
        self.destroy()

class Delivery(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_delivery()
        self.db = db
        self.price_products()
        self.price_full()

    def init_delivery(self):
        self.title('Способ доставки')
        self.geometry('1000x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        self.delivery_price = 0

        label_title = ttk.Label(self, text='Персональные данные:')
        label_title.pack(side=ttk.TOP, padx=35, pady=5)

        label_info = ttk.Label(self, text=f'ФИО: {fullname}, Телефон: {phone}, E-Mail: {email}')
        label_info.pack(side=ttk.TOP, padx=35, pady=5)

        label_address = ttk.Label(self, text=f'Страна: {country}, Город: {city}, Улица: {street},  Дом: {house}')
        label_address.pack(side=ttk.TOP, padx=35, pady=5)

        label_deliverys = ttk.Label(self, text='Выберите способ доставки:')
        label_deliverys.pack(side=ttk.TOP, padx=35, pady=5)

        label_pred = ttk.Label(self, text='Предоплата доставки')
        label_pred.pack(side=ttk.TOP, padx=35, pady=5)

        self.check_btn_CDEK_p = ttk.Checkbutton(self, text='CDEK', command=self.delivery_cdek)
        self.check_btn_CDEK_p.pack(side=ttk.TOP, padx=35, pady=5)

        self.check_btn_POCHTA_p = ttk.Checkbutton(self, text='Почта России', command=self.delivery_pochta)
        self.check_btn_POCHTA_p.pack(side=ttk.TOP, padx=35, pady=5)

        label_full = ttk.Label(self, text='Полная предоплата заказа')
        label_full.pack(side=ttk.TOP, padx=35, pady=5)

        self.check_btn_CDEK_f = ttk.Checkbutton(self, text='CDEK', command=self.delivery_cdek)
        self.check_btn_CDEK_f.pack(side=ttk.TOP, padx=35, pady=5)

        self.check_btn_POCHTA_f = ttk.Checkbutton(self, text='Почта России', command=self.delivery_pochta)
        self.check_btn_POCHTA_f.pack(side=ttk.TOP, padx=35, pady=5)

        self.full_price = 0
        self.label_full_price = ttk.Label(self, text=f'ИТОГО К ОПЛАТЕ: {self.full_price} руб.')
        self.label_full_price.pack(side=ttk.TOP, padx=35, pady=5)

        self.price_product = 0
        self.label_price_products = ttk.Label(self, text=f'СТОИМОСТЬ ТОВАРОВ: {self.price_product} руб.')
        self.label_price_products.pack(side=ttk.TOP, padx=35, pady=5)


        self.label_deliverys_price = ttk.Label(self, text=f'СТОИМОСТЬ ДОСТАВКИ: {self.delivery_price} руб.')
        self.label_deliverys_price.pack(side=ttk.TOP, padx=35, pady=5)

        btn_pay = ttk.Button(self, text='Оплатить', command=self.added_order,
                             bootstyle="dark")
        btn_pay.pack(side=ttk.TOP, padx=35, pady=5)

    def price_full(self):
        self.full_price = self.price_product + self.delivery_price
        self.label_full_price.config(text=f'ИТОГО К ОПЛАТЕ: {self.full_price} руб.')
    def price_products(self):
        price = self.db.cur.execute(
            f'''SELECT products.price, amount FROM cart 
            INNER JOIN products on cart.product_id = products.id
            WHERE user_id = {int(id[0])}'''
        )
        while True:
            price = self.db.cur.fetchone()
            if price:
                self.price_product = int(price[0]) * int(price[1])
            else:
                break
        self.label_price_products.config(text=f'СТОИМОСТЬ ТОВАРОВ: {self.price_product}')

    def added_order(self):
        cart = self.db.cur.execute(
            f'''SELECT amount, product_id, service_id FROM cart WHERE user_id = {int(id[0])}'''
        )
        # if (self.check_btn_POCHTA_f.state()[0] == 'alternate') or (self.check_btn_CDEK_f.state()[0] == 'alternate') or (self.check_btn_POCHTA_p.state()[0] == 'alternate') or (self.check_btn_CDEK_p.state()[0] == 'alternate'):
        #     DeliveryNull()
        # else:
        while True:
            cart = self.db.cur.fetchone()
            if cart:
                added = self.db.cur.execute(
                    f'''INSERT INTO orders(user_id, product_id, service_id, amount, email, fullname, phone_number, country, city, street, house, comment) VALUES({int(id[0])}, {cart[1]}, {cart[2]} , "{cart[0]}", "{email}", "{fullname}", "{phone}", "{country}", "{city}", "{street}", "{house}", "{comment}")'''
                )
                self.db.conn.commit()
            else:
                break

    def delivery_cdek(self):
        self.delivery_price = 550
        self.label_deliverys_price.config(text=f'СТОИМОСТЬ ДОСТАВКИ: {self.delivery_price}')
        self.full_price = self.price_product + self.delivery_price
        self.label_full_price.config(text=f'ИТОГО К ОПЛАТЕ: {self.full_price} руб.')


    def delivery_pochta(self):
        self.delivery_price = 500
        self.label_deliverys_price.config(text=f'СТОИМОСТЬ ДОСТАВКИ: {self.delivery_price}')
        self.full_price = self.price_product + self.delivery_price
        self.label_full_price.config(text=f'ИТОГО К ОПЛАТЕ: {self.full_price} руб.')

class DeliveryNull(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_delivery_null()

    def init_delivery_null(self):
        self.title('Ошибка')
        self.geometry('300x100')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_delete = ttk.Label(self, text='Не выбран способ доставки!')
        label_delete.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Ок', command=self.close,
                             bootstyle="dark")
        btn_yes.pack(side=ttk.TOP, padx=35, pady=5)

    def close(self):
        self.destroy()

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

        def select_item(a):
            item = self.tree.focus()
            global id_product_to_cart
            id_product_to_cart = self.tree.item(item)['values'][0]
            SelectItem()

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
        self.tree.bind('<ButtonRelease-1>', select_item)
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


class SelectItem(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_select_item()

    def init_select_item(self):
        self.title('Добавить товар в корзину')
        self.geometry('500x200')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_products = ttk.Label(self, text='Добавить выбранный товар в корзину?')
        label_products.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Добавить товар в корзину', command=self.open_service_add,
                                bootstyle="dark")
        btn_yes.pack(side=ttk.LEFT, padx=35, pady=5)

        btn_no = ttk.Button(self, text='Вернуться к каталогу товаров', command=self.no,
                                bootstyle="dark")
        btn_no.pack(side=ttk.LEFT, padx=35, pady=5)

    def no(self):
        self.destroy()

    def open_service_add(self):
        ServiceAdd()
        self.destroy()

class ServiceAdd(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_service_add()

    def init_service_add(self):
        self.title('Дополнительная услуга')
        self.geometry('400x200')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_products = ttk.Label(self, text='Хотите дополнительную услугу к товару?')
        label_products.pack(side=ttk.TOP, padx=35, pady=5)

        btn_yes = ttk.Button(self, text='Да', command=self.yes,
                             bootstyle="dark")
        btn_yes.pack(side=ttk.LEFT, padx=35, pady=5)

        btn_no = ttk.Button(self, text='Нет',
                            bootstyle="dark")
        btn_no.pack(side=ttk.RIGHT, padx=35, pady=5)

    def yes(self):
        ServiceAdded()
        self.destroy()
class ServiceAdded(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_select_service()
        self.db = db
        self.get_service()

    def init_select_service(self):
        self.title('Выбор дополнительной услуги')
        self.geometry('800x500')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_services = ttk.Label(self, text='Дополнительная услуга:')
        label_services.pack(side=ttk.TOP, padx=35, pady=5)

        button_add = ttk.Button(self, text='Добавить товар в корзину', command=self.add_product,
                                bootstyle="dark")
        button_add.pack(side=ttk.TOP, padx=35, pady=5)

        label_service = ttk.Label(self, text='Услуга:')
        label_service.pack(side=ttk.LEFT, padx=35, pady=5)

        self.combobox_services = ttk.Combobox(self, values=self.get_service)
        self.combobox_services.pack(side=ttk.LEFT, padx=35, pady=5)

        self.combobox_services.bind("<<ComboboxSelected>>", self.get_price)

        self.label_price = ttk.Label(self, text='Цена:')
        self.label_price.pack(side=ttk.LEFT, padx=35, pady=5)

        label_amount = ttk.Label(self, text='Количество товара:')
        label_amount.pack(side=ttk.LEFT, padx=35, pady=5)

        self.entry_amount = ttk.Entry(self, bootstyle='success')
        self.entry_amount.pack(side=ttk.LEFT, padx=35, pady=5)

    def add_product(self):
        id_service = self.db.cur.execute(
            f'''SELECT id FROM services WHERE title ="{self.combobox_services.get()}"'''
        )
        id_service = self.db.cur.fetchone()

        amount_product = self.entry_amount.get()

        added = self.db.cur.execute(
            f'''INSERT INTO cart(product_id, service_id, user_id, amount) VALUES({id_product_to_cart}, {id_service[0]}, {int(id[0])}, '{amount_product}')'''
        )
        self.db.conn.commit()

    def get_service(self):
        services_title = self.db.cur.execute(
            '''SELECT title FROM services'''
        )
        services = []
        for i in services_title:
            services += i
        self.combobox_services.config(values=services)

    def get_price(self, *args):
        services_price = self.db.cur.execute(
            f'''SELECT price FROM services WHERE title = "{self.combobox_services.get()}"'''
        )
        services_price = self.db.cur.fetchone()
        self.label_price.config(text=f'Цена: {services_price[0]}')


class AddToCart(ttk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add_to_cart()
        self.db = db
        self.get_product()
        self.get_service()

    def init_add_to_cart(self):
        self.title('Добавить товар в корзину')
        self.geometry('1400x400')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_products = ttk.Label(self, text='Товар:')
        label_products.pack(side=ttk.LEFT, padx=35, pady=5)

        self.combobox_products = ttk.Combobox(self, values=self.get_product)
        self.combobox_products.pack(side=ttk.LEFT, padx=35, pady=5)

        label_services = ttk.Label(self, text='Дополнительная услуга:')
        label_services.pack(side=ttk.LEFT, padx=35, pady=5)

        self.combobox_services = ttk.Combobox(self, values=self.get_service)
        self.combobox_services.pack(side=ttk.LEFT, padx=35, pady=5)

        label_amount = ttk.Label(self, text='Количество:')
        label_amount.pack(side=ttk.LEFT, padx=35, pady=5)

        self.entry_amount = ttk.Entry(self, bootstyle='success')
        self.entry_amount.pack(side=ttk.LEFT, padx=35, pady=5)

        button_add = ttk.Button(self, text='Добавить товар в корзину', command=self.add_product,
                                bootstyle="dark")
        button_add.pack(side=ttk.LEFT, padx=35, pady=5)

    def get_product(self):
        dbb = self.db.cur.execute(
            '''SELECT title FROM products'''
        )
        products = []
        for i in dbb:
            products += i
        self.combobox_products.config(values=products)

    def get_service(self):
        dbb = self.db.cur.execute(
            '''SELECT title FROM services'''
        )
        services = []
        for i in dbb:
            services += i
        self.combobox_services.config(values=services)

    def add_product(self):
        id_product = self.db.cur.execute(
            f'''SELECT id FROM products WHERE title ="{self.combobox_products.get()}"'''
        )
        id_product = self.db.cur.fetchone()

        id_service = self.db.cur.execute(
            f'''SELECT id FROM services WHERE title ="{self.combobox_services.get()}"'''
        )
        id_service = self.db.cur.fetchone()

        amount_product = self.entry_amount.get()

        added = self.db.cur.execute(
            f'''INSERT INTO cart(product_id, service_id, user_id, amount) VALUES({id_product[0]}, {id_service[0]}, {int(id[0])}, '{amount_product}')'''
        )
        self.db.conn.commit()


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
                        amount VARCHAR,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (product_id) REFERENCES products(id),
                        FOREIGN KEY (service_id) REFERENCES services(id)
                    );'''
        )
        self.conn.commit()

        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        product_id INTEGER,
                        service_id INTEGER, 
                        amount VARCHAR,
                        email INTEGER,
                        fullname VARCHAR,
                        phone_number VARCHAR,
                        country VARCHAR,
                        city VARCHAR,
                        street VARCHAR,
                        house VARCHAR,
                        comment VARCHAR,
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
