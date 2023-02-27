
from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'number_of_seats')
        lookup_field = "number"
