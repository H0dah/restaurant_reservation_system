from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Table(models.Model):
    number = models.IntegerField(unique=True)
    number_of_seats = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)])
    def __str__(self):
        return "%s" % (self.number)

class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    client = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return "%s --> %s" % (self.start, self.end)
