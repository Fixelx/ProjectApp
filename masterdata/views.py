from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from collections import defaultdict
from .registry import MASTERDATA
from django.forms import modelform_factory
from django.apps import apps
from core.forms.base import BaseForm
import subprocess
from django.http import JsonResponse
from django.conf import settings
import sys
from pathlib import Path

def get_registry_entry(model_name):
    entry = next(
        (
            x for x in MASTERDATA
            if x["model_name"] == model_name
        ),
        None
    )
    if not entry:
        raise Http404
    return entry

def create_setting_form(model):
    Meta = type(
        "Meta",
        (),
        {
            "model": model,
            "fields": "__all__",
        }
    )
    FormClass = type(
        f"{model.__name__}Form",
        (BaseForm,),
        {
            "Meta": Meta,

            "__init__": lambda self, *args, **kwargs: (
                BaseForm.__init__(self, *args, **kwargs),
                self.apply_style()
            )[-1]
        }
    )
    return FormClass

@login_required
@permission_required("settings_view")
def overview(request):
    groups = defaultdict(list)
    for item in MASTERDATA:
        groups[item["group"]].append(item)
    return render(request,"masterdata/overview.html",{"groups": dict(groups)})

@login_required
@permission_required("settings_detail_view")
def setting_detail(request, model_name):
    entry = get_registry_entry(model_name)
    model = entry["model"]
    if entry["type"] == "single":
        obj = model.objects.first()
        Form = create_setting_form(model)
        if request.method == "POST":
            form = Form(request.POST,request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                return redirect("masterdata:detail",model_name=model_name)
        else:
            form = Form(instance=obj)
        return render(request,"masterdata/detail_single.html",{"title": entry["verbose_name_plural"],"form": form,"object": obj,"model_name": model_name,})
    objects = model.objects.all()
    return render(request,"masterdata/detail.html",{"title": entry["verbose_name_plural"],"objects": objects,"model_name": model_name,})

@login_required
@permission_required("settings_add")
def setting_add(request, model_name):
    entry = get_registry_entry(model_name)
    model = entry["model"]
    if entry["type"] == "single":
        if model.objects.exists():
            return redirect("masterdata:detail",model_name=model_name)
    Form = create_setting_form(model)
    if request.method == "POST":
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("masterdata:detail",model_name=model_name)
    else:
        form = Form()
    return render(request,"masterdata/add.html",{"form": form,"title": f"{entry['verbose_name']}",})

@login_required
@permission_required("settings_delete")
def setting_delete(request, model_name, pk):
    entry = get_registry_entry(model_name)
    model = entry["model"]
    if entry["type"] == "single":
        return redirect("masterdata:detail",model_name=model_name)
    obj = get_object_or_404(model,pk=pk)
    if request.method == "POST":
        obj.delete()
    return redirect("masterdata:detail",model_name=model_name)

























BASE_DIR = settings.BASE_DIR

def _git(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
    return r.stdout.strip(), r.returncode

def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
    return r.stdout.strip(), r.returncode


@login_required
@permission_required("settings_update_check")
def update_check(request):
    _git(["git", "fetch", "origin"])
    local, _   = _git(["git", "rev-parse", "HEAD"])
    remote, _  = _git(["git", "rev-parse", "origin/main"])
    branch, _  = _git(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    log, _     = _git(["git", "log", f"{local}..{remote}", "--oneline"])
    date, _    = _git(["git", "log", "-1", "--format=%cd", "--date=format:%d.%m.%Y %H:%M"])
    author, _  = _git(["git", "log", "-1", "--format=%an"])
    msg, _     = _git(["git", "log", "-1", "--format=%s"])

    return JsonResponse({
        "up_to_date": local == remote,
        "local":      local[:7],
        "remote":     remote[:7],
        "branch":     branch,
        "changes":    log.splitlines() if log else [],
        "last_commit_date":   date,
        "last_commit_author": author,
        "last_commit_msg":    msg,
    })
    
@login_required
@permission_required("settings_update_apply")
def update_apply(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    _, code = _git(["git", "pull", "origin", "main"])
    if code != 0:
        return JsonResponse({"error": "git pull fehlgeschlagen"}, status=500)

    _, pip_code = _run([sys.executable, "-m", "pip", "install", "-r", str(BASE_DIR / "requirements.txt"), "-q"])
    if pip_code != 0:
        return JsonResponse({"error": "pip install fehlgeschlagen"}, status=500)

    _, migrate_code = _run([sys.executable, "manage.py", "migrate", "--no-input"])
    if migrate_code != 0:
        return JsonResponse({"error": "Migration fehlgeschlagen"}, status=500)

    return JsonResponse({"success": True})