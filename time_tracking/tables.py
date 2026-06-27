import django_tables2 as tables

from .models import TimeEntry


class TimeEntryTable(tables.Table):

    entry_type = tables.TemplateColumn(
        template_name="time_tracking/tables/entry_type.html",
        verbose_name="Typ",
        orderable=False,
    )

    activity = tables.TemplateColumn(
        template_name="time_tracking/tables/activity.html",
        verbose_name="Aktivität",
        orderable=False,
    )

    start = tables.TemplateColumn(
        template_name="time_tracking/tables/start.html",
        verbose_name="Start",
        orderable=False,
    )

    end = tables.TemplateColumn(
        template_name="time_tracking/tables/end.html",
        verbose_name="Ende",
        orderable=False,
    )

    break_minutes = tables.TemplateColumn(
        template_name="time_tracking/tables/break.html",
        verbose_name="Pause (Min)",
        orderable=False,
    )

    duration = tables.Column(
        accessor="duration_hhmm",
        verbose_name="Dauer",
        orderable=False,
    )

    invoiced = tables.TemplateColumn(
        template_name="time_tracking/tables/invoiced.html",
        verbose_name="Abgerechnet",
        orderable=False,
    )

    actions = tables.TemplateColumn(
        template_name="time_tracking/tables/actions.html",
        verbose_name="Aktionen",
        orderable=False,
    )


    class Meta:

        model = TimeEntry

        template_name = "django_tables2/table.html"

        attrs = {
            "class": "w-full text-sm min-w-[1200px]"
        }

        fields = (
            "entry_type",
            "activity",
            "start",
            "end",
            "break_minutes",
            "duration",
            "invoiced",
            "actions",
        )


    def __init__(self, *args, types=None, project=None, **kwargs):

        self.types = types
        self.project = project

        super().__init__(*args, **kwargs)


    def before_render(self, request):

        for row in self.rows:
            row.record.project = self.project
            row.record.types = self.types