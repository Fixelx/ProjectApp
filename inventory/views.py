from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from projects.models import ProjectMembership
from .models import InventoryItem, InventoryCategory, InventoryLocation, ProjectInventoryItem, ShoppingItem, Category, Supplier
from django.contrib.auth.models import User
from .forms import InventoryItemForm, ShoppingItemForm
from django.db.models import Sum, Value, F
from django_tables2 import RequestConfig
from .tables import ProjectInventoryItemTable, ShoppingItemTable, InventoryAddTable, InventoryGlobalTable
from django.db.models.functions import Coalesce

@login_required
@permission_required("projects_inventory_inventory_view")
def inventory_overview(request, project_id):
    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    items = (
        ProjectInventoryItem.objects
        .select_related(
            "item",
            "item__category",
            "item__location",
            "item__responsible",
        )
        .filter(project=project)
        .order_by("item__name")
    )

    table = ProjectInventoryItemTable(items)

    # Zusatzdaten für TemplateColumns
    table.project = project

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    shopping_items = (
        ShoppingItem.objects
        .select_related(
            "category",
            "supplier"
        )
        .filter(project=project)
        .order_by("name")
    )


    shopping_table = ShoppingItemTable(shopping_items)

    shopping_table.project = project
    shopping_table.categories = Category.objects.order_by("name")
    shopping_table.suppliers = Supplier.objects.order_by("name")

    return render(request, "inventory/overview.html", {
        "project": project,
        "table": table,
        "shopping_table": shopping_table,
    })


@login_required
@permission_required("projects_inventory_shopping_add")
def shopping_add(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    if request.method == "POST":

        form = ShoppingItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.project = project
            item.save()
            return redirect(
                "inventory:overview",
                project_id=project.id
            )

    else:

        form = ShoppingItemForm()

    return render(
        request,
        "inventory/shopping_add.html",
        {
            "project": project,
            "form": form,
        }
    )


@login_required
@permission_required("projects_inventory_inventory_add")
def inventory_add(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    items = (
        InventoryItem.objects
        .select_related(
            "category",
            "location"
        )
        .annotate(
            used_quantity=Coalesce(
                Sum("projectinventoryitem__quantity"),
                Value(0)
            )
        )
        .annotate(
            available_quantity=F("quantity") - F("used_quantity")
        )
        .filter(
            available_quantity__gt=0
        )
        .order_by("name")
    )

    if request.method == "POST":

        for item in items:

            quantity = request.POST.get(
                f"item_{item.id}"
            )

            if not quantity:
                continue

            quantity = int(quantity)

            if quantity <= 0:
                continue

            if quantity > item.available_quantity:
                continue

            project_item, created = ProjectInventoryItem.objects.get_or_create(
                project=project,
                item=item,
                defaults={
                    "quantity": quantity,
                    "status": ProjectInventoryItem.Status.OPEN,
                }
            )

            if not created:
                project_item.quantity += quantity
                project_item.save()

        return redirect(
            "inventory:overview",
            project_id=project.id
        )

    table = InventoryAddTable(items)

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "inventory/add.html",
        {
            "project": project,
            "table": table,
        }
    )






@login_required
@permission_required("inventory_view")
def inventory_global_overview(request):

    items = (
        InventoryItem.objects
        .select_related(
            "category",
            "location",
            "responsible"
        )
        .annotate(
            used_quantity=Coalesce(
                Sum("projectinventoryitem__quantity"),
                Value(0)
            )
        )
        .annotate(
            available_quantity=F("quantity") - F("used_quantity")
        )
        .order_by("name")
    )

    for item in items:

        used_quantity = (
            ProjectInventoryItem.objects
            .filter(item=item)
            .aggregate(total=Sum("quantity"))
            .get("total") or 0
        )

        item.available_quantity = max(
            0,
            item.quantity - used_quantity
        )

    table = InventoryGlobalTable(items)

    table.categories = InventoryCategory.objects.all()
    table.locations = InventoryLocation.objects.all()
    table.users = User.objects.order_by("username")

    RequestConfig(
        request,
        paginate=False
    ).configure(table)

    return render(
        request,
        "inventory/global/overview.html",
        {
            "table": table,
        }
    )
    

@login_required
@permission_required("inventory_add")
def inventory_global_add(request):

    if request.method == "POST":
        form = InventoryItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("inventory_global:overview")

    else:
        form = InventoryItemForm()

    return render(request, "inventory/global/add.html", {"form": form,})

















@login_required
@permission_required("projects_inventory_inventory_delete")
def inventory_delete(request, project_id, item_id):
    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)

    item = get_object_or_404(ProjectInventoryItem, id=item_id, project=membership.project)

    if request.method == "POST":
        item.delete()

    return redirect("inventory:overview", project_id=project_id)



@login_required
@permission_required("projects_inventory_shopping_delete")
def shopping_delete(request, project_id, item_id):
    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)

    item = get_object_or_404(ShoppingItem, id=item_id, project=membership.project)

    if request.method == "POST":
        item.delete()

    return redirect("inventory:overview", project_id=project_id)



@login_required
@permission_required("inventory_delete")
def inventory_global_delete(request, item_id):

    item = get_object_or_404(
        InventoryItem,
        id=item_id
    )

    if request.method == "POST":
        item.delete()

    return redirect("inventory_global:overview")










@login_required
@permission_required("projects_inventory_inventory_edit")
def inventory_edit(request, project_id, item_id):
    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
    item = get_object_or_404(ProjectInventoryItem, id=item_id, project=membership.project)
    if request.method == "POST":
        item.quantity = request.POST.get("quantity") or 0
        item.status = request.POST.get("status")
        item.save()
        return redirect("inventory:overview", project_id=project_id)

    return render(
        request,
        "inventory/edit.html",
        {
            "project": membership.project,
            "item": item,
        }
    )












@login_required
@permission_required("projects_inventory_shopping_edit")
def shopping_edit(request, project_id, item_id):
    membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
    item = get_object_or_404(ShoppingItem, id=item_id, project=membership.project)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.description = request.POST.get("description", "")
        item.quantity = request.POST.get("quantity") or 1
        item.price = request.POST.get("price") or None
        item.category_id = request.POST.get("category") or None
        item.supplier_id = request.POST.get("supplier") or None
        item.save()
        return redirect("inventory:overview", project_id=project_id)

    return render(
        request,
        "inventory/shopping_edit.html",
        {
            "project": membership.project,
            "item": item,
            "categories": Category.objects.all(),
            "suppliers": Supplier.objects.all(),
        }
    )








@login_required
@permission_required("inventory_edit")
def inventory_global_edit(request, item_id):
    item = get_object_or_404(
        InventoryItem,
        id=item_id
    )
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.quantity = request.POST.get("quantity")
        item.article_number = request.POST.get("article_number")
        item.description = request.POST.get("description", "")
        item.category_id = request.POST.get("category") or None
        item.location_id = request.POST.get("location") or None
        item.responsible_id = request.POST.get("responsible") or None
        item.save()
        return redirect("inventory_global:overview")

    return render(
        request,
        "inventory/global/edit.html",
        {
            "item": item,
            "categories": InventoryCategory.objects.all(),
            "locations": InventoryLocation.objects.all(),
            "users": User.objects.order_by("username"),
        }
    )