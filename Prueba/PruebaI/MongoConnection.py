from pymongo import MongoClient
from University import University  # Importa tu clase University correctamente

class MongoConnection:  # Usa mayúscula correctamente
    def __init__(self):
        user = "isaac"
        password = "isaac"  # Cambia aquí tu contraseña si corresponde
        cluster = "cluster0.xaitfht"
        uri = f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri)
        self.db = self.client["University"]  # Nombre exacto de tu base

    def get_universities(self):
        collection = self.db["university"]  # Nombre exacto de tu colección
        documents = collection.find()
        universities = []
        for doc in documents:
            u = University(
                doc.get("Id"),
                doc.get("name"),
                doc.get("monthlyIncome"),
                doc.get("numberOfStudent")
            )
            universities.append(u)
        return universities

    def close(self):
        self.client.close()
