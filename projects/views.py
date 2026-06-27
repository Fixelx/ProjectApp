from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from .forms import ProjectForm, ProjectAddLocationForm, ProjectAddContactForm, ProjectAddForm, ProjectAddWorkerForm

from .models import (
    Project,
    ProjectMembership,
    ProjectContact,
    ProjectLocation,
)

from invoices.models import CustomerContact, CustomerLocation



@login_required
@permission_required("projects_add")
def project_add(request):
    form = ProjectAddForm(request.POST or None,request.FILES or None,)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        ProjectMembership.objects.create(project=project,user=request.user,role=ProjectMembership.Role.OWNER,)
        return redirect("projects:overview",project.id)

    return render(request,"projects/add.html",{"form": form,})



@login_required
@permission_required("projects_archived_view")
def projects_archived(request):
    memberships = ProjectMembership.objects.select_related("project").filter(user=request.user,project__active=False)
    return render(request,"projects/archived.html",{"memberships": memberships,})



# ---------------------------
# OVERVIEW
# ---------------------------
@login_required
@permission_required("projects_view")
def project_overview(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    return render(request, "projects/overview.html", {
        "project": project,
        "role": membership.role
    })


@login_required
@permission_required("projects_detail_view")
def project_info(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    form = ProjectForm(
        instance=project
    )

    workers = project.memberships.select_related(
        "user"
    ).all()


    return render(
        request,
        "projects/info.html",
        {
            "project": project,
            "form": form,

            "locations": project.project_locations.select_related(
                "location"
            ),

            "contacts": project.project_contacts.select_related(
                "contact"
            ),

            "workers": workers,
        }
    )


@login_required
@permission_required("projects_edit")
def project_edit(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project


    if request.method != "POST":
        return redirect(
            "projects:info",
            project.id
        )


    form = ProjectForm(
        request.POST,
        request.FILES,
        instance=project
    )


    if form.is_valid():
        form.save()


    return redirect(
        "projects:info",
        project.id
    )

# ---------------------------
# ADD CONTACT TO PROJECT
# ---------------------------
@login_required
@permission_required("projects_contact_add")
def project_contact_add(request, project_id):

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectAddContactForm(
            request.POST,
            project=project,
        )

        if form.is_valid():
            contact = form.cleaned_data["contact"]

            ProjectContact.objects.get_or_create(
                project=project,
                contact=contact
            )

            return redirect("projects:info", project.id)

    else:
        form = ProjectAddContactForm(project=project)

    return render(request, "projects/contact_add.html", {
        "form": form,
        "project": project,
    })

@login_required
@permission_required("projects_contact_delete")
def project_contact_delete(request, project_id, contact_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project


    if request.method == "POST":

        ProjectContact.objects.filter(
            id=contact_id,
            project=project
        ).delete()


    return redirect(
        "projects:info",
        project.id
    )











# ---------------------------
# ADD LOCATION TO PROJECT
# ---------------------------
@login_required
@permission_required("projects_location_add")
def project_location_add(request, project_id):

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectAddLocationForm(
            request.POST,
            project=project,
        )

        if form.is_valid():
            location = form.cleaned_data["location"]

            ProjectLocation.objects.get_or_create(
                project=project,
                location=location
            )

            return redirect("projects:info", project.id)

    else:
        form = ProjectAddLocationForm(project=project)

    return render(request, "projects/location_add.html", {
        "form": form,
        "project": project,
    })

@login_required
@permission_required("projects_location_delete")
def project_location_delete(request, project_id, location_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project


    if request.method == "POST":

        ProjectLocation.objects.filter(
            id=location_id,
            project=project
        ).delete()


    return redirect(
        "projects:info",
        project.id
    )


@login_required
@permission_required("projects_user_add")
def project_worker_add(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    get_object_or_404(ProjectMembership,project=project,user=request.user)
    form = ProjectAddWorkerForm(request.POST or None,project=project)

    if request.method == "POST" and form.is_valid():
        membership = form.save(commit=False)
        membership.project = project
        membership.save()
        return redirect("projects:info",project.id)

    return render(request,"projects/worker_add.html",{"form": form,"project": project,})


@login_required
@permission_required("projects_user_delete")
def project_worker_delete(request, project_id, worker_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project


    worker = get_object_or_404(
        ProjectMembership,
        id=worker_id,
        project=project
    )


    if request.method == "POST":

        if worker.role != ProjectMembership.Role.OWNER:
            worker.delete()


    return redirect(
        "projects:info",
        project.id
    )