from django import forms
from .models import Drug, MedicationIntake


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ["name", "generic_name", "strength", "form", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "ชื่อยา",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "generic_name": forms.TextInput(
                attrs={
                    "placeholder": "ชื่อสามัญทางยา",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "strength": forms.TextInput(
                attrs={
                    "placeholder": "ขนาดยา เช่น 500 mg",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "form": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                            "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "รายละเอียดเพิ่มเติม...",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200 resize-none"
                }
            ),
        }

from django import forms
from .models import MedicationIntake


class MedicationIntakeForm(forms.ModelForm):
    class Meta:
        model = MedicationIntake
        # fields = ["drug", "dose", "frequency", "instruction", "start_date", "end_date", "note", "active"]
        fields = ["drug", "dose", "time", "note", "active"]

        widgets = {
            "drug": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "dose": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            # "frequency": forms.Select(  # ดึง choices จาก model อัตโนมัติ
            #     attrs={
            #         "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
            #                  "focus:outline-none focus:ring-2 focus:ring-gray-200"
            #     }
            # ),
            # "instruction": forms.Select(  # ดึง choices จาก model อัตโนมัติ
            #     attrs={
            #         "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
            #                  "focus:outline-none focus:ring-2 focus:ring-gray-200"
            #     }
            # ),
            # "start_date": forms.DateInput(
            #     attrs={
            #         "type": "date",
            #         "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
            #                  "focus:outline-none focus:ring-2 focus:ring-gray-200"
            #     }
            # ),
            # "end_date": forms.DateInput(
            #     attrs={
            #         "type": "date",
            #         "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
            #                  "focus:outline-none focus:ring-2 focus:ring-gray-200"
            #     }
            # ),

            # ⏰ เพิ่มช่อง “เวลา”
            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "บันทึกเพิ่มเติม...",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200 resize-none"
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "rounded border-gray-300 text-indigo-600 focus:ring-gray-200"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        # ✅ ดึง user ที่ส่งมาจาก view
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # ✅ ถ้ามี user → กรอง queryset ของ drug ให้เฉพาะยาของ user คนนั้น
        if user:
            self.fields["drug"].queryset = Drug.objects.filter(user=user)