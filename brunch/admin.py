from django.contrib import admin
from .models import Categorie, Furnizor, Ingredient, Sediu, Preparat, LotPreparat


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nume", "culoare", "ordine_afisare")


@admin.register(Furnizor)
class FurnizorAdmin(admin.ModelAdmin):
    list_display = ("nume", "telefon", "email")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("nume", "furnizor", "alergen")


@admin.register(Sediu)
class SediuAdmin(admin.ModelAdmin):
    list_display = ("nume", "adresa", "telefon")


@admin.register(Preparat)
class PreparatAdmin(admin.ModelAdmin):
    list_display = ("nume", "categorie", "pret", "gramaj", "tip", "disponibil")
    filter_horizontal = ("ingrediente",)


@admin.register(LotPreparat)
class LotPreparatAdmin(admin.ModelAdmin):
    list_display = ("numar_lot", "preparat", "sediu", "data_preparare", "data_expirare", "cantitate")
