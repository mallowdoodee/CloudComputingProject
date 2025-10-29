# views.py
import calendar
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.urls import reverse
from django.utils.timezone import localdate
from django.db.models import Q 

# ===== IMPORT MODEL ข้าม APP =====
from .models import Appointment, Profile
from symptoms.models import Symptom
from medications.models import MedicationIntake

# ===== FORM =====
from .forms import AppointmentForm
class AppointmentListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        from django.db.models import Q

        profile, _ = Profile.objects.get_or_create(user=request.user)
        today = localdate()

        # ========== นัดหมายวันนี้ ==========
        appointments_today = (
            Appointment.objects
            .filter(patient=profile, date=today)
            .select_related("clinic", "patient")
            .order_by("at_time")
        )

        # ========== อาการที่บันทึก "วันนี้" ==========
        # ✅ แก้ตรงนี้: ใช้ date แทน created_at__date
        symptom_logs = (
            Symptom.objects
            .filter(user=request.user, date=today)
            .order_by("-created_at")
        )

        # ========== แผนการกินยาที่ต้องกิน "วันนี้" ==========
        medications_upcoming = (
            MedicationIntake.objects
            .filter(
                user=request.user,
                active=True,
                start_date__lte=today
            )
            .filter(Q(end_date__gte=today) | Q(end_date__isnull=True))
            .select_related("drug")
            .order_by("time")
        )

        return render(request, "today_dashboard.html", {
            "appointments_today": appointments_today,
            "symptom_logs": symptom_logs,
            "medications_upcoming": medications_upcoming,
        })


# ================================
# CREATE
# ================================
class AppointmentCreateView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        form = AppointmentForm(initial={"patient": profile})
        return render(request, "appointment_form.html", {
            "form": form,
            "title": "เพิ่มนัดหมาย"
        })

    def post(self, request: HttpRequest):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = profile
            appt.save()
            return redirect("appointment-calendar")
        return render(request, "appointment_form.html", {
            "form": form,
            "title": "เพิ่มนัดหมาย"
        })


# ================================
# EDIT
# ================================
class AppointmentEditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk):
        appt = get_object_or_404(Appointment.objects.select_related("patient", "clinic"), pk=pk)
        if not (request.user.is_staff or getattr(request.user, "profile", None) == appt.patient):
            raise PermissionDenied("แก้ไขได้เฉพาะเจ้าของนัดหมายหรือเจ้าหน้าที่เท่านั้น")
        form = AppointmentForm(instance=appt)
        return render(request, "appointment_form.html", {
            "form": form,
            "title": "แก้ไขนัดหมาย"
        })

    def post(self, request: HttpRequest, pk):
        appt = get_object_or_404(Appointment.objects.select_related("patient", "clinic"), pk=pk)
        if not (request.user.is_staff or getattr(request.user, "profile", None) == appt.patient):
            raise PermissionDenied("แก้ไขได้เฉพาะเจ้าของนัดหมายหรือเจ้าหน้าที่เท่านั้น")
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = appt.patient
            obj.save()
            return redirect("appointment-calendar")
        return render(request, "appointment_form.html", {
            "form": form,
            "title": "แก้ไขนัดหมาย"
        })


# ================================
# DELETE
# ================================
class AppointmentDeleteView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk):
        appt = get_object_or_404(Appointment.objects.select_related("patient"), pk=pk)
        if not (request.user.is_staff or getattr(request.user, "profile", None) == appt.patient):
            raise PermissionDenied("ลบได้เฉพาะเจ้าของนัดหมายหรือเจ้าหน้าที่เท่านั้น")
        appt.delete()
        return redirect("appointment-calendar")


# ================================
# CALENDAR
# ================================
class AppointmentCalendarView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, year=None, month=None):
        today = localdate()
        if year is None or month is None:
            url = reverse("appointment-calendar", kwargs={"year": today.year, "month": today.month})
            qs = request.META.get("QUERY_STRING")
            return redirect(f"{url}?{qs}" if qs else url)

        y, m = int(year), int(month)
        prev_y, prev_m = (y - 1, 12) if m == 1 else (y, m - 1)
        next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)

        profile, _ = Profile.objects.get_or_create(user=request.user)
        appts_month = (
            Appointment.objects
            .filter(patient=profile, date__year=y, date__month=m)
            .select_related("clinic", "patient")
            .order_by("date", "at_time")
        )

        # group นัดหมายตามวัน
        appts_by_day = {}
        for a in appts_month:
            key = a.date.isoformat()
            appts_by_day.setdefault(key, []).append({
                "id": a.pk,
                "date": a.date.isoformat(),
                "weekday": a.date.strftime("%A"),
                "time": a.at_time.strftime("%H:%M"),
                "doctor": a.doctor_name,
                "patient": str(a.patient),
                "clinic": a.clinic.name,
                "details": a.details or "—",
            })

        # วันทั้งหมดที่มีนัด
        dates_with_appt = set(appts_month.values_list("date", flat=True))

        # สร้างปฏิทินรายสัปดาห์
        cal = calendar.Calendar(firstweekday=6)
        weeks, week = [], []
        for d in cal.itermonthdates(y, m):
            week.append({
                "date": d,
                "in_month": d.month == m,
                "is_today": d == today,
                "has_appt": d in dates_with_appt,
            })
            if len(week) == 7:
                weeks.append(week)
                week = []

        # กำหนดวันที่เลือก (highlight)
        selected_date = (
            today.isoformat()
            if y == today.year and m == today.month
            else next((d.isoformat() for d in sorted(dates_with_appt) if d.month == m), "")
        )

        ctx = {
            "year": y, "month": m, "month_name": calendar.month_name[m],
            "weeks": weeks, "prev_year": prev_y, "prev_month": prev_m,
            "next_year": next_y, "next_month": next_m,
            "appts_by_day": appts_by_day, "selected_date": selected_date,
            "today": today,
        }
        return render(request, "calendar.html", ctx)
