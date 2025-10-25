from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Symptom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้ใช้")
    name = models.CharField(max_length=100, verbose_name="ชื่ออาการ")
    note = models.TextField(blank=True, null=True, verbose_name="รายละเอียด / โน้ตเพิ่มเติม")
    date = models.DateField(default=timezone.localdate, verbose_name="วันที่เกิดอาการ")
    time = models.TimeField(blank=True, null=True, verbose_name="เวลาที่เกิดอาการ")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="เวลาที่บันทึก")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.date:%Y-%m-%d} {self.time or ''})"
