from django.db import models
from django.utils import timezone


class Categorie(models.Model):
    nume = models.CharField(
        max_length=60, unique=True,
        error_messages={"unique": "Există deja o categorie cu acest nume."},
    )
    descriere = models.TextField(null=True, blank=True)
    culoare = models.CharField(
        max_length=7, default="#E6EBD9",
        help_text="Culoare în format hexazecimal, de exemplu #E6EBD9.",
        error_messages={"max_length": "Culoarea poate avea cel mult 7 caractere."},
    )
    sigla = models.CharField(
        max_length=200, null=True, blank=True,
        help_text="Calea unei imagini din static sau numele unei pictograme.",
    )
    ordine_afisare = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = "categorie"
        verbose_name_plural = "categorii"
        ordering = ["ordine_afisare", "nume"]
        constraints = [
            models.CheckConstraint(check=models.Q(ordine_afisare__gte=0), name="categorie_ordine_pozitiva"),
            models.CheckConstraint(check=models.Q(culoare__regex=r"^#[0-9A-Fa-f]{6}$"), name="categorie_culoare_hex"),
        ]

    def __str__(self):
        return self.nume


class Furnizor(models.Model):
    nume = models.CharField(
        max_length=100, unique=True,
        error_messages={"unique": "Există deja un furnizor cu acest nume."},
    )
    telefon = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(
        null=True, blank=True,
        error_messages={"invalid": "Introdu o adresă de email validă pentru furnizor."},
    )

    class Meta:
        verbose_name = "furnizor"
        verbose_name_plural = "furnizori"
        ordering = ["nume"]

    def __str__(self):
        return self.nume


class Ingredient(models.Model):
    furnizor = models.ForeignKey(Furnizor, on_delete=models.PROTECT, related_name="ingrediente")
    nume = models.CharField(
        max_length=80, unique=True,
        error_messages={"unique": "Există deja un ingredient cu acest nume."},
    )
    alergen = models.BooleanField(default=False)
    denumiri_alternative = models.JSONField(
        default=list, blank=True,
        help_text='Listă de denumiri în format JSON, de exemplu ["lapte de vacă", "lapte integral"]. Pentru nicio denumire, folosește [].',
    )

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingrediente"
        ordering = ["nume"]

    def __str__(self):
        return self.nume


class Sediu(models.Model):
    nume = models.CharField(max_length=80)
    adresa = models.CharField(max_length=250)
    telefon = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "sediu"
        verbose_name_plural = "sedii"
        ordering = ["nume"]

    def __str__(self):
        return f"{self.nume} - {self.adresa}"


class Preparat(models.Model):
    TIPURI = [("sarat", "Sărat"), ("dulce", "Dulce"), ("bautura", "Băutură")]

    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="preparate")
    ingrediente = models.ManyToManyField(Ingredient, related_name="preparate")
    nume = models.CharField(
        max_length=100, unique=True,
        error_messages={"unique": "Există deja un preparat cu acest nume."},
    )
    descriere = models.TextField(null=True, blank=True)
    pret = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="Prețul unei porții, în lei. Trebuie să fie mai mare decât zero.",
    )
    gramaj = models.PositiveIntegerField(help_text="Cantitatea unei porții: grame pentru mâncare, mililitri pentru băuturi.")
    calorii = models.PositiveIntegerField(help_text="Numărul de kilocalorii pentru întreaga porție.")
    vegetarian = models.BooleanField(default=False)
    disponibil = models.BooleanField(default=True)
    tip = models.CharField(max_length=10, choices=TIPURI, default="sarat")
    data_lansare = models.DateField(null=True, blank=True)
    data_adaugare = models.DateTimeField(default=timezone.now)
    imagine = models.ImageField(upload_to="preparate/", null=True, blank=True)

    class Meta:
        verbose_name = "preparat"
        verbose_name_plural = "preparate"
        ordering = ["nume"]
        indexes = [
            models.Index(fields=["pret"], name="preparat_pret_idx"),
            models.Index(fields=["gramaj"], name="preparat_gramaj_idx"),
            models.Index(fields=["calorii"], name="preparat_calorii_idx"),
            models.Index(fields=["data_lansare"], name="preparat_lansare_idx"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(pret__gt=0), name="preparat_pret_pozitiv"),
            models.CheckConstraint(check=models.Q(gramaj__gt=0), name="preparat_gramaj_pozitiv"),
            models.CheckConstraint(check=models.Q(calorii__gte=0), name="preparat_calorii_pozitive"),
            models.CheckConstraint(check=models.Q(tip__in=["sarat", "dulce", "bautura"]), name="preparat_tip_valid"),
        ]

    def __str__(self):
        return f"{self.nume} - {self.pret} lei"


class LotPreparat(models.Model):
    # Lotul apartine unui preparat; numarul lui este unic doar pentru acel preparat.
    preparat = models.ForeignKey(Preparat, on_delete=models.CASCADE, related_name="loturi")
    numar_lot = models.PositiveIntegerField(help_text="Numărul lotului în cadrul preparatului ales.")
    sediu = models.ForeignKey(Sediu, on_delete=models.PROTECT, related_name="loturi")
    data_preparare = models.DateTimeField(default=timezone.now)
    data_expirare = models.DateTimeField(help_text="Trebuie să fie după data și ora preparării.")
    cantitate = models.PositiveIntegerField(help_text="Numărul de porții pregătite în acest lot.")

    class Meta:
        verbose_name = "lot de preparat"
        verbose_name_plural = "loturi de preparate"
        ordering = ["-data_preparare"]
        constraints = [
            # Django adauga un ID tehnic; perechea de mai jos identifica lotul din diagrama.
            models.UniqueConstraint(fields=["preparat", "numar_lot"], name="lot_preparat_numar_unic"),
            models.CheckConstraint(check=models.Q(numar_lot__gt=0), name="lot_numar_pozitiv"),
            models.CheckConstraint(check=models.Q(cantitate__gt=0), name="lot_cantitate_pozitiva"),
            models.CheckConstraint(check=models.Q(data_expirare__gt=models.F("data_preparare")), name="lot_expirare_dupa_preparare"),
        ]

    def __str__(self):
        return f"Lot {self.numar_lot} - {self.preparat.nume}"
