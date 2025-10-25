from django.urls import path
from .views import *

urlpatterns = [
    path("", SymptomDashboardView.as_view(), name="symptom-dashboard"),
    path("list/", SymptomListView.as_view(), name="symptom-list"),
    path("add/", SymptomCreateView.as_view(), name="symptom-add"),
    path("<int:pk>/edit/", SymptomUpdateView.as_view(), name="symptom-edit"),
]