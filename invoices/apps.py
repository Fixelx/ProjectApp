from django.apps import AppConfig


class InvoicesConfig(AppConfig):
    name = "invoices"

    def ready(self):
        import sys

        if any(cmd in sys.argv for cmd in ("migrate", "makemigrations", "shell", "test")):
            return

        from django.db import connection
        if "django_apscheduler_djangojob" not in connection.introspection.table_names():
            return

        from django_apscheduler.jobstores import DjangoJobStore
        from apscheduler.schedulers.background import BackgroundScheduler
        from . import scheduler

        sched = BackgroundScheduler()
        sched.add_jobstore(DjangoJobStore(), "default")

        sched.add_job(
            scheduler.mark_overdue,
            trigger="cron",
            hour=1,
            minute=0,
            id="mark_overdue",
            replace_existing=True,
        )

        sched.start()
