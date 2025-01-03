from django.db import models
from dataclasses import dataclass
from bson import ObjectId
from datetime import datetime

# Create your models here.


@dataclass
class Book:
    id: ObjectId
    title: str
    author: str
    publication_date: datetime
    genre: str
    price: float
