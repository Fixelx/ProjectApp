from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from projects.models import ProjectMembership
from .models import Document, DocumentCategory
from .forms import DocumentForm


@login_required
@permission_required("projects_documents_view")
def document_overview(request, project_id):

    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
    project = membership.project

    documents = Document.objects.filter(project=project).order_by("-created_at")
    categories = DocumentCategory.objects.all()

    form = DocumentForm()

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.project = project
            doc.uploaded_by = request.user
            doc.save()
            return redirect("documents:overview", project.id)

    # gruppiert nach Kategorie
    grouped = {}

    for cat in categories:
        docs = list(documents.filter(category=cat))

        if docs:
            grouped[cat] = docs

    uncategorized = documents.filter(category__isnull=True)

    return render(request, "documents/overview.html", {
        "project": project,
        "form": form,
        "grouped": grouped,
        "uncategorized": uncategorized,
    })


@login_required
@permission_required("projects_documents_delete")
def document_delete(request, project_id, doc_id):
    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
    doc = get_object_or_404(Document, id=doc_id, project=membership.project)
    doc.file.delete()
    doc.delete()
    return redirect("documents:overview", project_id)


@login_required
@permission_required("projects_documents_add")
def document_add(request, project_id):
    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
    project = membership.project

    documents = Document.objects.filter(project=project).order_by("-created_at")
    categories = DocumentCategory.objects.all()

    form = DocumentForm()

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.project = project
            doc.uploaded_by = request.user
            doc.save()
            return redirect("documents:overview", project.id)
    else:
        form = DocumentForm()

    return render(
        request,
        "documents/add.html",
        {
            "project": project,
            "form": form,
        }
    )