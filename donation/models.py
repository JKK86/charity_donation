from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

FUNDACJA = 1
ORG_POZA = 2
ZB_LOK = 3

INSTITUTION_TYPES = (
    (FUNDACJA, "Fundacja"),
    (ORG_POZA, "Organizacja pozarządowa"),
    (ZB_LOK, "Zbiórka lokalna"),
)


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nazwa")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ('name',)


class Institution(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nazwa")
    description = models.TextField(verbose_name="Opis")
    type = models.IntegerField(choices=INSTITUTION_TYPES, default=FUNDACJA, verbose_name="Typ")
    categories = models.ManyToManyField(Category, verbose_name="Kategorie", related_name="institutions")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instytucja"
        verbose_name_plural = "Instytucje"
        ordering = ('name',)


class Donation(models.Model):
    quantity = models.PositiveIntegerField(verbose_name="Liczba worków", default=1,
                                           validators=[MinValueValidator(1), MaxValueValidator(20)])
    categories = models.ManyToManyField(Category, verbose_name="Kategorie", related_name='donations')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Instytucja",
                                    related_name='donations')
    address = models.CharField(max_length=32, verbose_name="Adres")
    phone_number = models.CharField(max_length=16, verbose_name="Numer telefonu")
    city = models.CharField(max_length=32, verbose_name="Miasto")
    zip_code = models.CharField(max_length=6, verbose_name="Kod pocztowy")
    pick_up_date = models.DateField(verbose_name="Data odbioru")
    pick_up_time = models.TimeField(verbose_name="Godzina odbioru")
    pick_up_comment = models.TextField(verbose_name="Komentarz", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=True,
                             verbose_name="Użytkownik")
    is_taken = models.BooleanField(verbose_name="Stan", default=False)

    def __str__(self):
        return f'Worki: {self.quantity} dla {self.institution}'

    class Meta:
        verbose_name = "darowizna"
        verbose_name_plural = "Darowizny"
