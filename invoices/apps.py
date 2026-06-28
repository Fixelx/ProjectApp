from django.apps import AppConfig

class InvoicesConfig(AppConfig):
    name = "invoices"

    def ready(self):
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