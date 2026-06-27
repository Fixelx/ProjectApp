from projects.models import ProjectMembership
from .models import CompanySetting

def project_switcher(request):
    if not request.user.is_authenticated:
        return {"user_projects": []}

    memberships = ProjectMembership.objects.select_related("project").filter(
        user=request.user,
        project__active=True
    )

    return {
        "user_projects": [m.project for m in memberships]
    }


def company_settings(request):
    return {
        "company_settings": CompanySetting.objects.first()
    }