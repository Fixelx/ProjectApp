from projects.models import ProjectMembership, Project
from .models import CompanySetting

def project_switcher(request):
    if not request.user.is_authenticated:
        return {"user_projects": [], "archived_count": 0}

    memberships = ProjectMembership.objects.select_related("project").filter(
        user=request.user,
        project__active=True
    )

    archived_count = ProjectMembership.objects.filter(
        user=request.user,
        project__active=False
    ).count()

    return {
        "user_projects": [m.project for m in memberships],
        "archived_count": archived_count,
    }


def company_settings(request):
    return {
        "company_settings": CompanySetting.objects.first()
    }