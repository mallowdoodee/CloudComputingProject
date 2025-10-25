from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Drug, MedicationIntake
from .forms import DrugForm, MedicationIntakeForm


# ============ DASHBOARD ============
class MedDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        # แสดงเฉพาะยาของผู้ใช้ที่ล็อกอิน
        drugs = Drug.objects.filter(user=request.user).order_by("name")
        # แสดงเฉพาะแผนกินยาของผู้ใช้ที่ล็อกอิน
        intakes = MedicationIntake.objects.filter(user=request.user).order_by("-start_date")

        palette = [
            "bg-rose-100 text-rose-800",
            "bg-amber-100 text-amber-800",
            "bg-emerald-100 text-emerald-800",
            "bg-sky-100 text-sky-800",
            "bg-purple-100 text-purple-800",
        ]

        drugs_with_color = [(d, palette[i % len(palette)]) for i, d in enumerate(drugs)]

        return render(request, "dashboard.html", {
            "drugs_with_color": drugs_with_color,
            "intakes": intakes,
        })


# ============ DRUG ============
class DrugCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = DrugForm()
        return render(request, "drug_form.html", {"form": form, "title": "เพิ่มยาใหม่"})

    def post(self, request):
        form = DrugForm(request.POST)
        if form.is_valid():
            drug = form.save(commit=False)
            drug.user = request.user  # ผูกกับผู้ใช้ปัจจุบัน
            drug.save()
            return redirect("med-dashboard")
        return render(request, "drug_form.html", {"form": form, "title": "เพิ่มยาใหม่"})


class DrugUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # ป้องกันไม่ให้เห็นของคนอื่น
        drug = get_object_or_404(Drug, pk=pk, user=request.user)
        form = DrugForm(instance=drug)
        return render(request, "drug_form.html", {"form": form, "drug": drug, "title": f"แก้ไขยา: {drug.name}"})

    def post(self, request, pk):
        drug = get_object_or_404(Drug, pk=pk, user=request.user)

        if "delete" in request.POST:
            drug.delete()
            return redirect("med-dashboard")

        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            form.save()
            return redirect("med-dashboard")

        return render(request, "drug_form.html", {"form": form, "drug": drug, "title": f"แก้ไขยา: {drug.name}"})


# ============ MEDICATION INTAKE ============
from django.contrib import messages

class IntakeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        # ✅ ตรวจว่าผู้ใช้มียาหรือยัง
        user_drugs = Drug.objects.filter(user=request.user)
        if not user_drugs.exists():
            messages.warning(request, "⚠️ คุณยังไม่มียาในระบบ กรุณาเพิ่มยาก่อนสร้างแผนการกินยา")
            return redirect("med-dashboard")  # 👈 ไปหน้าเพิ่มยา (เปลี่ยนชื่อ url name ให้ตรงของคุณ)

        # ✅ ถ้ามียาแล้ว แสดงฟอร์ม
        form = MedicationIntakeForm(user=request.user)
        return render(request, "intake_form.html", {"form": form, "title": "เพิ่มแผนการกินยา"})

    def post(self, request):
        # ✅ ตรวจอีกครั้งกรณีโพสต์ (กัน user พิมพ์ URL ตรง)
        user_drugs = Drug.objects.filter(user=request.user)
        if not user_drugs.exists():
            messages.warning(request, "⚠️ คุณยังไม่มียาในระบบ กรุณาเพิ่มยาก่อนสร้างแผนการกินยา")
            return redirect("drug-add")

        form = MedicationIntakeForm(request.POST, user=request.user)
        if form.is_valid():
            intake = form.save(commit=False)
            intake.user = request.user
            intake.save()
            messages.success(request, "✅ เพิ่มแผนการกินยาเรียบร้อยแล้ว")
            return redirect("med-dashboard")

        return render(request, "intake_form.html", {"form": form, "title": "เพิ่มแผนการกินยา"})

class IntakeUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        intake = get_object_or_404(MedicationIntake, pk=pk, user=request.user)
        form = MedicationIntakeForm(instance=intake, user=request.user)
        return render(request, "intake_form.html", {"form": form, "intake": intake, "title": f"แก้ไขแผน: {intake.drug.name}"})

    def post(self, request, pk):
        intake = get_object_or_404(MedicationIntake, pk=pk, user=request.user)

        if "delete" in request.POST:
            intake.delete()
            return redirect("med-dashboard")

        form = MedicationIntakeForm(request.POST, instance=intake, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("med-dashboard")

        return render(request, "intake_form.html", {"form": form, "intake": intake, "title": f"แก้ไขแผน: {intake.drug.name}"})
