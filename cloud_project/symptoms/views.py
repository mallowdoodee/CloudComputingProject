from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .forms import SymptomForm
from .models import Symptom


class SymptomListView(LoginRequiredMixin, View):
    def get(self, request):
        symptoms = (
            Symptom.objects.filter(user=request.user)
            .order_by(F("time").desc(nulls_last=True), "-pk")
        )
        paginator = Paginator(symptoms, 4)
        page_obj = paginator.get_page(request.GET.get("page"))
        return render(
            request,
            "sym_list.html",
            {
                "symptoms": page_obj.object_list,
                "page_obj": page_obj,
            },
        )


class SymptomDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        today = timezone.localdate()
        symptoms = (
            Symptom.objects.filter(user=request.user, created_at__date=today)
            .order_by(F("time").desc(nulls_last=True), "-pk")
        )
        return render(request, "sym_dashboard.html", {"symptoms": symptoms})


class SymptomCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = SymptomForm()
        return render(
            request,
            "symptom_form.html",
            {"form": form, "title": "Add New Symptom"},
        )

    def post(self, request):
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom = form.save(commit=False)
            symptom.user = request.user
            symptom.save()
            return redirect("symptom-dashboard")
        return render(
            request,
            "symptom_form.html",
            {"form": form, "title": "Add New Symptom"},
        )


class SymptomUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        symptom = get_object_or_404(Symptom, pk=pk, user=request.user)
        form = SymptomForm(instance=symptom)
        return render(
            request,
            "symptom_form.html",
            {"form": form, "symptom": symptom, "title": "Edit Symptom"},
        )

    def post(self, request, pk):
        symptom = get_object_or_404(Symptom, pk=pk, user=request.user)

        if "delete" in request.POST:
            symptom.delete()
            return redirect("symptom-dashboard")

        form = SymptomForm(request.POST, instance=symptom)
        if form.is_valid():
            form.save()
            return redirect("symptom-dashboard")

        return render(
            request,
            "symptom_form.html",
            {"form": form, "symptom": symptom, "title": "Edit Symptom"},
        )
