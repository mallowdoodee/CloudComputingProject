from django.urls import path
from .views import *

urlpatterns = [
    path("", MedDashboardView.as_view(), name="med-dashboard"),

    # Drug
    path("drug/add/", DrugCreateView.as_view(), name="drug-add"),
    path("drug/<int:pk>/edit/", DrugUpdateView.as_view(), name="drug-edit"),

    # Intake
    path("intake/add/", IntakeCreateView.as_view(), name="intake-add"),
    path("intake/<int:pk>/edit/", IntakeUpdateView.as_view(), name="intake-edit"),
]