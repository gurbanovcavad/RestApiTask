"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from api.routers.oil_fields import oil_fields
from api.routers.wells import wells
from api.routers.sensors import sensors
from api.routers.production_readings import production_readings

api = NinjaAPI(title="Oilfield Operations API", version="0.1.0")

api.add_router("/oil-fields", oil_fields)
api.add_router("/wells", wells)
api.add_router("/sensors", sensors)
api.add_router("/production-readings", production_readings)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]