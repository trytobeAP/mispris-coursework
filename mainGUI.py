import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


path = "C:/Users/admin/source/repos/UNIVERSITY_repos/3 course/6 sem/mispris/coursework/furniture.db"


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("coursework")
        root.geometry("1000x600")

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        self.tree = ttk.Treeview(root, show="headings")
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)



        self.load_button = ttk.Button(root, text="Load Products", command=self.load_products)
        self.load_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.add_product_button = ttk.Button(root, text="Add product", command=self.add_product)
        self.add_product_button.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        self.edit_button = ttk.Button(root, text="Edit Selected", command=self.edit_product)
        self.edit_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        self.delete_button = ttk.Button(root, text="Delete Selected", command=self.delete_product)
        self.delete_button.grid(row=4, column=0, sticky="ew", padx=10, pady=5)



        self.load_category_button = ttk.Button(root, text="Load Categories", command=self.load_categories)
        self.load_category_button.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        self.add_category_button = ttk.Button(root, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        self.edit_category_button = ttk.Button(root, text="Edit Category", command=self.edit_category)
        self.edit_category_button.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        self.delete_category_button = ttk.Button(root, text="Delete Category", command=self.delete_category)
        self.delete_category_button.grid(row=4, column=1, sticky="ew", padx=10, pady=5)

        self.show_parents_button = ttk.Button(root, text="Show Parents", command=self.show_category_parents)
        self.show_parents_button.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        self.show_children_button = ttk.Button(root, text="Show Children", command=self.show_category_children)
        self.show_children_button.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

        self.show_products_button = ttk.Button(root, text="Show products", command=self.show_products_for_category)
        self.show_products_button.grid(row=7, column=1, sticky="ew", padx=10, pady=5)





        self.load_unit_button = ttk.Button(root, text="Load Unit", command=self.load_unit)
        self.load_unit_button.grid(row=1, column=2, sticky="ew", padx=10, pady=5)

        self.add_unit_button = ttk.Button(root, text="Add Unit", command=self.add_unit)
        self.add_unit_button.grid(row=2, column=2, sticky="ew", padx=10, pady=5)

        self.edit_unit_button = ttk.Button(root, text="Edit Selected", command=self.edit_unit)
        self.edit_unit_button.grid(row=3, column=2, sticky="ew", padx=10, pady=5)

        self.delete_unit_button = ttk.Button(root, text="Delete Selected", command=self.delete_unit)
        self.delete_unit_button.grid(row=4, column=2, sticky="ew", padx=10, pady=5)



        self.fill_example_data_button = ttk.Button(self.root, text="Fill Example Data", command=self.fill_example_data)
        self.fill_example_data_button.grid(row=1, column=3, sticky="ew", padx=10, pady=5)

        self.delete_all_data_button = ttk.Button(self.root, text="Delete All Data", command=self.delete_all_data)
        self.delete_all_data_button.grid(row=2, column=3, sticky="ew", padx=10, pady=5)






        # Configure row and column to resize
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)



        def create_category_table():
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS category
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_parent INTEGER,
                                category_name TEXT UNIQUE,
                                FOREIGN KEY (id_parent) REFERENCES category(id))''')
            self.conn.commit()


        def create_product_table():
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS product
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_category INTEGER,
                                id_unit INTEGER,
                                product_name TEXT NOT NULL,
                                quantity INTEGER DEFAULT 0,
                                price REAL DEFAULT 0,
                                FOREIGN KEY (id_unit) REFERENCES unit(id),
                                FOREIGN KEY (id_category) REFERENCES category(id))''')
            self.conn.commit()


        def create_unit_table():
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS unit
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                unit_name TEXT NOT NULL UNIQUE,
                                unit_name_short TEXT NOT NULL)''')
            self.conn.commit()

        def creating_tables():
            create_category_table()
            create_product_table()
            create_unit_table()

        creating_tables()

    def load_unit(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы unit
        self.cursor.execute("SELECT * FROM unit")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)


    def load_products(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы product
        self.cursor.execute("SELECT * FROM product")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", END, values=row)

    def load_categories(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы category
        self.cursor.execute("SELECT * FROM category")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", END, values=row)

    def add_category(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Category")

        Label(add_window, text="Category Name").grid(row=0, column=0)
        category_name_entry = Entry(add_window)
        category_name_entry.grid(row=0, column=1)

        Label(add_window, text="Parent Category Name (optional)").grid(row=1, column=0)
        parent_category_entry = Entry(add_window)
        parent_category_entry.grid(row=1, column=1)

        def save_new_category():
            category_name = category_name_entry.get()
            parent_name = parent_category_entry.get()

            if not category_name:
                messagebox.showerror("Error", "Category name cannot be empty.")
                return

            if parent_name:
                self.cursor.execute("SELECT id FROM category WHERE category_name = ?", (parent_name,))
                result = self.cursor.fetchone()
                if result:
                    parent_id = result[0]
                else:
                    messagebox.showerror("Error", f"Parent category '{parent_name}' not found.")
                    return
            else:
                parent_id = None

            try:
                if parent_id is not None:
                    self.cursor.execute('''
                        INSERT INTO category (category_name, id_parent)
                        VALUES (?, ?)
                    ''', (category_name, parent_id))
                else:
                    self.cursor.execute('''
                        INSERT INTO category (category_name, id_parent)
                        VALUES (?, NULL)
                    ''', (category_name,))
                self.conn.commit()
                self.load_categories()
                add_window.destroy()
                print('Категория успешно добавлена.')
            except Exception as _ex:
                print(f'Error {_ex} - такое название категории уже есть!')
                messagebox.showerror("Error", f"Error {_ex} - такое название категории уже есть!")

        Button(add_window, text="Save", command=save_new_category).grid(row=2, column=0, columnspan=2)


    def edit_category(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            edit_window = Toplevel(self.root)
            edit_window.title("Edit Category")

            entries = {}
            row_count = 0
            for col in self.tree["columns"]:
                Label(edit_window, text=col).grid(row=row_count, column=0)
                entry = Entry(edit_window)
                entry.grid(row=row_count, column=1)
                if col == "id":
                    entry.insert(0, selected_category[row_count])
                    entry.config(state="readonly")
                elif col == "id_parent":
                    self.cursor.execute("SELECT id_parent FROM category WHERE id = ?", (category_id,))
                    parent_id = self.cursor.fetchone()[0]
                    if parent_id:
                        entry.insert(0, parent_id)
                else:
                    entry.insert(0, selected_category[row_count])
                entries[col] = entry
                row_count += 1

            def update_category():
                update_values = []
                id_parent = None
                set_clause_parts = []
                for col in self.tree["columns"]:
                    if col == "id":
                        continue
                    value = entries[col].get()
                    if col == "id_parent":
                        if value:
                            if value == str(category_id):
                                messagebox.showerror("Error", "A category cannot be its own parent.")
                                return

                            self.cursor.execute("SELECT id FROM category WHERE id = ?", (value,))
                            result = self.cursor.fetchone()
                            if result:
                                id_parent = result[0]
                            else:
                                messagebox.showerror("Error", f"Parent category with id '{value}' not found.")
                                return

                            if self.check_cyclic_dependency(id_parent, category_id):
                                messagebox.showerror("Error", "Cyclic dependency detected.")
                                return
                        set_clause_parts.append(f"{col} = ?")
                        update_values.append(id_parent)
                    else:
                        set_clause_parts.append(f"{col} = ?")
                        update_values.append(value)

                set_clause = ", ".join(set_clause_parts)
                # print(f'set_clause - {set_clause}')
                self.cursor.execute(f"UPDATE category SET {set_clause} WHERE id = ?", update_values + [category_id])
                self.conn.commit()
                self.load_categories()
                edit_window.destroy()

            Button(edit_window, text="Save", command=update_category).grid(row=row_count, column=0, columnspan=2)

        except IndexError:
            pass


    def check_cyclic_dependency(self, new_parent_id, category_id):
        def fetch_parent_category(cat_id):
            self.cursor.execute("SELECT id_parent FROM category WHERE id = ?", (cat_id,))
            return self.cursor.fetchone()[0]

        current_id = new_parent_id
        while current_id is not None:
            if current_id == category_id:
                return True
            current_id = fetch_parent_category(current_id)
        return False


    def add_unit(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Unit")

        Label(add_window, text="Unit Name").grid(row=0, column=0)
        unit_name_entry = Entry(add_window)
        unit_name_entry.grid(row=0, column=1)

        Label(add_window, text="Unit Name Short").grid(row=1, column=0)
        unit_name_short_entry = Entry(add_window)
        unit_name_short_entry.grid(row=1, column=1)

        def save_new_unit():
            unit_name = unit_name_entry.get()
            unit_name_short = unit_name_short_entry.get()

            if not unit_name:
                messagebox.showerror("Error", "Unit name cannot be empty.")
                return

            if not unit_name_short:
                messagebox.showerror("Error", "Unit name short cannot be empty.")
                return

            try:
                self.cursor.execute('''
                    INSERT INTO unit (unit_name, unit_name_short)
                    VALUES (?, ?)
                ''', (unit_name, unit_name_short))
                self.conn.commit()
                self.load_unit()
                add_window.destroy()
                print('Unit successfully added.')
            except Exception as e:
                messagebox.showerror("Error", f"Error {e} - something went wrong when adding the unit!")

        Button(add_window, text="Save", command=save_new_unit).grid(row=2, column=0, columnspan=2)


    def edit_unit(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_product = self.tree.item(selected_item)['values']
            unit_id = selected_product[0]

            edit_window = Toplevel(self.root)
            edit_window.title("Edit Product")

            entries = {}
            row_count = 0

            # print(f'\n self.tree["columns"] = {self.tree["columns"]} \n')

            for col in self.tree["columns"]:
                Label(edit_window, text=col).grid(row=row_count, column=0)
                entry = Entry(edit_window)
                entry.grid(row=row_count, column=1)
                if col == "id":
                    entry.insert(0, selected_product[row_count])
                    entry.config(state="readonly")
                else:
                    entry.insert(0, selected_product[row_count])
                entries[col] = entry
                row_count += 1

            def update_unit():
                update_values = {}
                unit_name = None
                for col in self.tree["columns"]:
                    if col == "id":
                        continue
                    value = entries[col].get()
                    if col == "unit_name":
                        if not value.isdigit():
                            self.cursor.execute("SELECT COUNT(*) FROM unit WHERE unit_name = ?", (value,))
                            result = self.cursor.fetchone()[0]
                            # print(f'value in update_unit() - {value}')
                            # print(f'result in update_unit() - {result}')
                            if result == 0:
                                unit_name = value
                            else:
                                messagebox.showerror("Error", f"Unit_name already exists.")
                                return
                        else:
                            messagebox.showerror("Error", "unit_name must NOT be a number.")
                            return
                        update_values[col] = unit_name
                    if col == "unit_name_short":
                        if not value.isdigit():
                            update_values[col] = value
                        else:
                            messagebox.showerror("Error", "unit_name_short must NOT be a number.")
                            return

                set_clause_parts = [f"{col} = ?" for col in update_values.keys()]
                # print(f'\nset_clause_parts - {set_clause_parts}\n')
                set_clause = ", ".join(set_clause_parts)
                # print(f'\n set_clause -- {set_clause} \n')

                update_values_list = list(update_values.values())
                # print(f'update_values_list - {update_values_list}')

                update_values_list.append(unit_id)
                # print(f'update_values_list ----------- {update_values_list}')
                self.cursor.execute(f"UPDATE unit SET {set_clause} WHERE id = ?", update_values_list)
                self.conn.commit()
                self.load_unit()
                edit_window.destroy()

            Button(edit_window, text="Save", command=update_unit).grid(row=row_count, column=0, columnspan=2)

        except IndexError:
            pass


    def delete_unit(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_unit = self.tree.item(selected_item)['values']
            id_unit = selected_unit[0]
            self.cursor.execute("DELETE FROM unit WHERE id = ?", (id_unit,))

            self.cursor.execute("UPDATE product SET id_unit = NULL WHERE id_unit = ?", (id_unit,))

            # self.load_products()

            self.conn.commit()
            self.load_unit()
        except IndexError:
            pass


    def add_product(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Product")

        Label(add_window, text="Product Name").grid(row=0, column=0)
        product_name_entry = Entry(add_window)
        product_name_entry.grid(row=0, column=1)

        Label(add_window, text="id Category").grid(row=1, column=0)
        id_category_entry = Entry(add_window)
        id_category_entry.grid(row=1, column=1)

        Label(add_window, text="id unit").grid(row=2, column=0)
        id_unit_entry = Entry(add_window)
        id_unit_entry.grid(row=2, column=1)

        Label(add_window, text="Quantity (optional)").grid(row=3, column=0)
        quantity_entry = Entry(add_window)
        quantity_entry.grid(row=3, column=1)

        Label(add_window, text="Price (optional)").grid(row=4, column=0)
        price_entry = Entry(add_window)
        price_entry.grid(row=4, column=1)

        def save_new_product():
            product_name = product_name_entry.get()
            id_category = id_category_entry.get()
            id_unit = id_unit_entry.get()
            quantity = quantity_entry.get()
            price = price_entry.get()

            try:
                if quantity:
                    quantity = int(quantity_entry.get())
            except Exception as _ex:
                print(f'in add_product() error: {_ex}')
                messagebox.showerror("Error", "Quantity type should be type = int.")
                return

            try:
                if price:
                    price = int(price_entry.get())
            except Exception as _ex:
                print(f'in add_product() error: {_ex}')
                messagebox.showerror("Error", "Price type should be type = int.")
                return

            # print(f'type(quantity) - {type(quantity)}')
            # print(f'type(price) - {type(price)}')


            if not product_name:
                messagebox.showerror("Error", "Product name cannot be empty.")
                return


            self.cursor.execute("SELECT COUNT(*) FROM category WHERE id = ?", (id_category,))
            result = self.cursor.fetchone()
            # print(f'result on add_prod() - {result}')

            ## а мб все же так надо???
            if result[0] == 0:
                messagebox.showerror("Error", f"Parent category with id - '{id_category}' not found.")
                return

            # if id_category == 0:
            #     messagebox.showerror("Error", f"Parent category with id - '{id_category}' not found.")
            #     return

            if id_unit:
                self.cursor.execute("SELECT COUNT(*) FROM unit WHERE id = ?", (id_unit,))
                result_unit_id = self.cursor.fetchone()
                if result_unit_id[0] == 0:
                    messagebox.showerror("Error", f"unit with id - '{id_unit}' not found.")
                    return

            # try:

            self.cursor.execute('''
                INSERT INTO product (id_category, product_name, id_unit, quantity, price)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_category, product_name, id_unit, quantity, price))

            self.conn.commit()
            self.load_products()
            add_window.destroy()
            print('Изделие успешно добавлено.')
            # except Exception as _ex:
            #     messagebox.showerror("Error", f"Error {_ex} - что-то пошло не так при добавлении изделия!")

        Button(add_window, text="Save", command=save_new_product).grid(row=5, column=0, columnspan=2)


    def edit_product(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_product = self.tree.item(selected_item)['values']
            product_id = selected_product[0]

            edit_window = Toplevel(self.root)
            edit_window.title("Edit Product")

            entries = {}
            row_count = 0

            # print(f'\n self.tree["columns"] = {self.tree["columns"]} \n')

            for col in self.tree["columns"]:
                Label(edit_window, text=col).grid(row=row_count, column=0)
                entry = Entry(edit_window)
                entry.grid(row=row_count, column=1)
                if col == "id":
                    entry.insert(0, selected_product[row_count])
                    entry.config(state="readonly")
                else:
                    entry.insert(0, selected_product[row_count])
                entries[col] = entry
                row_count += 1

            def update_product():
                update_values = {}
                id_category = None
                for col in self.tree["columns"]:
                    if col == "id":
                        continue
                    value = entries[col].get()
                    if col == "id_category":
                        if value.isdigit():
                            self.cursor.execute("SELECT COUNT(*) FROM category WHERE id = ?", (value,))
                            result = self.cursor.fetchone()
                            if result[0] > 0:
                                id_category = value
                            else:
                                messagebox.showerror("Error", f"Category with id '{value}' not found.")
                                return
                        else:
                            messagebox.showerror("Error", "id_category must be a number.")
                            return
                        update_values[col] = id_category
                    if col == "quantity":
                        if not value.isdigit():
                            messagebox.showerror("Error", "Quantity must be a number.")
                            return
                        else:
                            update_values[col] = value
                    if col == "price":
                        if not value.isdigit():
                            messagebox.showerror("Error", "Price must be a number.")
                            return
                        else:
                            update_values[col] = value
                    if col == 'id_unit':
                        if value:
                            self.cursor.execute("SELECT COUNT(*) FROM unit WHERE id = ?", (value,))
                            result_unit_id = self.cursor.fetchone()
                            if result_unit_id[0] == 0:
                                messagebox.showerror("Error", f"unit with id - '{value}' not found.")
                                return
                            else:
                                update_values[col] = value
                    else:
                        update_values[col] = value

                set_clause_parts = [f"{col} = ?" for col in update_values.keys()]
                # print(f'\nset_clause_parts - {set_clause_parts}\n')
                set_clause = ", ".join(set_clause_parts)
                # print(f'\n set_clause ---- {set_clause} \n')

                update_values_list = list(update_values.values())
                # print(f'update_values_list - {update_values_list}')

                update_values_list.append(product_id)
                self.cursor.execute(f"UPDATE product SET {set_clause} WHERE id = ?", update_values_list)
                self.conn.commit()
                self.load_products()
                edit_window.destroy()

            Button(edit_window, text="Save", command=update_product).grid(row=row_count, column=0, columnspan=2)

        except IndexError:
            pass


    def delete_product(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_product = self.tree.item(selected_item)['values']
            product_id = selected_product[0]
            self.cursor.execute("DELETE FROM product WHERE id = ?", (product_id,))
            self.conn.commit()
            self.load_products()
        except IndexError:
            pass


    def fill_example_data(self):
        # Проверка, пусты ли все таблицы
        self.cursor.execute("SELECT COUNT(*) FROM product")
        if self.cursor.fetchone()[0] != 0:
            messagebox.showinfo("Info", "Tables are not empty. No data added.")
            return

        self.cursor.execute("SELECT COUNT(*) FROM category")
        if self.cursor.fetchone()[0] != 0:
            messagebox.showinfo("Info", "Tables are not empty. No data added.")
            return

        self.cursor.execute("SELECT COUNT(*) FROM unit")
        if self.cursor.fetchone()[0] != 0:
            messagebox.showinfo("Info", "Tables are not empty. No data added.")
            return

        # Вызов функции для заполнения контрольным примером
        self.add_example_data()

        self.load_products()
        messagebox.showinfo("Success", "Example data has been successfully added.")



    def load_products(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы product
        self.cursor.execute("SELECT * FROM product")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", END, values=row)


    def delete_category(self):
        try:
            selected_item = self.tree.selection()[0]
            # print(f'selected_item - {selected_item}')
            selected_category = self.tree.item(selected_item)['values']
            # print(f'selected_category - {selected_category}')
            category_name = selected_category[-1]
            # print(f'category_name - {category_name}')


            if self.is_category_exists(category_name):
                self.cursor.execute("SELECT id FROM category WHERE category_name = ?;", (category_name,))
                delete_id = self.cursor.fetchone()[0]

                # Перемещаем все подкатегории удаляемой категории в категорию "неопределенные"
                self.cursor.execute("UPDATE category SET id_parent = (SELECT id FROM category WHERE category_name = 'неопределенные') WHERE id_parent = ?", (delete_id,))

                self.cursor.execute("SELECT id_parent FROM category WHERE category_name = ?", ('неопределенные',))
                cat_id_undef = self.cursor.fetchone()
                if cat_id_undef:
                    self.cursor.execute("UPDATE category SET id_parent = NULL WHERE category_name = ?", ('неопределенные',))
                    # self.conn.commit()

                # Перемещаем все изделия удаляемой категории в категорию "неопределенные"
                self.cursor.execute("UPDATE product SET id_category = (SELECT id FROM category WHERE category_name = 'неопределенные') WHERE id_category = ?", (delete_id,))

                # Удаляем категорию
                self.cursor.execute("DELETE FROM category WHERE id = ?", (delete_id,))
                self.conn.commit()

                self.load_categories()
                print('Категория успешно удалена.')
            else:
                print('Указанная категория не существует.')
                messagebox.showerror("Error", "Указанная категория не существует.")

        except Exception as _ex:
            print(f"Произошла ошибка при удалении категории: {_ex}")
            messagebox.showerror("Error", f"Произошла ошибка при удалении категории: {_ex}")



    def is_category_exists(self, category_name):
        self.cursor.execute("SELECT COUNT(*) FROM category WHERE category_name = ?", (category_name,))
        count = self.cursor.fetchone()[0]
        return count > 0





















    # additional interface function only (several getters)



    def show_category_parents(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            self.cursor.execute("SELECT category_name FROM category WHERE id = ?", (category_id,))
            clicked_category_name = self.cursor.fetchone()[0]

            # Получаем все предки выбранной категории
            parents = []

            while category_id:
                self.cursor.execute("SELECT id, id_parent, category_name FROM category WHERE id = ?", (category_id,))
                result = self.cursor.fetchone()
                if not result:
                    break
                id, parent_id, category_name = result
                # print(f'\n\nresult - {result}\n\n')

                parents.append([id, parent_id, category_name])
                category_id = parent_id

            # Отображаем новое окно с предками категории
            parent_window = Toplevel(self.root)
            parent_window.minsize(600, 300)
            parent_window.title("Category Parents")

            # Получаем имена столбцов из таблицы category
            self.cursor.execute("PRAGMA table_info(category)")
            columns_info = self.cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            # Создаем Treeview для отображения предков
            parent_tree = ttk.Treeview(parent_window, columns=column_names, show='headings')
            parent_tree.pack(expand=True, fill='both')


            self.cursor.execute("SELECT id, id_parent, category_name FROM category WHERE category_name = ?", (clicked_category_name,))
            result_to_del = self.cursor.fetchone()

            id_self, parent_id_self, category_name_self = result_to_del
            parents.remove([id_self, parent_id_self, category_name_self])

            # Устанавливаем заголовки столбцов
            for col in column_names:
                parent_tree.heading(col, text=col)
                parent_tree.column(col, width=100)




            # Вставляем данные предков в Treeview
            for parent in reversed(parents):  # Обратный порядок для отображения от корня к категории
                parent_tree.insert('', 'end', values=parent)

        except IndexError:
            messagebox.showerror("Error", "No category selected.")



    def show_category_children(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            # Рекурсивно получаем всех потомков выбранной категории
            children = self.get_all_children(category_id)

            # Отображаем новое окно с потомками категории
            child_window = Toplevel(self.root)
            child_window.minsize(300, 100)
            child_window.title("Category Children")

            # Получаем имена столбцов из таблицы category
            self.cursor.execute("PRAGMA table_info(category)")
            columns_info = self.cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            # Создаем Treeview для отображения предков
            parent_tree = ttk.Treeview(child_window, columns=column_names, show='headings')
            parent_tree.pack(expand=True, fill='both')

            # Устанавливаем заголовки столбцов
            for col in column_names:
                parent_tree.heading(col, text=col)
                parent_tree.column(col, width=100)

            for parent in children:  # Обратный порядок для отображения от корня к категории
                parent_tree.insert('', 'end', values=parent)

        except IndexError:
            messagebox.showerror("Error", "No category selected.")


    def get_all_children(self, category_id):
        children = []

        # Получаем все дочерние категории для данного родителя
        self.cursor.execute("SELECT id, id_parent, category_name FROM category WHERE id_parent = ?", (category_id,))
        result = self.cursor.fetchall()
        # print(f'\nresult in children - {result}\n')
        for row in result:
            id, id_parent, category_name = row
            children.append([id, id_parent, category_name])  # Добавляем имя дочерней категории
            children.extend(self.get_all_children(row[0]))  # Рекурсивно добавляем всех потомков для каждой дочерней категории

        return children



    def show_products_for_category(self):
        def get_all_children(category_id):
            children = []
            self.cursor.execute("SELECT id FROM category WHERE id_parent = ?", (category_id,))
            results = self.cursor.fetchall()
            for result in results:
                children.append(result[0])
                children.extend(get_all_children(result[0]))  # Assuming id is the first column
            return children

        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            # Получаем все дочерние категории выбранной категории
            all_category_ids = [category_id] + get_all_children(category_id)

            # Получаем все изделия для выбранной категории и всех дочерних категорий
            products = []
            for cat_id in all_category_ids:
                self.cursor.execute("SELECT * FROM product WHERE id_category = ?", (cat_id,))
                products.extend(self.cursor.fetchall())

            column_names = [description[0] for description in self.cursor.description]

            # Отображаем новое окно со списком изделий для выбранной категории и её дочерних категорий
            products_window = Toplevel(self.root)
            products_window.minsize(600, 400)
            products_window.title("Products for Category")

            # Создаем Treeview для отображения изделий
            product_tree = ttk.Treeview(products_window, columns=column_names, show='headings')
            product_tree.pack(expand=True, fill='both')

            # Устанавливаем заголовки для столбцов
            for col in column_names:
                product_tree.heading(col, text=col)
                product_tree.column(col, width=100)

            # Вставляем данные изделий в Treeview
            for product in products:
                product_tree.insert('', 'end', values=product)

        except IndexError:
            messagebox.showerror("Error", "No category selected.")


    def delete_all_data(self):
        def dropAllTables():
            try:
                # Список таблиц в порядке, в котором их нужно удалить (сначала те, которые не содержат внешних ключей)
                tables_order = ['category', 'unit', 'product', 'sqlite_sequence']

                # Удаление данных из таблиц с внешними ключами
                for table_name in tables_order[::-1]:
                    self.cursor.execute(f"DELETE FROM {table_name};")

                # Удаление самих таблиц
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = self.cursor.fetchall()

                for table in tables:
                    table_name = table[0]
                    self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

                self.conn.commit()

                print("Все таблицы успешно удалены.")
            except Exception as _ex:
                print(f"Произошла ошибка при удалении таблиц: {_ex}")

        def confirm_delete():
            if messagebox.askokcancel("Confirm Delete", "Are you sure you want to delete all data from all tables?"):
                try:
                    # self.cursor.execute("DELETE FROM product")
                    # self.cursor.execute("DELETE FROM category")
                    # self.cursor.execute("DELETE FROM unit")

                    dropAllTables()
                    self.conn.commit()

                    # повторное создание таблиц для сброса id autoincrement
                    self.cursor.execute('''CREATE TABLE IF NOT EXISTS category
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_parent INTEGER,
                                category_name TEXT UNIQUE,
                                FOREIGN KEY (id_parent) REFERENCES category(id))''')
                    self.conn.commit()

                    self.cursor.execute('''CREATE TABLE IF NOT EXISTS product
                                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    id_category INTEGER,
                                                    id_unit INTEGER,
                                                    product_name TEXT NOT NULL,
                                                    quantity INTEGER DEFAULT 0,
                                                    price REAL DEFAULT 0,
                                                    FOREIGN KEY (id_unit) REFERENCES unit(id),
                                                    FOREIGN KEY (id_category) REFERENCES category(id))''')
                    self.conn.commit()

                    self.cursor.execute('''CREATE TABLE IF NOT EXISTS unit
                                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    unit_name TEXT NOT NULL UNIQUE,
                                                    unit_name_short TEXT NOT NULL)''')
                    self.conn.commit()
                    # повторное создание таблиц для сброса id autoincrement

                    messagebox.showinfo("Success", "All data successfully deleted.")
                    self.load_products()
                except Exception as e:
                    messagebox.showerror("Error", f"Error {e} occurred while deleting data.")

        confirm_delete_window = Toplevel(self.root)
        confirm_delete_window.title("Confirm Delete")

        Label(confirm_delete_window, text="Are you sure you want to delete all data from all tables?").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        Button(confirm_delete_window, text="OK", command=confirm_delete).grid(row=1, column=0, padx=10, pady=10)
        Button(confirm_delete_window, text="Cancel", command=confirm_delete_window.destroy).grid(row=1, column=1, padx=10, pady=10)





    def add_example_data(self):

        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('килограмм', 'кг')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('штук', 'шт')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('метр', 'м')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('квадратный метр', 'м2')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('кубический метр', 'м3')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('миллиметр', 'мм')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('ватт', 'вт')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('вольт', 'в')")
        self.cursor.execute("INSERT INTO unit (unit_name, unit_name_short) VALUES ('ампер', 'а')")



        # добавление корневых категорий
        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, NULL)', ('неопределенные',)) #1
        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, NULL)', ('изделия',)) #2

        ##
        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("столы", 2)) #3

        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("столы-металл", 3)) #4

        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стол_arizone', 4, 2, 110, 2500.0)")
        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стол_garden_story', 4, 2, 54, 5665.0)")
        #

        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("столы-дерево", 3)) #5

        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стол_эстер', 5, 2, 124, 6460.0)")
        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стол_кентуки', 5, 2, 1340, 2400.0)")

        ##
        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("стулья", 2)) #6

        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("стулья-пластик", 6)) #7


        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стул_rambo', 7, 2, 435, 1580.0)")
        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стул_keter', 7, 2, 252, 1300.0)")

        #
        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("стулья-металл", 6)) #8


        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стул_arizone', 8, 2, 245, 3400.0)")
        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('стул_giardino', 8, 2, 25, 2400.0)")

        ##
        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("кресла", 2)) #9

        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("кресла-кресло_кокон", 9)) #10

        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('кресло-m-group', 10, 2, 24, 12000.0)")
        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('кресло-гамак', 10, 2, 14, 15500.0)")
        #

        self.cursor.execute('INSERT INTO category (category_name, id_parent) VALUES (?, ?)', ("кресла-двухместное_кресло", 9)) #11

        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('кресло-gemini_promob', 11, 2, 4, 8999.0)")
        self.cursor.execute("INSERT INTO product (product_name, id_category, id_unit, quantity, price) VALUES ('кресло-парящая_кровать', 11, 2, 54, 9999.0)")


        self.conn.commit()


    def __del__(self):
        self.conn.close()












