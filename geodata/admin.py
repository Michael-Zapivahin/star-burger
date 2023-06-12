from django.contrib import admin

from geodata.models import Place

# Register your models here.
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = [
        'place',
        'lat',
        'lon',
    ]
