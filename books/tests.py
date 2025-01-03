from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from db import db
import json


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Obtener token JWT
        response = self.client.post(
            "/api/users/token/",
            {"username": "testuser", "password": "testpass"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_book(self):
        data = {
            "title": "Test Book",
            "author": "Author Test",
            "publication_date": "2023-01-01",
            "genre": "Test Genre",
            "price": 20.0,
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Test Book")
        print("respuesta del test", response.data)
        # Limpiar
        if "_id" in response.data:
            db.books.delete_one({"_id": response.data["_id"]})

    def test_average_price(self):

        books = [
            {
                "title": "Book1",
                "author": "Author1",
                "publication_date": "2023-05-10",
                "genre": "Genre1",
                "price": 10.0,
            },
            {
                "title": "Book2",
                "author": "Author2",
                "publication_date": "2023-06-15",
                "genre": "Genre2",
                "price": 20.0,
            },
        ]
        result = db.books.insert_many(books)
        response = self.client.get("/api/books/average-price/2023/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["average_price"], 20.0)
        # Limpiar
        db.books.delete_many({"_id": {"$in": result.inserted_ids}})
