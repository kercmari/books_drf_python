from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView

# Configuración del esquema de seguridad Bearer Token
schema_view = get_schema_view(
    openapi.Info(
        title="API de Gestión de Libros",
        default_version="v1",
        description="API para gestionar libros y usuarios",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Rutas principales
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("books.urls")),
    path("api/users/", include("users.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "",
        RedirectView.as_view(url="/swagger/", permanent=False),
        name="swagger-redirect",
    ),
]
