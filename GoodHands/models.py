from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    FUNDACJA = 'Fundacja'
    ORGANIZACJA_POZARZADOWA = 'Organizacja pozarządowa'
    ZBIORKA_LOKALNA = 'Zbiórka lokalna'
    CHOICES = (
        (FUNDACJA, 'Fundacja'),
        (ORGANIZACJA_POZARZADOWA, 'Organizacja pozarządowa'),
        (ZBIORKA_LOKALNA, 'Zbiórka lokalna'),
    )
    type = models.CharField(max_length=50, choices=CHOICES, default=FUNDACJA)
    categories = models.ManyToManyField('Category')

    class Meta:
        verbose_name_plural = "instytucje"

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=60)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
