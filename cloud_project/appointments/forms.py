from django import forms
from django.db.models import Q

from .models import Appointment, Clinic


class ClinicChoiceField(forms.ModelChoiceField):
    """Allow typing a clinic name instead of picking from a dropdown."""

    def prepare_value(self, value):
        if isinstance(value, Clinic):
            return value.name
        return super().prepare_value(value)

    def to_python(self, value):
        if not value:
            return super().to_python(value)
        if isinstance(value, Clinic):
            return value

        value = (value or "").strip()
        if not value:
            return super().to_python(value)

        try:
            return super().to_python(value)
        except (ValueError, self.queryset.model.DoesNotExist):
            pass

        match = (
            self.queryset.filter(
                Q(name__iexact=value) | Q(description__iexact=value)
            )
            .order_by("name")
            .first()
        )
        if match:
            return match
        raise forms.ValidationError("Clinic or hospital not found.")


class AppointmentForm(forms.ModelForm):
    clinic = ClinicChoiceField(
        queryset=Clinic.objects.order_by("name"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Clinic or hospital name",
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                         "focus:outline-none focus:ring-2 focus:ring-gray-200",
                "autocomplete": "off",
                "list": "clinic-options",
            }
        ),
    )

    class Meta:
        model = Appointment
        fields = [
            "title",
            "clinic",
            "doctor_name",
            "doctor_phone",
            "doctor_email",
            "condition",
            "address",
            "date",
            "at_time",
            "details",
            "patient",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Purpose of medical appointment",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "doctor_name": forms.TextInput(
                attrs={
                    "placeholder": "docker's name",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "doctor_phone": forms.TextInput(
                attrs={
                    "placeholder": "doctor's number",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "doctor_email": forms.EmailInput(
                attrs={
                    "placeholder": "docter's email",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "condition": forms.TextInput(
                attrs={
                    "placeholder": "Presenting symptoms",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Hospital address",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "at_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "details": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "more detail",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200 resize-none"
                }
            ),
            "patient": forms.Select(
                attrs={
                    "class": "w-full select-arrow border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Text input does not use Django's default empty label.
        self.fields["clinic"].empty_label = None
