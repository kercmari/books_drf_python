from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bson import ObjectId
from .serializers import BookSerializer
from db import db
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, time, date
from json import JSONEncoder
from helpers.utils import serializar_documento_mongo

from bson.errors import InvalidId


class WelcomeView(APIView):
    """
    Vista que da la bienvenida a la API de Gestión de Libros.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Mensaje de bienvenida a la API. No requiere autenticación.",
        responses={200: openapi.Response("¡Bienvenido a la API de Gestión de Libros!")},
    )
    def get(self, request):
        return Response({"message": "¡Bienvenido a la API de Gestión de Libros!"})


class BookListCreateView(APIView):
    """
    Endpoints para gestionar la lista de libros.
    - GET: Obtener la lista paginada de libros.
    - POST: Crear un nuevo libro.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        operation_description="Obtiene una lista paginada de libros. Requiere autenticación con JWT.",
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Número de página (por defecto: 1)",
                type=openapi.TYPE_INTEGER,
                default=1,
            )
        ],
        responses={
            200: openapi.Response(
                description="Lista de libros",
                examples={
                    "application/json": {
                        "count": 2,
                        "next": "http://api/books/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": "63d9f38e6d8b1a1e9ef45a1b",
                                "title": "Libro de ejemplo",
                                "author": "Autor Ejemplo",
                                "price": 15.99,
                                "publication_date": "2023-01-01",
                            },
                        ],
                    }
                },
            ),
        },
    )
    def get(self, request):
        # Obtener página actual, por defecto 1
        page = request.query_params.get("page", 1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        books = list(db.books.find())
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(books, request)
        print("Página actual:", result_page)
        serializer = BookSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Título del libro"
                ),
                "author": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Autor del libro"
                ),
                "genre": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Género del libro"
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Precio del libro"
                ),
                "publication_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Fecha de publicación (YYYY-MM-DD)",
                ),
            },
            required=["title", "author", "price"],  # Campos obligatorios
        ),
        responses={201: "Libro creado exitosamente", 400: "Datos inválidos"},
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Crear una copia de los datos validados
            libro = serializer.validated_data.copy()

            # Procesar la fecha de publicación
            fecha_publicacion = libro.get("publication_date")

            # Validar formato de fecha si es string
            if isinstance(fecha_publicacion, str):
                try:
                    fecha_publicacion = datetime.strptime(fecha_publicacion, "%Y-%m-%d")
                except ValueError:
                    return Response(
                        {
                            "publication_date": "Formato de fecha inválido. Use AAAA-MM-DD."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif isinstance(fecha_publicacion, date) and not isinstance(
                fecha_publicacion, datetime
            ):
                fecha_publicacion = datetime.combine(fecha_publicacion, time())

            elif isinstance(fecha_publicacion, datetime):
                pass

            else:
                return Response(
                    {"publication_date": "Tipo de dato no válido para la fecha."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            libro["publication_date"] = fecha_publicacion

            resultado = db.books.insert_one(libro)

            datos_respuesta = libro.copy()
            datos_respuesta["_id"] = resultado.inserted_id

            datos_serializados = serializar_documento_mongo(datos_respuesta)

            # Depuración

            return Response(datos_serializados, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    def get_object(self, id):
        """
        Obtiene un libro por su ID de MongoDB
        """
        try:

            object_id = ObjectId(id)

            return db.books.find_one({"_id": object_id})
        except InvalidId:
            return None

    """
    Endpoints para obtener, actualizar y eliminar un libro específico.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        operation_description="Obtiene los detalles de un libro por su ID.",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID del libro",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            200: openapi.Response(
                description="Detalles del libro",
                examples={
                    "application/json": {
                        "id": "63d9f38e6d8b1a1e9ef45a1b",
                        "title": "Libro de ejemplo",
                        "author": "Autor Ejemplo",
                        "price": 15.99,
                        "publication_date": "2023-01-01",
                    }
                },
            ),
            404: "Libro no encontrado",
        },
    )
    def get(self, request, id):
        book = self.get_object(id)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        operation_description="Actualiza los detalles de un libro por su ID.",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID del libro a actualizar",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title", "author", "price", "publication_date"],
            properties={
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Título del libro"
                ),
                "author": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Autor del libro"
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Precio del libro"
                ),
                "publication_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Fecha de publicación (YYYY-MM-DD)",
                ),
                "genre": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Género del libro (opcional)"
                ),
            },
            example={
                "title": "Nuevo título",
                "author": "Nuevo autor",
                "price": 20.0,
                "publication_date": "2023-05-15",
                "genre": "Ficción",
            },
        ),
        responses={
            200: openapi.Response(
                description="Libro actualizado exitosamente",
                examples={
                    "application/json": {
                        "title": "Nuevo título",
                        "author": "Nuevo autor",
                        "price": 20.0,
                        "publication_date": "2023-05-15",
                        "genre": "Ficción",
                    }
                },
            ),
            400: "Datos inválidos",
            404: "Libro no encontrado",
        },
    )
    def put(self, request, id):
        book = self.get_object(id)
        if book:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                db.books.update_one(
                    {"_id": ObjectId(id)}, {"$set": serializer.validated_data}
                )
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        operation_description="Elimina un libro por su ID.",
        responses={
            204: "Libro eliminado exitosamente",
            404: "Libro no encontrado",
        },
    )
    def delete(self, request, id):
        try:
            book = self.get_object(id)
            if book:
                result = db.books.delete_one({"_id": ObjectId(id)})
                if result.deleted_count > 0:
                    return Response(
                        {"message": "Libro eliminado exitosamente", "id": id},
                        status=status.HTTP_200_OK,
                    )
            return Response(
                {"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except InvalidId:
            return Response(
                {"error": "ID de libro inválido"}, status=status.HTTP_400_BAD_REQUEST
            )


class AveragePriceView(APIView):
    """
    Calcula el precio promedio de los libros publicados en un año específico.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year",
                openapi.IN_PATH,
                description="Año para calcular el precio promedio (YYYY)",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Precio promedio encontrado",
                examples={"application/json": {"year": "2025", "average_price": 20.0}},
            ),
            404: openapi.Response(
                description="No se encontraron libros",
                examples={
                    "application/json": {
                        "error": "No se encontraron libros para el año especificado"
                    }
                },
            ),
        },
    )
    def get(self, request, year):
        try:
            # Crear fechas de inicio y fin del año
            start_date = datetime(int(year), 1, 1)
            end_date = datetime(int(year), 12, 31, 23, 59, 59)

            pipeline = [
                {
                    "$match": {
                        "publication_date": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {"$group": {"_id": None, "average_price": {"$avg": "$price"}}},
            ]

            result = list(db.books.aggregate(pipeline))

            if result:
                return Response(
                    {"year": year, "average_price": result[0]["average_price"]},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "No se encontraron libros para el año especificado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError:
            return Response(
                {"error": "Formato de año inválido"}, status=status.HTTP_400_BAD_REQUEST
            )
