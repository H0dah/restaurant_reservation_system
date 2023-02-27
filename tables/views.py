from rest_framework import viewsets
from .models import Table
from rest_framework import permissions
from .serializers import TableSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import datetime
from django.db.models import Q


class TableViewSet(viewsets.ModelViewSet):

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "number"

    def destroy(self, request, *args, **kwargs):

        table = self.get_object()
        if table.booking_set.all().exists():
            data = {"error": "Table has reservations, So can't delete it"}
            return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        table.delete()
        data = "Table deleted!"
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class GetAvailableTimes(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        required_seats = request.data["required_seats"]
        table = Table.objects.filter(number_of_seats__gte=required_seats).order_by(
            "number_of_seats").first()


        end_of_today = datetime.datetime.combine(
            datetime.datetime.today(), datetime.time(23, 59, 59, 999999))
        bookings = table.booking_set.filter(Q(
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
                available_times.append({
                    str(time_pointer): book_start_time})
            time_pointer = book_end_time

        available_times.append({str(time_pointer): end_of_today})

        return Response(available_times, status=status.HTTP_200_OK)
