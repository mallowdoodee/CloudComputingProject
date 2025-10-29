from django import forms
from django.utils import timezone
from .models import Symptom

INPUT_STYLE = (
    "w-full rounded-2xl bg-[#f1f2f6] px-4 py-3 text-base text-gray-900 placeholder-gray-400 "
    "focus:outline-none focus:ring-2 focus:ring-[#d05a6b] focus:border-transparent transition-colors"
)
TEXTAREA_STYLE = INPUT_STYLE + " min-h-[120px] resize-none"


class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ["name", "note", "date", "time"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Add Symptom Description",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": TEXTAREA_STYLE,
                    "placeholder": "Any additional details about the symptom...",
                }
            ),
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": INPUT_STYLE,
                },
            ),
            "time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                    "class": INPUT_STYLE,
                    "placeholder": "12:00",
                },
            ),
        }

        labels = {
            "name": "Symptom Description",
            "note": "Additional Notes (Optional)",
            "date": "Date Started",
            "time": "Time Started",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ตั้งค่าวันเริ่มต้นเป็นวันนี้
        if not self.instance.pk:
            if not self.initial.get("date"):
                self.initial["date"] = timezone.localdate()
            if not self.initial.get("time"):
                self.initial["time"] = timezone.localtime().strftime("%H:%M")

        # 🚫 ห้ามเลือกวันที่ในอนาคต
        self.fields["date"].widget.attrs["max"] = timezone.localdate().isoformat()
