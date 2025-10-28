from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
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
                    "placeholder": "หัวข้อการนัดหมาย เช่น ตรวจสุขภาพประจำปี, ตรวจฟัน",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "clinic": forms.Select(
                attrs={
                    "class": "w-full select-arrow border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "doctor_name": forms.TextInput(
                attrs={
                    "placeholder": "ชื่อแพทย์ผู้ตรวจ เช่น นพ.สมชาย ใจดี",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "doctor_phone": forms.TextInput(
                attrs={
                    "placeholder": "เบอร์โทรศัพท์แพทย์ (ถ้ามี)",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "doctor_email": forms.EmailInput(
                attrs={
                    "placeholder": "อีเมลแพทย์ (ถ้ามี)",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "condition": forms.TextInput(
                attrs={
                    "placeholder": "อาการหรือเหตุผลที่ไปพบแพทย์ เช่น ปวดหัว, ตรวจตา",
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white "
                             "focus:outline-none focus:ring-2 focus:ring-gray-200"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "สถานที่นัดหมาย เช่น โรงพยาบาลลาดกระบัง, คลินิกสมใจ",
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
                    "placeholder": "รายละเอียดเพิ่มเติม เช่น เตรียมผลตรวจ, ถือเอกสารไปด้วย",
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
