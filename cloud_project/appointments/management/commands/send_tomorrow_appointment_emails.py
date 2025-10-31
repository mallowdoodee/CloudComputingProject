from django.core.management.base import BaseCommand
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from appointments.models import Appointment  # ✅ แก้ชื่อแอปให้ถูกต้อง
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "ส่งอีเมลเตือนนัดหมายล่วงหน้า 1 วัน (รายผู้ใช้) โดยใช้อีเมลจาก auth_user.email"

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        appointments = (
            Appointment.objects
            .select_related("patient__user", "clinic")
            .filter(date=tomorrow)
        )

        if not appointments.exists():
            self.stdout.write("ไม่มีนัดหมายของวันพรุ่งนี้")
            return

        sent_count = 0
        skipped_count = 0

        for appt in appointments:
            user = appt.patient.user  # ✅ ดึง user ที่แท้จริงจาก Profile
            if not getattr(user, "email", None) or not user.is_active:
                skipped_count += 1
                logger.warning(f"ข้าม {user.username}: ไม่มีอีเมลหรือ inactive")
                continue

            subject = "แจ้งเตือนนัดหมายแพทย์ล่วงหน้า 1 วัน 🩺"
            time_str = appt.at_time.strftime("%H:%M") if appt.at_time else "ไม่ระบุเวลา"

            message = (
                f"เรียนคุณ {user.first_name or user.username},\n\n"
                f"ขอแจ้งเตือนว่าวันพรุ่งนี้ ({appt.date}) "
                f"คุณมีนัดกับ {appt.doctor_name} ที่คลินิก {appt.clinic.name}\n"
                f"เวลา: {time_str} น.\n\n"
                f"กรุณามาตรงเวลา และนำเอกสารที่จำเป็นมาด้วย\n\n"
                f"- ระบบแจ้งเตือนอัตโนมัติ -"
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(f"ส่งอีเมลแจ้งเตือนให้ {user.email}")
            except Exception as e:
                logger.error(f"ส่งอีเมลล้มเหลว {user.email}: {e}")

        self.stdout.write(
            self.style.SUCCESS(f"สำเร็จ: ส่ง {sent_count} ฉบับ | ข้าม {skipped_count} ราย")
        )
