import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os
import csv
from tkinter import filedialog
import pandas as pd

# إنشاء قاعدة البيانات والجداول
def create_database():
    conn = sqlite3.connect('masry_phone.db')
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 role TEXT)''')
    
    # جدول المنتجات
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 category TEXT,
                 price REAL,
                 quantity INTEGER)''')
    
    # جدول المبيعات
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 product_id INTEGER,
                 product_name TEXT,
                 category TEXT,
                 quantity INTEGER,
                 price REAL,
                 total REAL,
                 employee TEXT,
                 customer_name TEXT,
                 date TEXT,
                 day TEXT)''')
    
    # جدول الصيانة
    c.execute('''CREATE TABLE IF NOT EXISTS maintenance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 customer_name TEXT,
                 device_type TEXT,
                 issue TEXT,
                 price REAL,
                 status TEXT,
                 employee TEXT,
                 date TEXT,
                 day TEXT)''')
    
    # إضافة المستخدمين الافتراضيين إذا لم يكونوا موجودين
    users = [
        ('elmasry', '01223416549', 'employee'),
        ('amr', '123456', 'employee'),
        ('admin', 'admin123', 'admin')
    ]
    
    for user in users:
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", user)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()

create_database()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("تسجيل الدخول - المصري فون")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f5ff")
        
        # تحسين الألوان والمظهر
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('TLabel', font=('Arial', 14), background="#f0f5ff", foreground="#2c3e50")
        self.style.configure('TButton', font=('Arial', 14, 'bold'), background="#3498db", foreground="white")
        self.style.configure('TEntry', font=('Arial', 14), fieldbackground="white")
        self.style.map('TButton', background=[('active', '#2980b9')])
        
        # إطار رئيسي
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(pady=50, padx=20, fill=tk.BOTH, expand=True)
        
        # عنوان النظام
        title_label = ttk.Label(main_frame, text="نظام المصري فون", font=('Arial', 24, 'bold'), foreground="#2c3e50")
        title_label.pack(pady=(0, 30))
        
        # إطار الحقول
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, padx=20)
        
        # حقل اسم المستخدم
        ttk.Label(form_frame, text="اسم المستخدم:").grid(row=0, column=0, padx=10, pady=15, sticky='e')
        self.entry_username = ttk.Entry(form_frame, width=25, font=('Arial', 14))
        self.entry_username.grid(row=0, column=1, padx=10, pady=15, sticky='w')
        
        # حقل كلمة المرور
        ttk.Label(form_frame, text="كلمة المرور:").grid(row=1, column=0, padx=10, pady=15, sticky='e')
        self.entry_password = ttk.Entry(form_frame, show="*", width=25, font=('Arial', 14))
        self.entry_password.grid(row=1, column=1, padx=10, pady=15, sticky='w')
        
        # زر الدخول
        self.btn_login = ttk.Button(main_frame, text="دخول", command=self.login, width=15)
        self.btn_login.pack(pady=20)
        
        # ربط زر الدخول بمفتاح الإدخال
        self.entry_password.bind('<Return>', lambda event: self.login())
        
        # توجيه التركيز لحقل اسم المستخدم
        self.entry_username.focus_set()
    
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showerror("خطأ", "يرجى إدخال اسم المستخدم وكلمة المرور")
            return
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            self.root.destroy()
            root = tk.Tk()
            app = MainApp(root, username, user[3])  # تمرير اسم المستخدم ودوره
            root.mainloop()
        else:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

class MainApp:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.root.title(f"المصري فون - {username}")
        self.root.geometry("1400x900")
        self.root.configure(bg="#ecf0f1")
        
        # تحسين الألوان والمظهر
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('.', font=('Arial', 12))
        self.style.configure('TLabel', font=('Arial', 12), background="#ecf0f1", foreground="#2c3e50")
        self.style.configure('TButton', font=('Arial', 12, 'bold'), background="#3498db", foreground="white")
        self.style.configure('Treeview', font=('Arial', 12), rowheight=30, fieldbackground="white")
        self.style.configure('Treeview.Heading', font=('Arial', 13, 'bold'), background="#3498db", foreground="white")
        self.style.configure('TNotebook.Tab', font=('Arial', 13, 'bold'), padding=(15, 8))
        self.style.configure('TLabelframe.Label', font=('Arial', 14, 'bold'), background="#ecf0f1", foreground="#2c3e50")
        self.style.configure('TLabelframe', background="#ecf0f1")
        self.style.map('TButton', background=[('active', '#2980b9')])
        self.style.map('Treeview', background=[('selected', '#3498db')])
        
        self.create_widgets()
    
    def create_widgets(self):
        # إنشاء شريط القوائم
        self.menubar = tk.Menu(self.root)
        
        # قوائم حسب الدور
        if self.role == 'admin':
            # قائمة الملف للمدير
            file_menu = tk.Menu(self.menubar, tearoff=0, font=('Arial', 12))
            file_menu.add_command(label="تصدير البيانات", command=self.export_all_data)
            file_menu.add_command(label="استيراد البيانات", command=self.import_all_data)
            file_menu.add_separator()
            file_menu.add_command(label="خروج", command=self.root.quit)
            self.menubar.add_cascade(label="ملف", menu=file_menu)
        
        # قائمة النظام للجميع
        system_menu = tk.Menu(self.menubar, tearoff=0, font=('Arial', 12))
        system_menu.add_command(label="تغيير المستخدم", command=self.logout)
        system_menu.add_command(label="إغلاق", command=self.root.quit)
        self.menubar.add_cascade(label="النظام", menu=system_menu)
        
        self.root.config(menu=self.menubar)
        
        # إنشاء دفتر الملاحظات (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # تبويب لوحة التحكم
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text='لوحة التحكم')
        self.create_dashboard()
        
        # تبويب بيع المنتج
        self.sales_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_tab, text='بيع منتج')
        self.create_sales_tab()
        
        # تبويب إدارة المخزون
        self.inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text='إدارة المخزون')
        self.create_inventory_tab()
        
        # تبويب الصيانة
        self.maintenance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.maintenance_tab, text='الصيانة')
        self.create_maintenance_tab()
        
        # تبويب المبيعات
        self.sales_report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_report_tab, text='عمليات البيع')
        self.create_sales_report_tab()
        
        # تبويب تقارير المبيعات (للمدير فقط)
        if self.role == 'admin':
            self.reports_tab = ttk.Frame(self.notebook)
            self.notebook.add(self.reports_tab, text='تقرير المبيعات')
            self.create_reports_tab()
            
            self.profit_tab = ttk.Frame(self.notebook)
            self.notebook.add(self.profit_tab, text='تقرير الأرباح')
            self.create_profit_tab()
    
    def create_dashboard(self):
        # إطار العنوان
        title_frame = ttk.Frame(self.dashboard_tab)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, text=f"مرحبًا بك، {self.username}", 
                              font=('Arial', 20, 'bold'), foreground="#2c3e50")
        title_label.pack(pady=10)
        
        # إحصائيات سريعة
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="إحصائيات سريعة")
        stats_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # 4 إطارات للإحصائيات
        stat1 = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=1)
        stat1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        stat1.config(style='Card.TFrame')
        
        stat2 = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=1)
        stat2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')
        
        stat3 = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=1)
        stat3.grid(row=0, column=2, padx=15, pady=15, sticky='nsew')
        
        stat4 = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=1)
        stat4.grid(row=0, column=3, padx=15, pady=15, sticky='nsew')
        
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)
        
        # ألوان البطاقات
        card_colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
        card_texts = ["عدد المنتجات", "إجمالي المبيعات", "طلبات الصيانة", "منتجات منخفضة"]
        
        # ملء الإحصائيات
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        # عدد المنتجات
        c.execute("SELECT COUNT(*) FROM products")
        products_count = c.fetchone()[0]
        
        # إجمالي المبيعات
        c.execute("SELECT SUM(total) FROM sales")
        total_sales = c.fetchone()[0] or 0
        
        # عدد عمليات الصيانة
        c.execute("SELECT COUNT(*) FROM maintenance")
        maintenance_count = c.fetchone()[0]
        
        # المنتجات المنخفضة في المخزون
        c.execute("SELECT COUNT(*) FROM products WHERE quantity < 5")
        low_stock = c.fetchone()[0]
        
        conn.close()
        
        # إضافة البطاقات
        stats = [products_count, total_sales, maintenance_count, low_stock]
        cards = [stat1, stat2, stat3, stat4]
        
        for i, (card, color, text, value) in enumerate(zip(cards, card_colors, card_texts, stats)):
            card.configure(style='Card.TFrame')
            self.style.configure(f'Card{i}.TFrame', background=color)
            card.config(style=f'Card{i}.TFrame')
            
            # عنوان البطاقة
            title = ttk.Label(card, text=text, font=('Arial', 14, 'bold'), foreground="white", 
                            background=color)
            title.pack(pady=(15, 5))
            
            # قيمة البطاقة
            if i == 1:  # المبيعات
                value_label = ttk.Label(card, text=f"{value:.2f} ج.م", font=('Arial', 22, 'bold'), 
                                      foreground="white", background=color)
            else:
                value_label = ttk.Label(card, text=str(value), font=('Arial', 24, 'bold'), 
                                      foreground="white", background=color)
            value_label.pack(pady=(5, 15))
    
    def create_sales_tab(self):
        # إطار اختيار المنتج
        product_frame = ttk.LabelFrame(self.sales_tab, text="اختر المنتج")
        product_frame.pack(pady=15, padx=20, fill='x')
        
        # تصفية حسب الفئة
        ttk.Label(product_frame, text="الفئة:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=15, sticky='e')
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(product_frame, textvariable=self.category_var, 
                                             font=('Arial', 12), state='readonly', width=25)
        self.category_combobox.grid(row=0, column=1, padx=15, pady=15, sticky='w')
        self.category_combobox.bind('<<ComboboxSelected>>', self.update_products_list)
        
        # اختيار المنتج
        ttk.Label(product_frame, text="المنتج:", font=('Arial', 12)).grid(row=1, column=0, padx=15, pady=15, sticky='e')
        self.product_var = tk.StringVar()
        self.product_combobox = ttk.Combobox(product_frame, textvariable=self.product_var, 
                                           font=('Arial', 12), state='readonly', width=25)
        self.product_combobox.grid(row=1, column=1, padx=15, pady=15, sticky='w')
        self.product_combobox.bind('<<ComboboxSelected>>', self.update_product_details)
        
        # تفاصيل المنتج
        details_frame = ttk.LabelFrame(self.sales_tab, text="تفاصيل المنتج")
        details_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(details_frame, text="السعر:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10, sticky='e')
        self.price_label = ttk.Label(details_frame, text="0.00 ج.م", font=('Arial', 12, 'bold'))
        self.price_label.grid(row=0, column=1, padx=15, pady=10, sticky='w')
        
        ttk.Label(details_frame, text="الكمية المتاحة:", font=('Arial', 12)).grid(row=1, column=0, padx=15, pady=10, sticky='e')
        self.quantity_label = ttk.Label(details_frame, text="0", font=('Arial', 12, 'bold'))
        self.quantity_label.grid(row=1, column=1, padx=15, pady=10, sticky='w')
        
        # تفاصيل المشتري
        customer_frame = ttk.LabelFrame(self.sales_tab, text="بيانات المشتري")
        customer_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(customer_frame, text="اسم المشتري:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.customer_name_entry = ttk.Entry(customer_frame, font=('Arial', 12), width=30)
        self.customer_name_entry.grid(row=0, column=1, padx=15, pady=10, columnspan=2)
        
        # إطار الكمية والسعر
        sale_frame = ttk.LabelFrame(self.sales_tab, text="تفاصيل البيع")
        sale_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(sale_frame, text="الكمية:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.sale_quantity = tk.IntVar(value=1)
        spinbox = ttk.Spinbox(sale_frame, from_=1, to=100, textvariable=self.sale_quantity, 
                            font=('Arial', 12), width=10, command=self.calculate_total)
        spinbox.grid(row=0, column=1, padx=15, pady=10)
        
        ttk.Label(sale_frame, text="السعر الإجمالي:", font=('Arial', 12)).grid(row=1, column=0, padx=15, pady=10)
        self.total_label = ttk.Label(sale_frame, text="0.00 ج.م", font=('Arial', 14, 'bold'), foreground="#e74c3c")
        self.total_label.grid(row=1, column=1, padx=15, pady=10, sticky='w')
        
        # أزرار التحكم
        button_frame = ttk.Frame(self.sales_tab)
        button_frame.pack(pady=20)
        
        self.style.configure('Action.TButton', font=('Arial', 14, 'bold'), padding=10)
        
        ttk.Button(button_frame, text="إتمام البيع", command=self.complete_sale, 
                  style='Action.TButton').grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="مسح الحقول", command=self.clear_sale_fields, 
                  style='Action.TButton').grid(row=0, column=1, padx=15)
        
        # تحديث قائمة الفئات
        self.update_categories()
    
    def clear_sale_fields(self):
        self.sale_quantity.set(1)
        self.total_label.config(text="0.00 ج.م")
        self.customer_name_entry.delete(0, tk.END)
    
    def update_categories(self):
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        c.execute("SELECT DISTINCT category FROM products WHERE quantity > 0")  # فقط الفئات التي لديها منتجات متاحة
        categories = [row[0] for row in c.fetchall()]
        
        self.category_combobox['values'] = categories
        if categories:
            self.category_var.set(categories[0])
            self.update_products_list()
        
        conn.close()
    
    def update_products_list(self, event=None):
        category = self.category_var.get()
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        c.execute("SELECT name FROM products WHERE category=? AND quantity > 0", (category,))
        products = [row[0] for row in c.fetchall()]
        
        self.product_combobox['values'] = products
        if products:
            self.product_var.set(products[0])
            self.update_product_details()
        else:
            self.product_var.set('')
            self.price_label.config(text="0.00 ج.م")
            self.quantity_label.config(text="0")
        
        conn.close()
    
    def update_product_details(self, event=None):
        product_name = self.product_var.get()
        
        if not product_name:
            return
            
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        c.execute("SELECT id, price, quantity, category FROM products WHERE name=?", (product_name,))
        product = c.fetchone()
        
        if product:
            self.current_product_id = product[0]
            self.current_product_price = product[1]
            self.current_product_quantity = product[2]
            self.current_product_category = product[3]
            
            self.price_label.config(text=f"{product[1]:.2f} ج.م")
            self.quantity_label.config(text=str(product[2]))
            
            # تحديث السعر الإجمالي
            self.calculate_total()
        else:
            self.price_label.config(text="0.00 ج.م")
            self.quantity_label.config(text="0")
        
        conn.close()
    
    def calculate_total(self):
        quantity = self.sale_quantity.get()
        if hasattr(self, 'current_product_price'):
            total = quantity * self.current_product_price
            self.total_label.config(text=f"{total:.2f} ج.م")
    
    def complete_sale(self):
        product_name = self.product_var.get()
        quantity = self.sale_quantity.get()
        customer = self.customer_name_entry.get()
        
        if not product_name:
            messagebox.showerror("خطأ", "يرجى اختيار منتج")
            return
        
        if quantity <= 0:
            messagebox.showerror("خطأ", "الكمية يجب أن تكون أكبر من الصفر")
            return
        
        if not customer:
            customer = "عميل بدون اسم"
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        # الحصول على أحدث بيانات المنتج من قاعدة البيانات
        c.execute("SELECT id, price, quantity, category FROM products WHERE name=?", (product_name,))
        product = c.fetchone()
        
        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود")
            conn.close()
            return
        
        product_id, price, available_quantity, category = product
        
        if quantity > available_quantity:
            messagebox.showerror("خطأ", "الكمية المطلوبة غير متوفرة في المخزون")
            conn.close()
            return
        
        total = quantity * price
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        day_str = now.strftime("%A")  # اسم اليوم
        
        # عرض تفاصيل العملية قبل التأكيد
        confirm_msg = f"""
        تفاصيل عملية البيع:
        المنتج: {product_name}
        الفئة: {category}
        الكمية: {quantity}
        السعر: {price:.2f} ج.م
        الإجمالي: {total:.2f} ج.م
        المشتري: {customer}
        الموظف: {self.username}
        الكمية قبل البيع: {available_quantity}
        الكمية بعد البيع: {available_quantity - quantity}
        
        هل تريد تأكيد عملية البيع؟
        """
        
        if not messagebox.askyesno("تأكيد عملية البيع", confirm_msg):
            conn.close()
            return
        
        try:
            # تسجيل عملية البيع
            c.execute("""INSERT INTO sales 
                      (product_id, product_name, category, quantity, price, total, employee, customer_name, date, day) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (product_id, product_name, category, quantity, price, total, self.username, customer, date_str, day_str))
            
            # تحديث المخزون
            c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
            
            conn.commit()
            
            messagebox.showinfo("نجاح", "تمت عملية البيع بنجاح")
            
            # تحديث البيانات في جميع الأقسام
            self.update_product_details()
            if hasattr(self, 'inventory_tree'):
                self.load_inventory()
            if hasattr(self, 'sales_tree'):
                self.load_sales()
            if hasattr(self, 'sales_report_tree'):
                self.load_sales_report()
            
            # تحديث قائمة المنتجات بعد البيع
            self.update_products_list()
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("خطأ", f"حدث خطأ أثناء عملية البيع: {str(e)}")
        finally:
            conn.close()
    
    def create_inventory_tab(self):
        # إطار عرض المنتجات
        tree_frame = ttk.Frame(self.inventory_tab)
        tree_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        # شريط التمرير
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # جدول المنتجات
        self.inventory_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
        self.inventory_tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=self.inventory_tree.yview)
        
        # تعريف الأعمدة
        self.inventory_tree['columns'] = ('id', 'name', 'category', 'price', 'quantity')
        
        # تنسيق الأعمدة
        self.inventory_tree.column('#0', width=0, stretch=tk.NO)
        self.inventory_tree.column('id', width=70, anchor='center')
        self.inventory_tree.column('name', width=250, anchor='center')
        self.inventory_tree.column('category', width=180, anchor='center')
        self.inventory_tree.column('price', width=150, anchor='center')
        self.inventory_tree.column('quantity', width=120, anchor='center')
        
        # عناوين الأعمدة
        self.inventory_tree.heading('id', text='ID')
        self.inventory_tree.heading('name', text='اسم المنتج')
        self.inventory_tree.heading('category', text='الفئة')
        self.inventory_tree.heading('price', text='السعر')
        self.inventory_tree.heading('quantity', text='الكمية')
        
        # زر تحديث القائمة
        button_frame = ttk.Frame(self.inventory_tab)
        button_frame.pack(pady=15)
        
        self.style.configure('Table.TButton', font=('Arial', 12), padding=8)
        
        ttk.Button(button_frame, text="تحديث القائمة", command=self.load_inventory, 
                  style='Table.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="تصدير البيانات", command=self.export_inventory, 
                  style='Table.TButton').grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="استيراد البيانات", command=self.import_inventory, 
                  style='Table.TButton').grid(row=0, column=2, padx=10)
        
        # إطار إضافة/تعديل المنتج
        form_frame = ttk.LabelFrame(self.inventory_tab, text="إدارة المنتجات")
        form_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(form_frame, text="اسم المنتج:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.product_name = ttk.Entry(form_frame, font=('Arial', 12))
        self.product_name.grid(row=0, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="الفئة:", font=('Arial', 12)).grid(row=1, column=0, padx=15, pady=10)
        self.product_category = ttk.Combobox(form_frame, font=('Arial', 12), 
                                           values=['شحن', 'صيانة', 'إكسسوار', 'هاتف', 'قطع غيار'])
        self.product_category.grid(row=1, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="السعر:", font=('Arial', 12)).grid(row=2, column=0, padx=15, pady=10)
        self.product_price = ttk.Entry(form_frame, font=('Arial', 12))
        self.product_price.grid(row=2, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="الكمية:", font=('Arial', 12)).grid(row=3, column=0, padx=15, pady=10)
        self.product_quantity = ttk.Entry(form_frame, font=('Arial', 12))
        self.product_quantity.grid(row=3, column=1, padx=15, pady=10)
        
        # أزرار التحكم
        button_frame = ttk.Frame(self.inventory_tab)
        button_frame.pack(pady=15)
        
        self.style.configure('Form.TButton', font=('Arial', 12), padding=8)
        
        ttk.Button(button_frame, text="إضافة", command=self.add_product, 
                  style='Form.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="تحديث", command=self.update_product, 
                  style='Form.TButton').grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="حذف", command=self.delete_product, 
                  style='Form.TButton').grid(row=0, column=2, padx=10)
        ttk.Button(button_frame, text="مسح الحقول", command=self.clear_product_fields, 
                  style='Form.TButton').grid(row=0, column=3, padx=10)
        
        # ربط حدث اختيار عنصر في الجدول
        self.inventory_tree.bind('<<TreeviewSelect>>', self.select_product)
        
        # تحميل البيانات
        self.load_inventory()
    
    def load_inventory(self):
        # مسح البيانات الحالية
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM products ORDER BY name")
        products = c.fetchall()
        
        for product in products:
            self.inventory_tree.insert('', 'end', values=product)
        
        conn.close()
    
    def select_product(self, event):
        selected = self.inventory_tree.focus()
        if selected:
            values = self.inventory_tree.item(selected, 'values')
            
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, values[1])
            
            self.product_category.set(values[2])
            
            self.product_price.delete(0, tk.END)
            self.product_price.insert(0, values[3])
            
            self.product_quantity.delete(0, tk.END)
            self.product_quantity.insert(0, values[4])
    
    def clear_product_fields(self):
        self.product_name.delete(0, tk.END)
        self.product_category.set('')
        self.product_price.delete(0, tk.END)
        self.product_quantity.delete(0, tk.END)
    
    def add_product(self):
        name = self.product_name.get()
        category = self.product_category.get()
        price = self.product_price.get()
        quantity = self.product_quantity.get()
        
        if not name or not category or not price or not quantity:
            messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للسعر والكمية")
            return
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
                     (name, category, price, quantity))
            conn.commit()
            
            messagebox.showinfo("نجاح", "تمت إضافة المنتج بنجاح")
            self.load_inventory()
            self.clear_product_fields()
            self.update_categories()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("خطأ", "اسم المنتج موجود بالفعل")
        finally:
            conn.close()
    
    def update_product(self):
        selected = self.inventory_tree.focus()
        if not selected:
            messagebox.showerror("خطأ", "يرجى اختيار منتج للتحديث")
            return
        
        product_id = self.inventory_tree.item(selected, 'values')[0]
        name = self.product_name.get()
        category = self.product_category.get()
        price = self.product_price.get()
        quantity = self.product_quantity.get()
        
        if not name or not category or not price or not quantity:
            messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للسعر والكمية")
            return
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            c.execute("UPDATE products SET name=?, category=?, price=?, quantity=? WHERE id=?",
                     (name, category, price, quantity, product_id))
            conn.commit()
            
            messagebox.showinfo("نجاح", "تم تحديث المنتج بنجاح")
            self.load_inventory()
            self.clear_product_fields()
            self.update_categories()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("خطأ", "اسم المنتج موجود بالفعل")
        finally:
            conn.close()
    
    def delete_product(self):
        selected = self.inventory_tree.focus()
        if not selected:
            messagebox.showerror("خطأ", "يرجى اختيار منتج للحذف")
            return
        
        product_id = self.inventory_tree.item(selected, 'values')[0]
        product_name = self.inventory_tree.item(selected, 'values')[1]
        
        if not messagebox.askyesno("تأكيد", f"هل أنت متأكد من حذف المنتج '{product_name}'؟"):
            return
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            
            messagebox.showinfo("نجاح", "تم حذف المنتج بنجاح")
            self.load_inventory()
            self.clear_product_fields()
            self.update_categories()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحذف: {str(e)}")
        finally:
            conn.close()
    
    def export_inventory(self):
        folder_path = filedialog.askdirectory(title="اختر مجلد لحفظ البيانات")
        if not folder_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            
            # تصدير جدول المنتجات
            products = pd.read_sql_query("SELECT * FROM products", conn)
            products.to_csv(os.path.join(folder_path, 'منتجات.csv'), index=False, encoding='utf-8-sig')
            
            conn.close()
            
            messagebox.showinfo("نجاح", f"تم تصدير بيانات المخزون بنجاح إلى: {folder_path}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def import_inventory(self):
        file_path = filedialog.askopenfilename(filetypes=[("ملفات CSV", "*.csv"), ("كل الملفات", "*.*")],
                                             title="اختر ملف بيانات المخزون للاستيراد")
        if not file_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            c = conn.cursor()
            
            # استيراد المنتجات
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                try:
                    c.execute("INSERT OR REPLACE INTO products (id, name, category, price, quantity) VALUES (?, ?, ?, ?, ?)",
                             (row['id'], row['name'], row['category'], row['price'], row['quantity']))
                except:
                    # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                    c.execute("INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
                             (row['name'], row['category'], row['price'], row['quantity']))
            
            conn.commit()
            messagebox.showinfo("نجاح", "تم استيراد بيانات المخزون بنجاح")
            self.load_inventory()
            self.update_categories()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الاستيراد: {str(e)}")
    
    def create_maintenance_tab(self):
        # إطار عرض طلبات الصيانة
        tree_frame = ttk.Frame(self.maintenance_tab)
        tree_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        # شريط التمرير
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # جدول الصيانة
        self.maintenance_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
        self.maintenance_tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=self.maintenance_tree.yview)
        
        # تعريف الأعمدة
        self.maintenance_tree['columns'] = ('id', 'customer', 'device', 'issue', 'price', 'status', 'employee', 'date', 'day')
        
        # تنسيق الأعمدة
        self.maintenance_tree.column('#0', width=0, stretch=tk.NO)
        self.maintenance_tree.column('id', width=60, anchor='center')
        self.maintenance_tree.column('customer', width=180, anchor='center')
        self.maintenance_tree.column('device', width=180, anchor='center')
        self.maintenance_tree.column('issue', width=250, anchor='center')
        self.maintenance_tree.column('price', width=120, anchor='center')
        self.maintenance_tree.column('status', width=150, anchor='center')
        self.maintenance_tree.column('employee', width=120, anchor='center')
        self.maintenance_tree.column('date', width=180, anchor='center')
        self.maintenance_tree.column('day', width=120, anchor='center')
        
        # عناوين الأعمدة
        self.maintenance_tree.heading('id', text='ID')
        self.maintenance_tree.heading('customer', text='اسم العميل')
        self.maintenance_tree.heading('device', text='نوع الجهاز')
        self.maintenance_tree.heading('issue', text='العطل')
        self.maintenance_tree.heading('price', text='السعر')
        self.maintenance_tree.heading('status', text='الحالة')
        self.maintenance_tree.heading('employee', text='الموظف')
        self.maintenance_tree.heading('date', text='التاريخ')
        self.maintenance_tree.heading('day', text='اليوم')
        
        # زر تحديث القائمة
        button_frame = ttk.Frame(self.maintenance_tab)
        button_frame.pack(pady=15)
        
        self.style.configure('Table.TButton', font=('Arial', 12), padding=8)
        
        ttk.Button(button_frame, text="تحديث القائمة", command=self.load_maintenance, 
                  style='Table.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="تصدير البيانات", command=self.export_maintenance, 
                  style='Table.TButton').grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="استيراد البيانات", command=self.import_maintenance, 
                  style='Table.TButton').grid(row=0, column=2, padx=10)
        
        # إطار إضافة/تعديل طلب الصيانة
        form_frame = ttk.LabelFrame(self.maintenance_tab, text="إدارة طلبات الصيانة")
        form_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(form_frame, text="اسم العميل:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.customer_name = ttk.Entry(form_frame, font=('Arial', 12))
        self.customer_name.grid(row=0, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="نوع الجهاز:", font=('Arial', 12)).grid(row=1, column=0, padx=15, pady=10)
        self.device_type = ttk.Entry(form_frame, font=('Arial', 12))
        self.device_type.grid(row=1, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="العطل:", font=('Arial', 12)).grid(row=2, column=0, padx=15, pady=10)
        self.issue = ttk.Entry(form_frame, font=('Arial', 12))
        self.issue.grid(row=2, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="السعر:", font=('Arial', 12)).grid(row=3, column=0, padx=15, pady=10)
        self.maintenance_price = ttk.Entry(form_frame, font=('Arial', 12))
        self.maintenance_price.grid(row=3, column=1, padx=15, pady=10)
        
        ttk.Label(form_frame, text="الحالة:", font=('Arial', 12)).grid(row=4, column=0, padx=15, pady=10)
        self.status = ttk.Combobox(form_frame, font=('Arial', 12), 
                                 values=['قيد الإصلاح', 'تم التسليم'], state='readonly')
        self.status.grid(row=4, column=1, padx=15, pady=10)
        
        # أزرار التحكم
        button_frame = ttk.Frame(self.maintenance_tab)
        button_frame.pack(pady=15)
        
        self.style.configure('Form.TButton', font=('Arial', 12), padding=8)
        
        ttk.Button(button_frame, text="إضافة", command=self.add_maintenance, 
                  style='Form.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="تحديث", command=self.update_maintenance, 
                  style='Form.TButton').grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="حذف", command=self.delete_maintenance, 
                  style='Form.TButton').grid(row=0, column=2, padx=10)
        ttk.Button(button_frame, text="مسح الحقول", command=self.clear_maintenance_fields, 
                  style='Form.TButton').grid(row=0, column=3, padx=10)
        
        # ربط حدث اختيار عنصر في الجدول
        self.maintenance_tree.bind('<<TreeviewSelect>>', self.select_maintenance)
        
        # تحميل البيانات
        self.load_maintenance()
    
    def load_maintenance(self):
        # مسح البيانات الحالية
        for item in self.maintenance_tree.get_children():
            self.maintenance_tree.delete(item)
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM maintenance ORDER BY date DESC")
        maintenance_requests = c.fetchall()
        
        for request in maintenance_requests:
            self.maintenance_tree.insert('', 'end', values=request)
        
        conn.close()
    
    def select_maintenance(self, event):
        selected = self.maintenance_tree.focus()
        if selected:
            values = self.maintenance_tree.item(selected, 'values')
            
            self.customer_name.delete(0, tk.END)
            self.customer_name.insert(0, values[1])
            
            self.device_type.delete(0, tk.END)
            self.device_type.insert(0, values[2])
            
            self.issue.delete(0, tk.END)
            self.issue.insert(0, values[3])
            
            self.maintenance_price.delete(0, tk.END)
            self.maintenance_price.insert(0, values[4])
            
            self.status.set(values[5])
    
    def clear_maintenance_fields(self):
        self.customer_name.delete(0, tk.END)
        self.device_type.delete(0, tk.END)
        self.issue.delete(0, tk.END)
        self.maintenance_price.delete(0, tk.END)
        self.status.set('')
    
    def add_maintenance(self):
        customer = self.customer_name.get()
        device = self.device_type.get()
        issue = self.issue.get()
        price = self.maintenance_price.get()
        status = self.status.get()
        
        if not customer or not device or not issue or not price or not status:
            messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return
        
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيمة صحيحة للسعر")
            return
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        day_str = now.strftime("%A")  # اسم اليوم
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            c.execute("""INSERT INTO maintenance 
                      (customer_name, device_type, issue, price, status, employee, date, day) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                     (customer, device, issue, price, status, self.username, date_str, day_str))
            conn.commit()
            
            messagebox.showinfo("نجاح", "تمت إضافة طلب الصيانة بنجاح")
            self.load_maintenance()
            self.clear_maintenance_fields()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الإضافة: {str(e)}")
        finally:
            conn.close()
    
    def update_maintenance(self):
        selected = self.maintenance_tree.focus()
        if not selected:
            messagebox.showerror("خطأ", "يرجى اختيار طلب صيانة للتحديث")
            return
        
        request_id = self.maintenance_tree.item(selected, 'values')[0]
        customer = self.customer_name.get()
        device = self.device_type.get()
        issue = self.issue.get()
        price = self.maintenance_price.get()
        status = self.status.get()
        
        if not customer or not device or not issue or not price or not status:
            messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return
        
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيمة صحيحة للسعر")
            return
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            c.execute("""UPDATE maintenance SET 
                      customer_name=?, device_type=?, issue=?, price=?, status=? 
                      WHERE id=?""",
                     (customer, device, issue, price, status, request_id))
            conn.commit()
            
            messagebox.showinfo("نجاح", "تم تحديث طلب الصيانة بنجاح")
            self.load_maintenance()
            self.clear_maintenance_fields()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التحديث: {str(e)}")
        finally:
            conn.close()
    
    def delete_maintenance(self):
        selected = self.maintenance_tree.focus()
        if not selected:
            messagebox.showerror("خطأ", "يرجى اختيار طلب صيانة للحذف")
            return
        
        request_id = self.maintenance_tree.item(selected, 'values')[0]
        customer_name = self.maintenance_tree.item(selected, 'values')[1]
        
        if not messagebox.askyesno("تأكيد", f"هل أنت متأكد من حذف طلب الصيانة للعميل '{customer_name}'؟"):
            return
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM maintenance WHERE id=?", (request_id,))
            conn.commit()
            
            messagebox.showinfo("نجاح", "تم حذف طلب الصيانة بنجاح")
            self.load_maintenance()
            self.clear_maintenance_fields()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحذف: {str(e)}")
        finally:
            conn.close()
    
    def export_maintenance(self):
        folder_path = filedialog.askdirectory(title="اختر مجلد لحفظ البيانات")
        if not folder_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            
            # تصدير جدول الصيانة
            maintenance = pd.read_sql_query("SELECT * FROM maintenance", conn)
            maintenance.to_csv(os.path.join(folder_path, 'صيانة.csv'), index=False, encoding='utf-8-sig')
            
            conn.close()
            
            messagebox.showinfo("نجاح", f"تم تصدير بيانات الصيانة بنجاح إلى: {folder_path}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def import_maintenance(self):
        file_path = filedialog.askopenfilename(filetypes=[("ملفات CSV", "*.csv"), ("كل الملفات", "*.*")],
                                             title="اختر ملف بيانات الصيانة للاستيراد")
        if not file_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            c = conn.cursor()
            
            # استيراد الصيانة
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                try:
                    c.execute("""INSERT OR REPLACE INTO maintenance 
                              (id, customer_name, device_type, issue, price, status, employee, date, day) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                             (row['id'], row['customer_name'], row['device_type'], row['issue'], 
                              row['price'], row['status'], row['employee'], row['date'], row['day']))
                except:
                    # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                    c.execute("""INSERT INTO maintenance 
                              (customer_name, device_type, issue, price, status, employee, date, day) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                             (row['customer_name'], row['device_type'], row['issue'], 
                              row['price'], row['status'], row['employee'], row['date'], row['day']))
            
            conn.commit()
            messagebox.showinfo("نجاح", "تم استيراد بيانات الصيانة بنجاح")
            self.load_maintenance()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الاستيراد: {str(e)}")
    
    def create_sales_report_tab(self):
        # إطار الفلاتر
        filter_frame = ttk.LabelFrame(self.sales_report_tab, text="تصفية المبيعات")
        filter_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(filter_frame, text="من تاريخ:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.sales_from_date = ttk.Entry(filter_frame, font=('Arial', 12))
        self.sales_from_date.grid(row=0, column=1, padx=15, pady=10)
        self.sales_from_date.insert(0, datetime.now().strftime("%Y-%m-01"))
        
        ttk.Label(filter_frame, text="إلى تاريخ:", font=('Arial', 12)).grid(row=0, column=2, padx=15, pady=10)
        self.sales_to_date = ttk.Entry(filter_frame, font=('Arial', 12))
        self.sales_to_date.grid(row=0, column=3, padx=15, pady=10)
        self.sales_to_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(filter_frame, text="تطبيق الفلتر", command=self.load_sales_report, 
                  style='Table.TButton').grid(row=0, column=4, padx=15, pady=10)
        
        # إطار عرض المبيعات
        tree_frame = ttk.Frame(self.sales_report_tab)
        tree_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        # شريط التمرير
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # جدول المبيعات
        self.sales_report_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        self.sales_report_tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=self.sales_report_tree.yview)
        
        # تعريف الأعمدة
        self.sales_report_tree['columns'] = ('id', 'date', 'day', 'product', 'category', 'quantity', 'price', 'total', 'customer', 'employee')
        
        # تنسيق الأعمدة
        self.sales_report_tree.column('#0', width=0, stretch=tk.NO)
        self.sales_report_tree.column('id', width=60, anchor='center')
        self.sales_report_tree.column('date', width=180, anchor='center')
        self.sales_report_tree.column('day', width=120, anchor='center')
        self.sales_report_tree.column('product', width=200, anchor='center')
        self.sales_report_tree.column('category', width=150, anchor='center')
        self.sales_report_tree.column('quantity', width=100, anchor='center')
        self.sales_report_tree.column('price', width=120, anchor='center')
        self.sales_report_tree.column('total', width=150, anchor='center')
        self.sales_report_tree.column('customer', width=180, anchor='center')
        self.sales_report_tree.column('employee', width=150, anchor='center')
        
        # عناوين الأعمدة
        self.sales_report_tree.heading('id', text='ID')
        self.sales_report_tree.heading('date', text='التاريخ')
        self.sales_report_tree.heading('day', text='اليوم')
        self.sales_report_tree.heading('product', text='المنتج')
        self.sales_report_tree.heading('category', text='الفئة')
        self.sales_report_tree.heading('quantity', text='الكمية')
        self.sales_report_tree.heading('price', text='السعر')
        self.sales_report_tree.heading('total', text='الإجمالي')
        self.sales_report_tree.heading('customer', text='المشتري')
        self.sales_report_tree.heading('employee', text='الموظف')
        
        # إجمالي المبيعات
        self.sales_total_label = ttk.Label(self.sales_report_tab, text="إجمالي المبيعات: 0.00 ج.م", 
                                         font=('Arial', 14, 'bold'), foreground="#27ae60")
        self.sales_total_label.pack(pady=15)
        
        # أزرار التحكم
        button_frame = ttk.Frame(self.sales_report_tab)
        button_frame.pack(pady=10)
        
        self.style.configure('Table.TButton', font=('Arial', 12), padding=8)
        
        ttk.Button(button_frame, text="تصدير البيانات", command=self.export_sales, 
                  style='Table.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="استيراد البيانات", command=self.import_sales, 
                  style='Table.TButton').grid(row=0, column=1, padx=10)
        
        # تحميل البيانات
        self.load_sales_report()
    
    def load_sales_report(self):
        # مسح البيانات الحالية
        for item in self.sales_report_tree.get_children():
            self.sales_report_tree.delete(item)
        
        from_date = self.sales_from_date.get()
        to_date = self.sales_to_date.get()
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            # تحويل تواريخ النص إلى كائنات تاريخ للتحقق من الصحة
            datetime.strptime(from_date, "%Y-%m-%d")
            datetime.strptime(to_date, "%Y-%m-%d")
            
            if self.role == 'admin':
                c.execute("SELECT * FROM sales WHERE date BETWEEN ? AND ? ORDER BY date DESC", (from_date, to_date))
            else:
                c.execute("SELECT * FROM sales WHERE employee=? AND date BETWEEN ? AND ? ORDER BY date DESC", 
                         (self.username, from_date, to_date))
            
            sales = c.fetchall()
            
            total_sales = 0
            
            for sale in sales:
                # ترتيب البيانات حسب الأعمدة الجديدة
                values = (
                    sale[0],  # id
                    sale[9],  # date
                    sale[10], # day
                    sale[2],  # product_name
                    sale[3],  # category
                    sale[4],  # quantity
                    sale[5],  # price
                    sale[6],  # total
                    sale[8],  # customer_name
                    sale[7]   # employee
                )
                self.sales_report_tree.insert('', 'end', values=values)
                total_sales += sale[6]  # العمود 6 هو الإجمالي
            
            self.sales_total_label.config(text=f"إجمالي المبيعات: {total_sales:.2f} ج.م")
            
        except ValueError:
            messagebox.showerror("خطأ", "صيغة التاريخ غير صحيحة. استخدم YYYY-MM-DD")
        finally:
            conn.close()
    
    def export_sales(self):
        folder_path = filedialog.askdirectory(title="اختر مجلد لحفظ البيانات")
        if not folder_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            
            # تصدير جدول المبيعات
            if self.role == 'admin':
                sales = pd.read_sql_query("SELECT * FROM sales", conn)
            else:
                sales = pd.read_sql_query(f"SELECT * FROM sales WHERE employee='{self.username}'", conn)
                
            sales.to_csv(os.path.join(folder_path, 'مبيعات.csv'), index=False, encoding='utf-8-sig')
            
            conn.close()
            
            messagebox.showinfo("نجاح", f"تم تصدير بيانات المبيعات بنجاح إلى: {folder_path}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def import_sales(self):
        file_path = filedialog.askopenfilename(filetypes=[("ملفات CSV", "*.csv"), ("كل الملفات", "*.*")],
                                             title="اختر ملف بيانات المبيعات للاستيراد")
        if not file_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            c = conn.cursor()
            
            # استيراد المبيعات
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                try:
                    c.execute("""INSERT OR REPLACE INTO sales 
                              (id, product_id, product_name, category, quantity, price, total, employee, customer_name, date, day) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                             (row['id'], row['product_id'], row['product_name'], row['category'], 
                              row['quantity'], row['price'], row['total'], row['employee'], 
                              row['customer_name'], row['date'], row['day']))
                except:
                    # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                    c.execute("""INSERT INTO sales 
                              (product_id, product_name, category, quantity, price, total, employee, customer_name, date, day) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                             (row['product_id'], row['product_name'], row['category'], 
                              row['quantity'], row['price'], row['total'], row['employee'], 
                              row['customer_name'], row['date'], row['day']))
            
            conn.commit()
            messagebox.showinfo("نجاح", "تم استيراد بيانات المبيعات بنجاح")
            self.load_sales_report()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الاستيراد: {str(e)}")
    
    def create_reports_tab(self):
        # إطار الفلاتر
        filter_frame = ttk.LabelFrame(self.reports_tab, text="تصفية المبيعات")
        filter_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(filter_frame, text="من تاريخ:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.from_date = ttk.Entry(filter_frame, font=('Arial', 12))
        self.from_date.grid(row=0, column=1, padx=15, pady=10)
        self.from_date.insert(0, datetime.now().strftime("%Y-%m-01"))
        
        ttk.Label(filter_frame, text="إلى تاريخ:", font=('Arial', 12)).grid(row=0, column=2, padx=15, pady=10)
        self.to_date = ttk.Entry(filter_frame, font=('Arial', 12))
        self.to_date.grid(row=0, column=3, padx=15, pady=10)
        self.to_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(filter_frame, text="تطبيق الفلتر", command=self.load_sales, 
                  style='Table.TButton').grid(row=0, column=4, padx=15, pady=10)
        
        # إطار عرض المبيعات
        tree_frame = ttk.Frame(self.reports_tab)
        tree_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        # شريط التمرير
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # جدول المبيعات
        self.sales_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        self.sales_tree.pack(fill='both', expand=True)
        
        tree_scroll.config(command=self.sales_tree.yview)
        
        # تعريف الأعمدة
        self.sales_tree['columns'] = ('id', 'date', 'product', 'category', 'quantity', 'price', 'total', 'customer', 'employee')
        
        # تنسيق الأعمدة
        self.sales_tree.column('#0', width=0, stretch=tk.NO)
        self.sales_tree.column('id', width=60, anchor='center')
        self.sales_tree.column('date', width=180, anchor='center')
        self.sales_tree.column('product', width=200, anchor='center')
        self.sales_tree.column('category', width=150, anchor='center')
        self.sales_tree.column('quantity', width=100, anchor='center')
        self.sales_tree.column('price', width=120, anchor='center')
        self.sales_tree.column('total', width=150, anchor='center')
        self.sales_tree.column('customer', width=180, anchor='center')
        self.sales_tree.column('employee', width=150, anchor='center')
        
        # عناوين الأعمدة
        self.sales_tree.heading('id', text='ID')
        self.sales_tree.heading('date', text='التاريخ')
        self.sales_tree.heading('product', text='المنتج')
        self.sales_tree.heading('category', text='الفئة')
        self.sales_tree.heading('quantity', text='الكمية')
        self.sales_tree.heading('price', text='السعر')
        self.sales_tree.heading('total', text='الإجمالي')
        self.sales_tree.heading('customer', text='المشتري')
        self.sales_tree.heading('employee', text='الموظف')
        
        # إجمالي المبيعات
        self.total_sales_label = ttk.Label(self.reports_tab, text="إجمالي المبيعات: 0.00 ج.م", 
                                         font=('Arial', 14, 'bold'), foreground="#27ae60")
        self.total_sales_label.pack(pady=15)
        
        # أزرار التحكم
        button_frame = ttk.Frame(self.reports_tab)
        button_frame.pack(pady=10)
        
        self.style.configure('Table.TButton', font=('Arial', 12), padding=8)
        
        ttk.Button(button_frame, text="تصدير البيانات", command=self.export_admin_sales, 
                  style='Table.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="استيراد البيانات", command=self.import_sales, 
                  style='Table.TButton').grid(row=0, column=1, padx=10)
        
        # تحميل البيانات
        self.load_sales()
    
    def create_profit_tab(self):
        # إطار الفلاتر
        filter_frame = ttk.LabelFrame(self.profit_tab, text="تصفية الأرباح")
        filter_frame.pack(pady=15, padx=20, fill='x')
        
        ttk.Label(filter_frame, text="من تاريخ:", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=10)
        self.profit_from_date = ttk.Entry(filter_frame, font=('Arial', 12))
        self.profit_from_date.grid(row=0, column=1, padx=15, pady=10)
        self.profit_from_date.insert(0, datetime.now().strftime("%Y-%m-01"))
        
        ttk.Label(filter_frame, text="إلى تاريخ:", font=('Arial', 12)).grid(row=0, column=2, padx=15, pady=10)
        self.profit_to_date = ttk.Entry(filter_frame, font=('Arial', 12))
        self.profit_to_date.grid(row=0, column=3, padx=15, pady=10)
        self.profit_to_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(filter_frame, text="تطبيق الفلتر", command=self.calculate_profit, 
                  style='Table.TButton').grid(row=0, column=4, padx=15, pady=10)
        
        # إطار النتائج
        result_frame = ttk.LabelFrame(self.profit_tab, text="نتائج الأرباح")
        result_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        ttk.Label(result_frame, text="إجمالي المبيعات:", font=('Arial', 14)).grid(row=0, column=0, padx=20, pady=15, sticky='e')
        self.total_sales_amount = ttk.Label(result_frame, text="0.00 ج.م", font=('Arial', 14, 'bold'), foreground="#3498db")
        self.total_sales_amount.grid(row=0, column=1, padx=20, pady=15, sticky='w')
        
        ttk.Label(result_frame, text="إجمالي الصيانة:", font=('Arial', 14)).grid(row=1, column=0, padx=20, pady=15, sticky='e')
        self.total_maintenance_amount = ttk.Label(result_frame, text="0.00 ج.م", font=('Arial', 14, 'bold'), foreground="#3498db")
        self.total_maintenance_amount.grid(row=1, column=1, padx=20, pady=15, sticky='w')
        
        ttk.Label(result_frame, text="الإجمالي الكلي:", font=('Arial', 16)).grid(row=2, column=0, padx=20, pady=20, sticky='e')
        self.grand_total_amount = ttk.Label(result_frame, text="0.00 ج.م", font=('Arial', 18, 'bold'), foreground="#27ae60")
        self.grand_total_amount.grid(row=2, column=1, padx=20, pady=20, sticky='w')
        
        # زر تصدير البيانات
        ttk.Button(self.profit_tab, text="تصدير التقرير", command=self.export_profit_report, 
                  style='Action.TButton').pack(pady=15)
        
        # حساب الأرباح أول مرة
        self.calculate_profit()
    
    def calculate_profit(self):
        from_date = self.profit_from_date.get()
        to_date = self.profit_to_date.get()
        
        try:
            # تحقق من صحة التواريخ
            datetime.strptime(from_date, "%Y-%m-%d")
            datetime.strptime(to_date, "%Y-%m-%d")
            
            conn = sqlite3.connect('masry_phone.db')
            c = conn.cursor()
            
            # حساب إجمالي المبيعات
            c.execute("SELECT SUM(total) FROM sales WHERE date BETWEEN ? AND ?", (from_date, to_date))
            sales_total = c.fetchone()[0] or 0
            
            # حساب إجمالي الصيانة
            c.execute("SELECT SUM(price) FROM maintenance WHERE date BETWEEN ? AND ? AND status='تم التسليم'", (from_date, to_date))
            maintenance_total = c.fetchone()[0] or 0
            
            conn.close()
            
            # تحديث الواجهة
            self.total_sales_amount.config(text=f"{sales_total:.2f} ج.م")
            self.total_maintenance_amount.config(text=f"{maintenance_total:.2f} ج.م")
            self.grand_total_amount.config(text=f"{sales_total + maintenance_total:.2f} ج.م")
            
        except ValueError:
            messagebox.showerror("خطأ", "صيغة التاريخ غير صحيحة. استخدم YYYY-MM-DD")
    
    def export_profit_report(self):
        from_date = self.profit_from_date.get()
        to_date = self.profit_to_date.get()
        sales_total = float(self.total_sales_amount.cget('text').split()[0])
        maintenance_total = float(self.total_maintenance_amount.cget('text').split()[0])
        grand_total = sales_total + maintenance_total
        
        # إنشاء DataFrame للتصدير
        data = {
            'البند': ['إجمالي المبيعات', 'إجمالي الصيانة', 'الإجمالي الكلي'],
            'المبلغ': [sales_total, maintenance_total, grand_total]
        }
        df = pd.DataFrame(data)
        
        # اختيار مكان الحفظ
        folder_path = filedialog.askdirectory(title="اختر مجلد لحفظ البيانات")
        if not folder_path:
            return
        
        try:
            file_path = os.path.join(folder_path, f"تقرير_الأرباح_{from_date}_إلى_{to_date}.csv")
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("نجاح", f"تم تصدير التقرير بنجاح إلى: {file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def export_admin_sales(self):
        from_date = self.from_date.get()
        to_date = self.to_date.get()
        
        # اختيار مكان الحفظ
        folder_path = filedialog.askdirectory(title="اختر مجلد لحفظ البيانات")
        if not folder_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            query = "SELECT * FROM sales WHERE date BETWEEN ? AND ? ORDER BY date DESC"
            sales = pd.read_sql_query(query, conn, params=(from_date, to_date))
            file_path = os.path.join(folder_path, f"المبيعات_الإدارية_{from_date}_إلى_{to_date}.csv")
            sales.to_csv(file_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("نجاح", f"تم التصدير إلى {file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
        finally:
            conn.close()
    
    def load_sales(self):
        # مسح البيانات الحالية
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        from_date = self.from_date.get()
        to_date = self.to_date.get()
        
        conn = sqlite3.connect('masry_phone.db')
        c = conn.cursor()
        
        try:
            # تحويل تواريخ النص إلى كائنات تاريخ للتحقق من الصحة
            datetime.strptime(from_date, "%Y-%m-%d")
            datetime.strptime(to_date, "%Y-%m-%d")
            
            c.execute("SELECT * FROM sales WHERE date BETWEEN ? AND ? ORDER BY date DESC", (from_date, to_date))
            sales = c.fetchall()
            
            total_sales = 0
            
            for sale in sales:
                # ترتيب البيانات حسب الأعمدة الجديدة
                values = (
                    sale[0],  # id
                    sale[9],  # date
                    sale[2],  # product_name
                    sale[3],  # category
                    sale[4],  # quantity
                    sale[5],  # price
                    sale[6],  # total
                    sale[8],  # customer_name
                    sale[7]   # employee
                )
                self.sales_tree.insert('', 'end', values=values)
                total_sales += sale[6]  # العمود 6 هو الإجمالي
            
            self.total_sales_label.config(text=f"إجمالي المبيعات: {total_sales:.2f} ج.م")
            
        except ValueError:
            messagebox.showerror("خطأ", "صيغة التاريخ غير صحيحة. استخدم YYYY-MM-DD")
        finally:
            conn.close()
    
    def export_all_data(self):
        # اختيار مكان الحفظ
        folder_path = filedialog.askdirectory(title="اختر مجلد لحفظ البيانات")
        if not folder_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            
            # تصدير جدول المنتجات
            products = pd.read_sql_query("SELECT * FROM products", conn)
            products.to_csv(os.path.join(folder_path, 'منتجات.csv'), index=False, encoding='utf-8-sig')
            
            # تصدير جدول المبيعات
            sales = pd.read_sql_query("SELECT * FROM sales", conn)
            sales.to_csv(os.path.join(folder_path, 'مبيعات.csv'), index=False, encoding='utf-8-sig')
            
            # تصدير جدول الصيانة
            maintenance = pd.read_sql_query("SELECT * FROM maintenance", conn)
            maintenance.to_csv(os.path.join(folder_path, 'صيانة.csv'), index=False, encoding='utf-8-sig')
            
            # تصدير جدول المستخدمين (للمدير فقط)
            users = pd.read_sql_query("SELECT * FROM users", conn)
            users.to_csv(os.path.join(folder_path, 'مستخدمين.csv'), index=False, encoding='utf-8-sig')
            
            conn.close()
            
            messagebox.showinfo("نجاح", f"تم تصدير جميع البيانات بنجاح إلى المجلد: {folder_path}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def import_all_data(self):
        # اختيار ملف الاستيراد
        file_path = filedialog.askopenfilename(filetypes=[("ملفات CSV", "*.csv"), ("كل الملفات", "*.*")],
                                             title="اختر ملف البيانات للاستيراد")
        if not file_path:
            return
        
        try:
            conn = sqlite3.connect('masry_phone.db')
            c = conn.cursor()
            
            # تحديد نوع البيانات من اسم الملف
            if 'منتجات' in file_path:
                # استيراد المنتجات
                df = pd.read_csv(file_path)
                
                for _, row in df.iterrows():
                    try:
                        c.execute("INSERT OR REPLACE INTO products (id, name, category, price, quantity) VALUES (?, ?, ?, ?, ?)",
                                 (row['id'], row['name'], row['category'], row['price'], row['quantity']))
                    except:
                        # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                        c.execute("INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
                                 (row['name'], row['category'], row['price'], row['quantity']))
                
                conn.commit()
                messagebox.showinfo("نجاح", "تم استيراد بيانات المنتجات بنجاح")
                self.load_inventory()
                self.update_categories()
                
            elif 'مبيعات' in file_path:
                # استيراد المبيعات
                df = pd.read_csv(file_path)
                
                for _, row in df.iterrows():
                    try:
                        c.execute("""INSERT OR REPLACE INTO sales 
                                  (id, product_id, product_name, category, quantity, price, total, employee, customer_name, date, day) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (row['id'], row['product_id'], row['product_name'], row['category'], 
                                  row['quantity'], row['price'], row['total'], row['employee'], 
                                  row['customer_name'], row['date'], row['day']))
                    except:
                        # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                        c.execute("""INSERT INTO sales 
                                  (product_id, product_name, category, quantity, price, total, employee, customer_name, date, day) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (row['product_id'], row['product_name'], row['category'], 
                                  row['quantity'], row['price'], row['total'], row['employee'], 
                                  row['customer_name'], row['date'], row['day']))
                
                conn.commit()
                messagebox.showinfo("نجاح", "تم استيراد بيانات المبيعات بنجاح")
                if hasattr(self, 'sales_tree'):
                    self.load_sales()
                if hasattr(self, 'sales_report_tree'):
                    self.load_sales_report()
                
            elif 'صيانة' in file_path:
                # استيراد الصيانة
                df = pd.read_csv(file_path)
                
                for _, row in df.iterrows():
                    try:
                        c.execute("""INSERT OR REPLACE INTO maintenance 
                                  (id, customer_name, device_type, issue, price, status, employee, date, day) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (row['id'], row['customer_name'], row['device_type'], row['issue'], 
                                  row['price'], row['status'], row['employee'], row['date'], row['day']))
                    except:
                        # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                        c.execute("""INSERT INTO maintenance 
                                  (customer_name, device_type, issue, price, status, employee, date, day) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (row['customer_name'], row['device_type'], row['issue'], 
                                  row['price'], row['status'], row['employee'], row['date'], row['day']))
                
                conn.commit()
                messagebox.showinfo("نجاح", "تم استيراد بيانات الصيانة بنجاح")
                if hasattr(self, 'maintenance_tree'):
                    self.load_maintenance()
            
            elif 'مستخدمين' in file_path and self.role == 'admin':
                # استيراد المستخدمين (للمدير فقط)
                df = pd.read_csv(file_path)
                
                for _, row in df.iterrows():
                    try:
                        c.execute("INSERT OR REPLACE INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
                                 (row['id'], row['username'], row['password'], row['role']))
                    except:
                        # إذا كان ID غير موجود (لإضافة سجلات جديدة)
                        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                 (row['username'], row['password'], row['role']))
                
                conn.commit()
                messagebox.showinfo("نجاح", "تم استيراد بيانات المستخدمين بنجاح")
            
            else:
                messagebox.showerror("خطأ", "اسم الملف غير معروف أو ليس لديك الصلاحيات الكافية")
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الاستيراد: {str(e)}")
    
    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

# تشغيل البرنامج
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
