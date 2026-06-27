from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime
from projects.models import ProjectMembership
from .models import TimeEntry
from django_tables2 import RequestConfig
from .tables import TimeEntryTable

@login_required
@permission_required("projects_time_tracking_view")
def time_tracking_overview(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        project_id=project_id,
        user=request.user
    )

    project = membership.project


    # ==========================
    # POST ACTIONS
    # ==========================

    if request.method == "POST":

        action = request.POST.get("action")


        # --------------------------
        # START TIMER
        # --------------------------

        if action == "start":

            open_entry = TimeEntry.objects.filter(
                project=project,
                user=request.user,
                end__isnull=True
            ).first()


            if not open_entry:

                TimeEntry.objects.create(
                    project=project,
                    user=request.user,
                    entry_type=TimeEntry.EntryType.WORK,
                    activity="",
                    start=timezone.now(),
                    break_minutes=0,
                )


            return redirect(
                "time_tracking:overview",
                project.id
            )


        # --------------------------
        # STOP TIMER
        # --------------------------

        if action == "stop":

            open_entry = TimeEntry.objects.filter(
                project=project,
                user=request.user,
                end__isnull=True
            ).order_by("-start").first()


            if open_entry:

                open_entry.end = timezone.now()

                open_entry.save(
                    update_fields=[
                        "end"
                    ]
                )


            return redirect(
                "time_tracking:overview",
                project.id
            )


        # --------------------------
        # ADD ENTRY
        # --------------------------

        if action == "add":

            start_str = request.POST.get("start", "")
            end_str = request.POST.get("end", "")
            
            start_dt = None
            end_dt = None
            
            try:
                start_dt = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
                start_dt = timezone.make_aware(start_dt)
            except (ValueError, TypeError):
                pass
            
            if end_str:
                try:
                    end_dt = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
                    end_dt = timezone.make_aware(end_dt)
                except (ValueError, TypeError):
                    pass

            TimeEntry.objects.create(
                project=project,
                user=request.user,
                entry_type=request.POST.get("entry_type"),
                activity=request.POST.get("activity"),
                start=start_dt or timezone.now(),
                end=end_dt,
                break_minutes=request.POST.get("break_minutes") or 0,
                note=request.POST.get("note", "")
            )


            return redirect(
                "time_tracking:overview",
                project.id
            )



    # ==========================
    # TABLE
    # ==========================

    entries = project.time_entries.select_related(
        "user"
    ).order_by(
        "-start"
    )


    table = TimeEntryTable(
        entries,
        request=request,
    )

    RequestConfig(
        request,
        paginate={
            "per_page": 25
        }
    ).configure(table)



    # ==========================
    # RESPONSE
    # ==========================

    return render(
        request,
        "time_tracking/overview.html",
        {
            "project": project,
            "table": table,
            "types": TimeEntry.EntryType.choices,
        }
    )


@login_required
@permission_required("projects_time_tracking_edit")
def time_tracking_edit(request, project_id, entry_id):

    membership = get_object_or_404(
        ProjectMembership,
        project_id=project_id,
        user=request.user
    )

    project = membership.project


    if request.method != "POST":
        return redirect(
            "time_tracking:overview",
            project.id
        )


    entry = get_object_or_404(
        TimeEntry,
        id=entry_id,
        project=project
    )

    # Parse datetime fields
    start_str = request.POST.get("start", "")
    end_str = request.POST.get("end", "")
    
    try:
        # Format: "Y-m-dTH:i" (e.g., "2026-06-27T13:36")
        entry.start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
        entry.start = timezone.make_aware(entry.start)
    except (ValueError, TypeError):
        pass
    
    if end_str:
        try:
            entry.end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
            entry.end = timezone.make_aware(entry.end)
        except (ValueError, TypeError):
            entry.end = None
    else:
        entry.end = None

    entry.entry_type = request.POST.get("entry_type")
    entry.activity = request.POST.get("activity")
    entry.break_minutes = request.POST.get("break_minutes") or 0
    entry.note = request.POST.get("note", "")

    entry.save()


    return redirect(
        "time_tracking:overview",
        project.id
    )


@login_required
@permission_required("projects_time_tracking_delete")
def time_tracking_delete(request, project_id, entry_id):

    membership = get_object_or_404(
        ProjectMembership,
        project_id=project_id,
        user=request.user
    )

    project = membership.project


    if request.method == "POST":

        TimeEntry.objects.filter(
            id=entry_id,
            project=project
        ).delete()


    return redirect(
        "time_tracking:overview",
        project.id
    )