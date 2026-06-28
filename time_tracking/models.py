from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()


class TimeEntry(models.Model):

    class EntryType(models.TextChoices):
        TRAVEL = "travel", "Anfahrt"
        WORK = "work", "Arbeitszeit"

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="time_entries",
        verbose_name="Projekt"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="time_entries",
        verbose_name="Mitarbeiter"
    )

    entry_type = models.CharField(
        max_length=20,
        choices=EntryType.choices,
        default=EntryType.WORK,
        verbose_name="Typ"
    )

    activity = models.CharField(
        max_length=255,
        verbose_name="Tätigkeit",
        blank=True,
    )

    start = models.DateTimeField(
        verbose_name="Beginn"
    )

    end = models.DateTimeField(null=True, blank=True)

    break_minutes = models.PositiveIntegerField(
        default=0,
        verbose_name="Pause (Minuten)"
    )

    note = models.TextField(
        blank=True,
        verbose_name="Notiz"
    )

    invoiced = models.BooleanField(default=False,verbose_name="Abgerechnet")

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Zeiterfassung"
        verbose_name_plural = "Zeiterfassungen"
        ordering = ["-start"]

    def __str__(self):
        return f"{self.user} - {self.start:%d.%m.%Y} - {self.duration_hours} Stunden"

    def clean(self):
        if self.start and self.end and self.start >= self.end:
            raise ValidationError({
                'end': 'Das Ende muss nach dem Start liegen.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def duration_minutes(self):

        if not self.end:
            return 0

        duration = (self.end - self.start).total_seconds() / 60
        return max(0, int(duration) - self.break_minutes)

    @property
    def duration_hours(self):

        if not self.end:
            return 0

        return round(self.duration_minutes / 60, 2)

    @property
    def duration_minutes_total(self):
        end = self.end or None
        if not end:
            return 0
        return max(0, int((end - self.start).total_seconds() / 60) - self.break_minutes)

    @property
    def duration_hhmm(self):
        total_minutes = self.duration_minutes_total

        hours = total_minutes // 60
        minutes = total_minutes % 60

        return f"{hours:02d}:{minutes:02d}"