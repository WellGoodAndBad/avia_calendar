from django.db import models


class PriceOfTicket(models.Model):
    id_in_api = models.TextField()
    date = models.DateField()
    city_from = models.TextField()
    city_to = models.TextField()
    price = models.FloatField()
    booking_token = models.TextField()
    flights_checked = models.NullBooleanField()
    flights_invalid = models.NullBooleanField()
    price_change = models.NullBooleanField()