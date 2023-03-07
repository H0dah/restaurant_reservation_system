from rest_framework import viewsets
from .models import Table
from rest_framework import permissions
from .serializers import TableSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .utils import get_available_times, get_first_available_table


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
        table = get_first_available_table(required_seats)
        if not table:
            return Response({"error": "There's no table with required seats"}, status=status.HTTP_204_NO_CONTENT)

        available_times = get_available_times(table)
        if not available_times:
            return Response({"error": "There's no available times today"}, status=status.HTTP_204_NO_CONTENT)

        return Response(available_times, status=status.HTTP_200_OK)
