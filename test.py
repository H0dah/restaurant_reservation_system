from tables.models import Table, Booking
import datetime
from django.db.models import Q

required_seats = 1
table = Table.objects.filter(number_of_seats__gte = required_seats).order_by("number_of_seats").first()

end_of_today = datetime.datetime.combine(datetime.datetime.today(), datetime.time(23, 59, 59, 999999))
bookings = table.booking_set.filter( Q(
    start__gte=datetime.datetime.now(),
    start__lte=end_of_today) | Q(
    end__gt=datetime.datetime.now())
).order_by('start').all()

available_times = []
time_pointer = datetime.datetime.now().time()
for book in bookings:
    book_start_time = book.start.time()
    book_end_time = book.end.time()
    if book_start_time > time_pointer:
        available_times.append(Booking(start=time_pointer, end=book_start_time))
    time_pointer = book_end_time

available_times.append(Booking(start=time_pointer, end=end_of_today))


    # if i ==0 and book_start_time > time_now:
    #     available_times.append(Booking(start=time_now, end=book_start_time))
    # elif i == 0 :
    #     available_times.append(Booking(start=book_end_time, end = bookings[1].end.time()))
    # else:
    #     if i-1 == len(bookings):
    #         if book_end_time != datetime.time(11, 59):
    #             available_times.append(Booking(start=book_end_time, end = bookings[i+1].end.time()))

    #     else:
    #         available_times.append(Booking(start=book_end_time, end = bookings[i+1].end.time()))
