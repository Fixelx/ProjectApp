from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserAddForm, RoleForm
from .models import Role, UserProfile
from .tables import UserTable, ArchivedUserTable, RoleTable
from django_tables2 import RequestConfig


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    pass


@login_required
@permission_required("users_view")
def overview(request):

    users = (
        User.objects
        .filter(is_active=True)
        .select_related(
            "profile",
            "profile__role"
        )
        .order_by("username")
    )

    archived_users = (
        User.objects
        .filter(is_active=False)
        .select_related(
            "profile",
            "profile__role"
        )
        .order_by("username")
    )

    roles = list(
        Role.objects.order_by("name")
    )


    # ==================================================
    # ROLE PERMISSIONS FÜR CHECKBOXEN
    # ==================================================

    permission_fields = []

    for field in Role._meta.fields:

        if field.get_internal_type() == "BooleanField":

            permission_fields.append({
                "name": field.name,
                "verbose_name": field.verbose_name or field.name
            })


    for role in roles:

        role.permissions = []

        for permission in permission_fields:

            role.permissions.append({

                "name": permission["name"],

                "verbose_name": permission["verbose_name"],

                "value": getattr(
                    role,
                    permission["name"]
                )

            })


    # ==================================================
    # USER ROLLEN-PERMISSIONS
    # ==================================================

    for user in list(users) + list(archived_users):

        role = getattr(
            getattr(user, "profile", None),
            "role",
            None
        )

        user.role_permissions = []

        if role:

            for permission in permission_fields:

                if getattr(
                    role,
                    permission["name"]
                ):
                    user.role_permissions.append(
                        permission["verbose_name"]
                    )


    # ==================================================
    # TABLES
    # ==================================================
    table = UserTable(users)
    table.roles = roles
    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    archived_table = ArchivedUserTable(archived_users)
    archived_table.roles = roles
    RequestConfig(
        request,
        paginate=False
    ).configure(archived_table)


    role_table = RoleTable(roles)
    role_table.roles = roles
    RequestConfig(
        request,
        paginate=False
    ).configure(role_table)


    return render(
        request,
        "accounts/overview.html",
        {
            "table": table,
            "archived_table": archived_table,
            "role_table": role_table,
        }
    )

@login_required
@permission_required("users_edit")
def user_edit(request, user_id):

    user = get_object_or_404(
        User.objects.select_related(
            "profile"
        ),
        id=user_id
    )

    if user.is_superuser:
        return redirect("accounts:overview")

    if request.method != "POST":
        return redirect("accounts:overview")

    # -------------------------
    # USER
    # -------------------------
    user.username = request.POST.get(
        "username",
        user.username
    )

    user.first_name = request.POST.get(
        "first_name",
        user.first_name
    )

    user.last_name = request.POST.get(
        "last_name",
        user.last_name
    )

    user.email = request.POST.get(
        "email",
        user.email
    )

    user.save()

    # -------------------------
    # PROFILE / ROLE
    # -------------------------
    profile, _ = UserProfile.objects.get_or_create(
        user=user
    )

    role_id = request.POST.get("role")

    if role_id:
        profile.role_id = role_id
    else:
        profile.role = None

    profile.save()

    return redirect(
        "accounts:overview"
    )



@login_required
@permission_required("users_archive")
def user_archive(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user.is_superuser:
        return redirect("accounts:overview")

    if request.method == "POST":
        user.is_active = False
        user.save()

    return redirect("accounts:overview")


@login_required
@permission_required("users_activate")
def user_reactivate(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user.is_superuser:
        return redirect("accounts:overview")

    if request.method == "POST":
        user.is_active = True
        user.save()

    return redirect("accounts:overview")





@login_required
@permission_required("users_add")
def user_add(request):

    form = UserAddForm(
        request.POST or None
    )

    if form.is_valid():

        user = form.save(commit=False)

        password = form.cleaned_data["password"]

        user.set_password(password)
        user.save()

        UserProfile.objects.create(
            user=user,
            role=form.cleaned_data["role"]
        )

        return redirect(
            "accounts:overview"
        )

    return render(
        request,
        "accounts/add.html",
        {
            "form": form
        }
    )






def get_role_permissions():

    fields = []

    for field in Role._meta.fields:

        if field.get_internal_type() == "BooleanField":

            fields.append({
                "name": field.name,
                "label": field.verbose_name or field.name
            })

    return fields



@login_required
@permission_required("users_groups_edit")
def role_edit(request, role_id):

    role = get_object_or_404(
        Role,
        id=role_id
    )


    if request.method == "POST":

        for field in Role._meta.fields:

            if (
                field.get_internal_type()
                == "BooleanField"
            ):

                setattr(
                    role,
                    field.name,
                    field.name in request.POST
                )


        role.name = request.POST.get(
            "name",
            role.name
        )


        role.save()


    return redirect(
        "accounts:overview"
    )


@login_required
@permission_required("users_groups_delete")
def role_delete(request, role_id):

    role = get_object_or_404(
        Role,
        id=role_id
    )


    if request.method == "POST":

        role.delete()


    return redirect(
        "accounts:overview"
    )


@login_required
@permission_required("users_groups_add")
def role_add(request):

    if request.method == "POST":

        form = RoleForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "accounts:overview"
            )

    else:

        form = RoleForm()


    return render(
        request,
        "accounts/role_add.html",
        {
            "form": form
        }
    )