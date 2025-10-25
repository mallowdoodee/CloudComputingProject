from django import forms
from django.utils import timezone
from .models import Symptom


class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ["name", "note", "date", "time"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none "
                         "focus:ring-2 focus:ring-[#981E1E] focus:border-transparent",
                "placeholder": "ชื่ออาการ เช่น ปวดหัว / เวียนหัว / ไอ",
            }),
            "note": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none "
                         "focus:ring-2 focus:ring-[#981E1E] focus:border-transparent",
                "placeholder": "รายละเอียดเพิ่มเติม เช่น ปวดข้างซ้าย เริ่มตั้งแต่เมื่อเช้า...",
            }),
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-[#981E1E] focus:border-transparent",
                }
            ),
            "time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-lg bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-[#981E1E] focus:border-transparent",
                }
            ),
        }

        labels = {
            "name": "ชื่ออาการ",
            "note": "รายละเอียด / โน้ตเพิ่มเติม",
            "date": "วันที่เกิดอาการ",
            "time": "เวลาที่เกิดอาการ",
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ให้ค่าเริ่มต้นของ date และ time เป็นวันและเวลาปัจจุบัน
        if not self.instance.pk:
            if not self.initial.get("date"):
                self.initial["date"] = timezone.localdate()
            if not self.initial.get("time"):
                self.initial["time"] = timezone.localtime().strftime("%H:%M")
