# medications/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Drug(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้ใช้", null=True, blank=True)
    FORM_CHOICES = [
        ("TAB", "เม็ด"),
        ("CAP", "แคปซูล"),
        ("SYP", "น้ำเชื่อม"),
        ("SOL", "สารละลาย/หยด"),
        ("INJ", "ฉีด"),
        ("OTH", "อื่น ๆ"),
    ]
    name = models.CharField(max_length=100, verbose_name="ชื่อยา")
    generic_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="ชื่อสามัญ (Generic)")
    strength = models.CharField(max_length=50, blank=True, null=True, verbose_name="ขนาดยา เช่น 500mg")
    form = models.CharField(max_length=10, choices=FORM_CHOICES, default="TAB", verbose_name="รูปแบบยา")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียดเพิ่มเติม")

    def __str__(self):
        return f"{self.name}{f' ({self.strength})' if self.strength else ''}"

class MedicationIntake(models.Model):
    FREQ_CHOICES = [
        ("QD", "วันละครั้ง"),
        ("BID", "วันละ 2 ครั้ง (เช้า–เย็น)"),
        ("TID", "วันละ 3 ครั้ง"),
        ("QID", "วันละ 4 ครั้ง"),
        ("PRN", "เมื่อมีอาการ"),
    ]
    INSTRUCTION_CHOICES = [
        ("BEFORE", "ก่อนอาหาร"),
        ("AFTER", "หลังอาหาร"),
        ("WITH", "พร้อมอาหาร"),
        ("NONE", "ไม่ระบุ"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้ใช้")
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name="ยา")
    dose = models.CharField(max_length=100, verbose_name="ขนาด/จำนวน", help_text="เช่น 1 เม็ด")
    frequency = models.CharField(max_length=10, choices=FREQ_CHOICES, default="QD", verbose_name="ความถี่")
    instruction = models.CharField(max_length=10, choices=INSTRUCTION_CHOICES, default="NONE", verbose_name="คำแนะนำ")
    time = models.TimeField(blank=True, null=True, verbose_name="เวลาที่ต้องกิน")
    start_date = models.DateField(default=timezone.localdate, verbose_name="วันที่เริ่ม")
    end_date = models.DateField(blank=True, null=True, verbose_name="วันที่สิ้นสุด")
    note = models.TextField(blank=True, null=True, verbose_name="หมายเหตุเพิ่มเติม")
    active = models.BooleanField(default=True, verbose_name="ยังใช้อยู่")

    class Meta:
        ordering = ["-active", "start_date"]

    def __str__(self):
        return f"{self.user.username} - {self.drug.name}"
