import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# Clase University
class University:
    def __init__(self, id, name, monthlyIncome, numberOfStudent):
        self.id = id
        self.name = name
        self.monthlyIncome = monthlyIncome
        self.numberOfStudent = numberOfStudent

# Clase lógica de negocio
class UniversityBusiness:
    def __init__(self, university):
        self.university = university

    def income_per_student(self):
        if self.university.numberOfStudent == 0:
            return 0
        return self.university.monthlyIncome / self.university.numberOfStudent

# Conexión a MongoDB
class MongoConnection:
    def __init__(self):
        user = "isaac"
        password = "isaac"  # Cambia por tu contraseña real
        cluster = "cluster0.xaitfht"
        uri = f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri)
        self.db = self.client["University"]

    def get_universities(self):
        collection = self.db["university"]
        documents = collection.find()
        universities = []
        for doc in documents:
            u = University(
                doc.get("id"),
                doc.get("name"),
                doc.get("monthlyIncome"),
                doc.get("numberOfStudent")
            )
            universities.append(u)
        return universities

    def insert_university(self, university):
        collection = self.db["university"]
        data = {
            "id": university.id,
            "name": university.name,
            "monthlyIncome": university.monthlyIncome,
            "numberOfStudent": university.numberOfStudent
        }
        collection.insert_one(data)

    def close(self):
        self.client.close()

# Ventana para crear universidad
class CreateWindow(tk.Toplevel):
    def __init__(self, parent, mongo):
        super().__init__(parent)
        self.title("Crear Universidad")
        self.geometry("400x300")
        self.resizable(False, False)
        self.mongo = mongo

        tk.Label(self, text="Id (entero):").pack(pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        tk.Label(self, text="Nombre:").pack(pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        tk.Label(self, text="Ingreso Mensual (decimal):").pack(pady=5)
        self.entry_income = tk.Entry(self)
        self.entry_income.pack()

        tk.Label(self, text="Nro de Estudiantes (entero):").pack(pady=5)
        self.entry_students = tk.Entry(self)
        self.entry_students.pack()

        tk.Button(self, text="Guardar Universidad", command=self.save_university).pack(pady=15)

    def save_university(self):
        try:
            id = int(self.entry_id.get())
            name = self.entry_name.get()
            income = float(self.entry_income.get())
            students = int(self.entry_students.get())

            if not name:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return

            university = University(id, name, income, students)
            self.mongo.insert_university(university)
            messagebox.showinfo("Éxito", "Universidad guardada exitosamente.")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa datos válidos (números correctos).")

# Ventana para mostrar cálculo de ingreso por estudiante
class CalcWindow(tk.Toplevel):
    def __init__(self, parent, universities):
        super().__init__(parent)
        self.title("Ingreso Promedio por Estudiante")
        self.geometry("750x400")
        self.resizable(False, False)

        columns = ("Id", "Nombre", "Ingreso Mensual", "Nro Estudiantes", "Ingreso/Estudiante")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for u in universities:
            business = UniversityBusiness(u)
            income = business.income_per_student()
            tree.insert("", tk.END, values=(
                u.id,
                u.name,
                u.monthlyIncome,
                u.numberOfStudent,
                f"{income:.2f}"
            ))

# Ventana principal con menú
class FrmMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("University Manager - Menú")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self.mongo = MongoConnection()

        lbl_title = tk.Label(root, text="Menú Principal", font=("Arial", 20, "bold"))
        lbl_title.pack(pady=20)

        btn_create = tk.Button(root, text="Crear Universidad", width=25, command=self.open_create)
        btn_create.pack(pady=10)

        btn_calc = tk.Button(root, text="Calcular Ingreso por Estudiante", width=25, command=self.open_calc)
        btn_calc.pack(pady=10)

    def open_create(self):
        CreateWindow(self.root, self.mongo)

    def open_calc(self):
        universities = self.mongo.get_universities()
        if not universities:
            messagebox.showinfo("Información", "No hay universidades registradas.")
            return
        CalcWindow(self.root, universities)

if __name__ == "__main__":
    root = tk.Tk()
    app = FrmMenu(root)
    root.mainloop()
