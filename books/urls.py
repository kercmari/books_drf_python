from django.urls import path
from .views import BookListCreateView, BookDetailView, AveragePriceView, WelcomeView
from django.contrib import admin


urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<str:id>/", BookDetailView.as_view(), name="book-detail"),
    path(
        "books/average-price/<str:year>/",
        AveragePriceView.as_view(),
        name="average-price",
    ),
]
