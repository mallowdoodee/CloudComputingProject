from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
# List
from django.core.paginator import Paginator
from django.db.models import F
from medications.models import MedicationIntake

class SymptomListView(LoginRequiredMixin, View):
    def get(self, request):
        from django.db.models import F
        from django.utils import timezone

        # ========== อาการทั้งหมด ==========
        qs = (
            Symptom.objects
            .filter(user=request.user)
            .order_by(F('date').desc(nulls_last=True), F('time').desc(nulls_last=True), '-pk')
        )
        paginator = Paginator(qs, 4)
        page_obj = paginator.get_page(request.GET.get('page'))

        # ========== แผนการทานยาทั้งหมด ==========
        medications_all = (
            MedicationIntake.objects
            .filter(user=request.user)
            .select_related("drug")
            .order_by("-active", "-start_date", "time")
        )

        return render(request, "sym_list.html", {
            "symptoms": page_obj.object_list,
            "page_obj": page_obj,
            "medications_all": medications_all,
            "today": timezone.localdate(),
        })

# ============ DASHBOARD ============ #
class SymptomDashboardView(LoginRequiredMixin, View):
    """หน้าเดียว แสดงรายการอาการ + ปุ่มไปหน้าเพิ่ม เฉพาะวันนี้"""
    def get(self, request):
        # today = timezone.localdate()  # ชัวร์เรื่องโซนเวลา
        symptoms = (Symptom.objects
                    .filter(user=request.user)
                    .order_by(F('date').desc(nulls_last=True), '-pk'))
        return render(request, "sym_dashboard.html", {"symptoms": symptoms, "today": timezone.localdate()})

# ============ CREATE ============ #
class SymptomCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = SymptomForm()
        return render(request, "symptom_form.html", {"form": form, "title": "เพิ่มอาการ"})

    def post(self, request):
        form = SymptomForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            # หากไม่กรอกเวลา time จะเป็น None ตามโมเดล (blank=True, null=True)
            s.save()
            return redirect("symptom-dashboard")
        return render(request, "symptom_form.html", {"form": form, "title": "เพิ่มอาการ"})

# ============ UPDATE / DELETE (ลบในหน้าเดียว) ============ #
class SymptomUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        symptom = get_object_or_404(Symptom, pk=pk, user=request.user)
        form = SymptomForm(instance=symptom)
        return render(request, "symptom_form.html",
                      {"form": form, "symptom": symptom, "title": f"แก้ไขอาการ: {symptom.name}"})

    def post(self, request, pk):
        symptom = get_object_or_404(Symptom, pk=pk, user=request.user)

        # ลบในหน้าเดียวกัน
        if "delete" in request.POST:
            symptom.delete()
            return redirect("symptom-dashboard")

        form = SymptomForm(request.POST, instance=symptom)
        if form.is_valid():
            form.save()
            return redirect("symptom-dashboard")

        return render(request, "symptom_form.html",
                      {"form": form, "symptom": symptom, "title": f"แก้ไขอาการ: {symptom.name}"})