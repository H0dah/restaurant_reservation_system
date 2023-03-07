from pytz import timezone as pytz_timezone
import datetime
from django.db.models import Q
from .models import Table
from django.utils import timezone
from django.utils.timezone import localtime


def get_first_available_table(required_seats):
    table = Table.objects.filter(number_of_seats__gte=required_seats).order_by(
        "number_of_seats").first()
    return table


def get_available_times(table):

    cairo_time = pytz_timezone('Africa/Cairo')

    end_of_today = cairo_time.localize(datetime.datetime.combine(
        datetime.datetime.today(), datetime.time(23, 59, 59, 999999)))

    bookings = table.booking_set.filter(Q(
        start__gte=timezone.now(),
        start__lte=end_of_today) | Q(
        end__gt=timezone.now())
    ).order_by('start').all()

    available_times = []

    time_pointer = localtime(timezone.now())

    # when request available times outside of working hours(before 12 o'clock)
    if time_pointer.time() < datetime.time(12, 00, 00, 0000):
        time_pointer = cairo_time.localize(datetime.datetime.combine(
            datetime.datetime.today(), datetime.time(12, 00, 00, 0000)))

    for book in bookings:
        book_start_time = book.start
        book_end_time = book.end
        if book_start_time > time_pointer:
            available_times.append({
                "start": time_pointer, "end": localtime(book_start_time)})
        time_pointer = localtime(book_end_time)

    available_times.append({"start": time_pointer, "end": end_of_today})

    if len(available_times) == 1 and \
            available_times[0]["start"].time() == datetime.time(00, 00, 00) and \
            available_times[0]["end"].time() == datetime.time(23, 59, 59, 999999):
        return []

    return (available_times)
