
from geodata.models import Place


def create_place(place_content):
    place, created = Place.objects.update_or_create(
        lat=place_content['lat'],
        lon=place_content['lon'],
        place=place_content['place'],
    )
    return place



