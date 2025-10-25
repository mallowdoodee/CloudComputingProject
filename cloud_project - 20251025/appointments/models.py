from datetime import datetime, date
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True)
    address      = models.TextField(blank=True)
    birth_date   = models.DateField(null=True, blank=True)

    def __str__(self):
        full = self.user.get_full_name().strip()
        return full or self.user.username

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

class Clinic(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    code        = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.description

class Appointment(models.Model):
    clinic        = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name="appointments")
    patient       = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="appointments")
    title = models.TextField(null=True, blank=True)
    # เก็บชื่อหมอเป็นข้อความ (ไม่ต้องมี Doctor model)
    doctor_name   = models.CharField(max_length=150)
    doctor_phone  = models.CharField(max_length=20, blank=True)  # optional เผื่อจดเบอร์
    doctor_email  = models.EmailField(blank=True)                # optional เผื่อจดอีเมล
    date          = models.DateField()
    at_time       = models.TimeField()
    details       = models.TextField(null=True, blank=True)

    # อาการป่วย
    condition = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["date", "at_time"]
        indexes = [
            models.Index(fields=["date", "at_time"]),
            models.Index(fields=["clinic"]),
        ]

    def __str__(self):
        when = datetime.combine(self.date, self.at_time).strftime("%Y-%m-%d %H:%M")
        return f"Appt {self.patient} · {self.clinic} · {self.doctor_name} @ {when}"
