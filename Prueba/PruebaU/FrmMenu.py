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

    def update_university(self, university):
        collection = self.db["university"]
        result = collection.update_one(
            {"id": university.id},
            {"$set": {
                "name": university.name,
                "monthlyIncome": university.monthlyIncome,
                "numberOfStudent": university.numberOfStudent
            }}
        )
        return result.matched_count > 0

    def close(self):
        self.client.close()

# Ventana para actualizar universidad con tabla visible
class UpdateWindow(tk.Toplevel):
    def __init__(self, parent, mongo):
        super().__init__(parent)
        self.title("Actualizar Universidad")
        self.geometry("700x500")
        self.resizable(False, False)
        self.mongo = mongo

        # Tabla de universidades
        columns = ("Id", "Nombre", "Ingreso Mensual", "Nro Estudiantes")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_universities()

        # Formulario de actualización
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Id a actualizar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(form_frame)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nuevo Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nuevo Ingreso Mensual:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_income = tk.Entry(form_frame)
        self.entry_income.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nuevo Nro Estudiantes:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_students = tk.Entry(form_frame)
        self.entry_students.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self, text="Actualizar Universidad", command=self.update_university).pack(pady=10)

    def load_universities(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        universities = self.mongo.get_universities()
        for u in universities:
            self.tree.insert("", tk.END, values=(u.id, u.name, u.monthlyIncome, u.numberOfStudent))

    def update_university(self):
        try:
            id = int(self.entry_id.get())
            name = self.entry_name.get()
            income = float(self.entry_income.get())
            students = int(self.entry_students.get())

            if not name:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return

            university = University(id, name, income, students)
            updated = self.mongo.update_university(university)
            if updated:
                messagebox.showinfo("Éxito", "Universidad actualizada correctamente.")
                self.load_universities()
            else:
                messagebox.showerror("Error", f"No existe una universidad con id {id}.")
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

        btn_update = tk.Button(root, text="Actualizar Universidad", width=25, command=self.open_update)
        btn_update.pack(pady=10)

        btn_calc = tk.Button(root, text="Calcular Ingreso por Estudiante", width=25, command=self.open_calc)
        btn_calc.pack(pady=10)

    def open_update(self):
        UpdateWindow(self.root, self.mongo)

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
