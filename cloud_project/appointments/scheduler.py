from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

scheduler = BackgroundScheduler()

def start():
    if not scheduler.get_jobs():
        scheduler.add_job(
            lambda: call_command("send_tomorrow_appointment_emails"),
            "cron",
            hour=8,
            minute=00,
            timezone="Asia/Bangkok"
        )
        scheduler.start()
        print("✅ APScheduler started (will run at 08.00)")