###################################################################################################################




class DatabaseUserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("coursework")
        root.geometry("1000x600")

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        self.tree = ttk.Treeview(root, show="headings")
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)



        self.load_button = ttk.Button(root, text="Load Products", command=self.load_products)
        self.load_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)



        self.load_category_button = ttk.Button(root, text="Load Categories", command=self.load_categories)
        self.load_category_button.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        self.show_parents_button = ttk.Button(root, text="Show Parents", command=self.show_category_parents)
        self.show_parents_button.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        self.show_children_button = ttk.Button(root, text="Show Children", command=self.show_category_children)
        self.show_children_button.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        self.show_products_button = ttk.Button(root, text="Show products", command=self.show_products_for_category)
        self.show_products_button.grid(row=4, column=1, sticky="ew", padx=10, pady=5)



        self.load_unit_button = ttk.Button(root, text="Load Unit", command=self.load_unit)
        self.load_unit_button.grid(row=1, column=2, sticky="ew", padx=10, pady=5)



        # Configure row and column to resize
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)




        def create_category_table():
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS category
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_parent INTEGER,
                                category_name TEXT UNIQUE,
                                FOREIGN KEY (id_parent) REFERENCES category(id))''')
            self.conn.commit()


        def create_product_table():
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS product
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_category INTEGER,
                                id_unit INTEGER,
                                product_name TEXT NOT NULL,
                                quantity INTEGER DEFAULT 0,
                                price REAL DEFAULT 0,
                                FOREIGN KEY (id_unit) REFERENCES unit(id),
                                FOREIGN KEY (id_category) REFERENCES category(id))''')
            self.conn.commit()


        def create_unit_table():
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS unit
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                unit_name TEXT NOT NULL UNIQUE,
                                unit_name_short TEXT NOT NULL)''')
            self.conn.commit()

        def creating_tables():
            create_category_table()
            create_product_table()
            create_unit_table()

        creating_tables()

    def load_unit(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы unit
        self.cursor.execute("SELECT * FROM unit")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)


    def load_products(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы product
        self.cursor.execute("SELECT * FROM product")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", END, values=row)


    def load_categories(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы category
        self.cursor.execute("SELECT * FROM category")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", END, values=row)



    def load_products(self):
        # Очистка текущих данных из Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получение данных из таблицы product
        self.cursor.execute("SELECT * FROM product")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Очистка старых заголовков столбцов
        self.tree["columns"] = column_names
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину столбцов

        # Вставка данных в Treeview
        for row in rows:
            self.tree.insert("", END, values=row)



    # additional interface function only (several getters)

    def show_category_parents(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            self.cursor.execute("SELECT category_name FROM category WHERE id = ?", (category_id,))
            clicked_category_name = self.cursor.fetchone()[0]

            # Получаем все предки выбранной категории
            parents = []

            while category_id:
                self.cursor.execute("SELECT id, id_parent, category_name FROM category WHERE id = ?", (category_id,))
                result = self.cursor.fetchone()
                if not result:
                    break
                id, parent_id, category_name = result
                # print(f'\n\nresult - {result}\n\n')

                parents.append([id, parent_id, category_name])
                category_id = parent_id

            # Отображаем новое окно с предками категории
            parent_window = Toplevel(self.root)
            parent_window.minsize(600, 300)
            parent_window.title("Category Parents")

            # Получаем имена столбцов из таблицы category
            self.cursor.execute("PRAGMA table_info(category)")
            columns_info = self.cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            # Создаем Treeview для отображения предков
            parent_tree = ttk.Treeview(parent_window, columns=column_names, show='headings')
            parent_tree.pack(expand=True, fill='both')


            self.cursor.execute("SELECT id, id_parent, category_name FROM category WHERE category_name = ?", (clicked_category_name,))
            result_to_del = self.cursor.fetchone()

            id_self, parent_id_self, category_name_self = result_to_del
            parents.remove([id_self, parent_id_self, category_name_self])

            # Устанавливаем заголовки столбцов
            for col in column_names:
                parent_tree.heading(col, text=col)
                parent_tree.column(col, width=100)




            # Вставляем данные предков в Treeview
            for parent in reversed(parents):  # Обратный порядок для отображения от корня к категории
                parent_tree.insert('', 'end', values=parent)

        except IndexError:
            messagebox.showerror("Error", "No category selected.")



    def show_category_children(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            # Рекурсивно получаем всех потомков выбранной категории
            children = self.get_all_children(category_id)

            # Отображаем новое окно с потомками категории
            child_window = Toplevel(self.root)
            child_window.minsize(300, 100)
            child_window.title("Category Children")

            # Получаем имена столбцов из таблицы category
            self.cursor.execute("PRAGMA table_info(category)")
            columns_info = self.cursor.fetchall()
            column_names = [info[1] for info in columns_info]

            # Создаем Treeview для отображения предков
            parent_tree = ttk.Treeview(child_window, columns=column_names, show='headings')
            parent_tree.pack(expand=True, fill='both')

            # Устанавливаем заголовки столбцов
            for col in column_names:
                parent_tree.heading(col, text=col)
                parent_tree.column(col, width=100)

            for parent in children:  # Обратный порядок для отображения от корня к категории
                parent_tree.insert('', 'end', values=parent)

        except IndexError:
            messagebox.showerror("Error", "No category selected.")


    def get_all_children(self, category_id):
        children = []

        # Получаем все дочерние категории для данного родителя
        self.cursor.execute("SELECT id, id_parent, category_name FROM category WHERE id_parent = ?", (category_id,))
        result = self.cursor.fetchall()
        # print(f'\nresult in children - {result}\n')
        for row in result:
            id, id_parent, category_name = row
            children.append([id, id_parent, category_name])  # Добавляем имя дочерней категории
            children.extend(self.get_all_children(row[0]))  # Рекурсивно добавляем всех потомков для каждой дочерней категории

        return children



    def show_products_for_category(self):
        def get_all_children(category_id):
            children = []
            self.cursor.execute("SELECT id FROM category WHERE id_parent = ?", (category_id,))
            results = self.cursor.fetchall()
            for result in results:
                children.append(result[0])
                children.extend(get_all_children(result[0]))  # Assuming id is the first column
            return children

        try:
            selected_item = self.tree.selection()[0]
            selected_category = self.tree.item(selected_item)['values']
            category_id = selected_category[0]

            # Получаем все дочерние категории выбранной категории
            all_category_ids = [category_id] + get_all_children(category_id)

            # Получаем все изделия для выбранной категории и всех дочерних категорий
            products = []
            for cat_id in all_category_ids:
                self.cursor.execute("SELECT * FROM product WHERE id_category = ?", (cat_id,))
                products.extend(self.cursor.fetchall())

            column_names = [description[0] for description in self.cursor.description]

            # Отображаем новое окно со списком изделий для выбранной категории и её дочерних категорий
            products_window = Toplevel(self.root)
            products_window.minsize(600, 400)
            products_window.title("Products for Category")

            # Создаем Treeview для отображения изделий
            product_tree = ttk.Treeview(products_window, columns=column_names, show='headings')
            product_tree.pack(expand=True, fill='both')

            # Устанавливаем заголовки для столбцов
            for col in column_names:
                product_tree.heading(col, text=col)
                product_tree.column(col, width=100)

            # Вставляем данные изделий в Treeview
            for product in products:
                product_tree.insert('', 'end', values=product)

        except IndexError:
            messagebox.showerror("Error", "No category selected.")




    def __del__(self):
        self.conn.close()


###################################################################################################################



class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("300x150")

        self.label_login = tk.Label(self.master, text="Login:")
        self.label_login.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.label_password = tk.Label(self.master, text="Password:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_login = tk.Entry(self.master)
        self.entry_login.grid(row=0, column=1, padx=10, pady=10)

        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.btn_login = tk.Button(self.master, text="Login", command=self.login)
        self.btn_login.grid(row=2, columnspan=2, padx=10, pady=10)

    def login(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        if login == "admin" and password == "admin":
            self.master.destroy()
            root = tk.Tk()
            root.minsize(600, 350)
            app = DatabaseApp(root)
            root.mainloop()
        elif login == "user" and password == "user":
            self.master.destroy()
            root = tk.Tk()
            root.minsize(600, 350)
            app = DatabaseUserApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login or password.")



if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()