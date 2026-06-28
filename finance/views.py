from django.contrib.auth.decorators import login_required
from accounts.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncDay
from django.db.models import Sum
from datetime import date, datetime, timedelta
from projects.models import ProjectMembership
from .models import Income, Expense
import csv
from django.http import HttpResponse
from calendar import monthrange
from .forms import IncomeForm, ExpenseForm
from .tables import PeriodAnalyticsTable, FinanceTransactionTable
import json
from inventory.models import ShoppingItem

# =========================================================
# OVERVIEW
# =========================================================
@login_required
@permission_required("projects_finance_view")
def finance_overview(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    # -------------------------
    # DATE FILTER (for KPI ONLY)
    # -------------------------
    start = request.GET.get("start")
    end = request.GET.get("end")

    if not start or not end:
        start_date = end_date = date.today()
    else:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()

    # -------------------------
    # KPI DATA (FILTERED)
    # -------------------------
    filtered_incomes = Income.objects.filter(
        project=project,
        date__date__range=[start_date, end_date]
    )

    filtered_expenses = Expense.objects.filter(
        project=project,
        date__date__range=[start_date, end_date]
    )

    total_income = sum(i.amount for i in filtered_incomes)
    total_expense = sum(e.amount for e in filtered_expenses)
    total_profit = total_income - total_expense

    incomes = Income.objects.filter(
        project=project,
        date__date__range=[start_date, end_date]
    ).order_by("-date")

    expenses = Expense.objects.filter(
        project=project,
        date__date__range=[start_date, end_date]
    ).order_by("-date")

    # -------------------------
    # PERIOD VIEW
    # -------------------------
    period = request.GET.get("period", "year")

    if period == "year":
        trunc = TruncYear("date")
    elif period == "week":
        trunc = TruncWeek("date")
    elif period == "day":
        trunc = TruncDay("date")
    else:
        trunc = TruncMonth("date")

    income_stats = (
        Income.objects.filter(project=project)
        .annotate(period_key=trunc)
        .values("period_key")
        .annotate(total=Sum("amount"))
        .order_by("-period_key")
    )

    expense_stats = (
        Expense.objects.filter(project=project)
        .annotate(period_key=trunc)
        .values("period_key")
        .annotate(total=Sum("amount"))
        .order_by("-period_key")
    )

    expense_map = {
        str(e["period_key"]): e["total"]
        for e in expense_stats
    }

    period_data = []
    period_keys = set()
    for i in income_stats:
        period_keys.add(i["period_key"])
    for e in expense_stats:
        period_keys.add(e["period_key"])

    income_map = {
        str(i["period_key"]): i["total"] or 0
        for i in income_stats
    }
    expense_map = {
        str(e["period_key"]): e["total"] or 0
        for e in expense_stats
    }

    for period_start in sorted(period_keys, reverse=True):
        income_total = income_map.get(str(period_start), 0)
        expense_total = expense_map.get(str(period_start), 0)
        if period == "year":
            period_end = period_start.replace(month=12, day=31)
        elif period == "week":
            period_end = period_start + timedelta(days=6)
        elif period == "day":
            period_end = period_start
        else:
            last_day = monthrange(
                period_start.year,
                period_start.month
            )[1]
            period_end = period_start.replace(day=last_day)

        period_data.append({
            "period": period_start,
            "period_start": period_start,
            "period_end": period_end,
            "income": income_total,
            "expense": expense_total,
            "profit": income_total - expense_total,
        })

    # -------------------------
    # RETURN
    # -------------------------

    table = PeriodAnalyticsTable(
        period_data,
        period_type=period,
        request=request,
    )

    return render(request, "finance/overview.html", {
        "project": project,

        # KPI (filtered)
        "total_income": total_income,
        "total_expense": total_expense,
        "total_profit": total_profit,

        # LISTS (all data)
        "incomes": incomes,
        "expenses": expenses,

        # PERIOD
        "period_data": period_data,
        "period": period,

        # UI
        "start_date": start_date,
        "end_date": end_date,

        "table": table,
    })


@login_required
@permission_required("projects_finance_view")
def finance_view(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    start = request.GET.get("start")
    end = request.GET.get("end")

    incomes = Income.objects.filter(project=project)
    expenses = Expense.objects.filter(project=project)

    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            incomes = incomes.filter(date__date__gte=start_date)
            expenses = expenses.filter(date__date__gte=start_date)
        except ValueError:
            pass

    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            incomes = incomes.filter(date__date__lte=end_date)
            expenses = expenses.filter(date__date__lte=end_date)
        except ValueError:
            pass

    # -------------------------
    # MERGED LIST (LIKE EXPORT ORDER)
    # -------------------------
    transactions = []

    for i in incomes:
        transactions.append({
            "type": "Einnahme",
            "date": i.date,
            "amount": i.amount,
            "category": i.category,
            "name": i.name,
            "created_by": i.created_by,
            "note": i.note,
        })

    for e in expenses:
        transactions.append({
            "type": "Ausgabe",
            "date": e.date,
            "amount": e.amount,
            "category": e.category,
            "name": e.name,
            "created_by": e.created_by,
            "note": e.note,
            "supplier": e.supplier,
            "payment_method": e.payment_method,
            "receipt": e.receipt,
        })

    transactions.sort(
        key=lambda x: x["date"],
        reverse=True,
    )

    table = FinanceTransactionTable(
        transactions,
        request=request,
    )

    return render(
        request,
        "finance/view.html",
        {
            "project": project,
            "table": table,
            "start_date": start_date,
            "end_date": end_date,
        },
    )













# =========================
# INCOME CREATE
# =========================
@login_required
@permission_required("projects_finance_income_add")
def add_income(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    if request.method == "POST":
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.project = project
            income.created_by = request.user
            income.save()
            return redirect("finance:overview", project_id=project.id)

    else:
        form = IncomeForm()

    return render(request, "finance/form.html", {
        "form": form,
        "project": project,
        "type": "income",
    })


# =========================
# EXPENSE CREATE
# =========================
@login_required
@permission_required("projects_finance_expense_add")
def add_expense(request, project_id):

    membership = get_object_or_404(
        ProjectMembership,
        user=request.user,
        project_id=project_id
    )

    project = membership.project

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.created_by = request.user
            expense.save()

            shopping_ids = request.session.pop(
                "shopping_item_ids",
                []
            )

            if shopping_ids:
                ShoppingItem.objects.filter(
                    id__in=shopping_ids,
                    project=project
                ).delete()

            return redirect(
                "finance:overview",
                project_id=project.id
            )

    else:
        initial = request.session.pop(
            "expense_initial",
            {}
        )

        form = ExpenseForm(initial=initial)

    return render(request, "finance/form.html", {
        "form": form,
        "project": project,
        "type": "expense",
    })