from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from projects.models import ProjectMembership

@login_required
def dashboard(request):
    memberships = ProjectMembership.objects.select_related("project").filter(user=request.user,project__active=True)
    archived_count = ProjectMembership.objects.filter(user=request.user,project__active=False).count()
    return render(request,"core/dashboard.html",{"memberships": memberships,"archived_count": archived_count,})