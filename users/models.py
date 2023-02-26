from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    employee_number = models.IntegerField(unique=True, validators=[
        MaxValueValidator(9999), MinValueValidator(1000)
    ])

    # Admin or Employee (user role)
    def is_admin(self):
        return self.user.is_staff
