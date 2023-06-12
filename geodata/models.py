from django.db import models

from django.db import models


class Place(models.Model):
    place = models.CharField(
        verbose_name='Наименование локации',
        unique=True,
        max_length=150
    )

    lat = models.FloatField(verbose_name='широта', blank=True, null=True)

    lon = models.FloatField(verbose_name='долгота', blank=True, null=True)
