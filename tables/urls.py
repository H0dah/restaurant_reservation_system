from .views import TableViewSet, GetAvailableTimes
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'', TableViewSet, basename='table')
urlpatterns = router.urls

urlpatterns = [
    path('get_available_times',GetAvailableTimes.as_view(), name="available_times" )
]