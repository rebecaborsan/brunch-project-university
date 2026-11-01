from django.urls import path, re_path
from . import views

app_name = "brunch"
urlpatterns = [
    path("", views.index, name="index"),
    path("info", views.info, name="info"),
    path("log", views.log, name="log"),
    path("despre", views.despre, name="despre"),
    path("istoric", views.istoric, name="istoric"),
    path("produse", views.in_lucru, name="produse"),
    path("contact", views.in_lucru, name="contact"),
    path("cos_virtual", views.in_lucru, name="cos_virtual"),
    path("meniu_sezon", views.in_lucru, name="meniu_sezon"),
    path("evenimente", views.in_lucru, name="evenimente"),
    re_path(r"^accesare(?P<id>[0-9]+)$", views.detaliu_accesare, name="accesare"),
]
