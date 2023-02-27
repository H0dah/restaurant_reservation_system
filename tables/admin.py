from django.contrib import admin
from .models import Table, Booking

@admin.register(Table)
class TablesAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass