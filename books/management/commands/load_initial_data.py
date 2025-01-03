from django.core.management.base import BaseCommand
from db import db
import json


class Command(BaseCommand):
    help = "Carga datos de prueba iniciales en la base de datos MongoDB"

    def handle(self, *args, **kwargs):
        books = [
            {
                "title": "Cien Años de Soledad",
                "author": "Gabriel García Márquez",
                "publication_date": "1967-05-30",
                "genre": "Realismo Mágico",
                "price": 19.99,
            },
            {
                "title": "Don Quijote de la Mancha",
                "author": "Miguel de Cervantes",
                "publication_date": "1605-01-16",
                "genre": "Novela",
                "price": 14.99,
            },
            {
                "title": "La Sombra del Viento",
                "author": "Carlos Ruiz Zafón",
                "publication_date": "2001-04-10",
                "genre": "Misterio",
                "price": 12.99,
            },
            {
                "title": "El Principito",
                "author": "Antoine de Saint-Exupéry",
                "publication_date": "1943-04-06",
                "genre": "Fábula",
                "price": 9.99,
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "publication_date": "1949-06-08",
                "genre": "Distopía",
                "price": 15.99,
            },
        ]

        # Insertar libros si la colección está vacía
        if db.books.count_documents({}) == 0:
            db.books.insert_many(books)
            self.stdout.write(
                self.style.SUCCESS("Datos de prueba insertados correctamente.")
            )
        else:
            self.stdout.write(self.style.WARNING("La colección ya contiene datos."))
