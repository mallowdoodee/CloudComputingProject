from django import forms
from .models import Drug, MedicationIntake

INPUT_STYLE = (
    "w-full rounded-2xl bg-gray-100 border border-transparent px-4 py-3 "
    "text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 "
    "focus:ring-rose-300 focus:border-rose-400 transition-colors"
)
TEXTAREA_STYLE = INPUT_STYLE + " resize-none min-h-[120px]"
CHECKBOX_STYLE = "h-5 w-5 rounded border-gray-300 text-rose-500 focus:ring-rose-300 focus:outline-none"


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ["name", "generic_name", "strength", "form", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Medicine's Name",
                    "class": INPUT_STYLE,
                }
            ),
            "generic_name": forms.TextInput(
                attrs={
                    "placeholder": "generic name",
                    "class": INPUT_STYLE,
                }
            ),
            "strength": forms.TextInput(
                attrs={
                    "placeholder": "3",
                    "class": INPUT_STYLE,
                }
            ),
            "form": forms.Select(
                attrs={
                    "class": INPUT_STYLE,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "4",
                    "class": TEXTAREA_STYLE,
                }
            ),
        }


class MedicationIntakeForm(forms.ModelForm):
    class Meta:
        model = MedicationIntake
        # fields = ["drug", "dose", "frequency", "instruction", "start_date", "end_date", "note", "active"]
        fields = ["drug", "dose", "time", "note", "active"]

        widgets = {
            "drug": forms.Select(
                attrs={
                    "class": INPUT_STYLE,
                }
            ),
            "dose": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                }
            ),
            # "frequency": forms.Select(
            #     attrs={
            #         "class": INPUT_STYLE,
            #     }
            # ),
            # "instruction": forms.Select(
            #     attrs={
            #         "class": INPUT_STYLE,
            #     }
            # ),
            # "start_date": forms.DateInput(
            #     attrs={
            #         "type": "date",
            #         "class": INPUT_STYLE,
            #     }
            # ),
            # "end_date": forms.DateInput(
            #     attrs={
            #         "type": "date",
            #         "class": INPUT_STYLE,
            #     }
            # ),
            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": INPUT_STYLE,
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "5",
                    "class": TEXTAREA_STYLE,
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_STYLE,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["drug"].queryset = Drug.objects.filter(user=user)
