# appointments/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Appointment
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/edit/', AppointmentEditView.as_view(), name='appointment-edit'),
    path('<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path("calendar/<int:year>/<int:month>/", AppointmentCalendarView.as_view(), name="appointment-calendar"),
    path("calendar/", AppointmentCalendarView.as_view(), name="appointment-calendar"),
]