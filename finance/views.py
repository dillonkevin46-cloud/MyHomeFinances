from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from .models import Transaction, Budget, Account
from .forms import TransactionForm
import json
from decimal import Decimal

def calculate_rollover(month, year):
    """
    Calculates the difference between the Budget limit (plus previous rollover)
    and actual spending for a month.
    """
    try:
        budget = Budget.objects.get(month=month, year=year)
        limit = budget.limit_amount
        rollover = budget.rollover_amount

        # Calculate total expenses for that month
        total_expenses = Transaction.objects.filter(
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)

        balance = (limit + rollover) - total_expenses
        return balance
    except Budget.DoesNotExist:
        return Decimal(0)

def dashboard(request):
    now = timezone.now()
    # allow filtering by month/year from query params
    try:
        month = int(request.GET.get('month', now.month))
        year = int(request.GET.get('year', now.year))
    except ValueError:
        month = now.month
        year = now.year

    account_filter = request.GET.get('account')

    # get budget
    budget = Budget.objects.filter(month=month, year=year).first()
    limit_amount = budget.limit_amount if budget else Decimal(0)
    rollover_amount = budget.rollover_amount if budget else Decimal(0)
    total_budget = limit_amount + rollover_amount

    # Global transactions (for global remaining calculation)
    all_transactions = Transaction.objects.filter(date__month=month, date__year=year)
    global_expenses = all_transactions.aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
    global_remaining = total_budget - global_expenses

    # Filtered transactions
    transactions = all_transactions.order_by('-date')
    if account_filter and account_filter != 'All':
        transactions = transactions.filter(account__name=account_filter)

    # Calculate totals for the view
    total_expenses = transactions.aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
    unexpected_expenses = transactions.filter(is_unexpected=True).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)

    # Remaining to show:
    # If filtered, we show the global remaining because budget is shared.
    # But we could also show "Available for this person" if we had per-person budgets.
    # Let's stick to displaying Global Remaining but labeling it clearly if needed.
    # Actually, the user wants "individual views".
    # I'll pass 'global_remaining' as 'remaining'.

    # For charts
    # Budget vs Actual
    # If filtered, we show Filtered Expenses vs Total Budget?
    # Or keep it Global?
    # Let's make the chart reflect the current view's expenses against the total budget.
    remaining_budget_after_filtered = max(total_budget - total_expenses, 0)
    # Wait, "Budget vs Actual" chart usually fills up.
    # If I spent 100 out of 1000. Chart shows 100 spent, 900 remaining.
    # If I filter to "Me" (spent 20), chart shows 20 spent, 980 remaining?
    # That implies 980 is available, but actually only 900 is available globally.
    # This is tricky.
    # Let's just show "My Spending" vs "Total Budget".
    # The "Remaining" part of the doughnut should probably be "Total Budget - My Spending" or "Global Remaining"?
    # If I use "Global Remaining", the chart might have 3 segments: "My Spending", "Others Spending", "Remaining".
    # That would be cool.
    # But for simplicity, let's just stick to:
    # Doughnut: [Remaining Budget (Global), Expenses (Filtered)] -> This misrepresents if others spent money.

    # Let's stick to Global Budget vs Global Actual for the chart, even in individual view,
    # OR change the chart to "Expense Breakdown by Owner" which is more relevant for individual view (it becomes 100% one color).

    # Let's keep the "Budget vs Actual" as GLOBAL context, even when filtered.
    # And "Total Expenses" card shows FILTERED amount.
    # And "Transactions" list shows FILTERED list.

    budget_vs_actual_data = {
        'labels': ['Remaining Budget', 'Global Expenses'],
        'data': [float(max(global_remaining, 0)), float(global_expenses)]
    }

    # Expense Breakdown by Owner (Global context is better here too to see comparison)
    owner_expenses = all_transactions.values('account__name').annotate(total=Sum('amount'))
    owner_labels = [item['account__name'] for item in owner_expenses]
    owner_data = [float(item['total']) for item in owner_expenses]

    # If we want the charts to update based on filter...
    # Maybe "Budget vs Actual" should be: [Global Remaining, My Expenses, Other Expenses] ?
    # Let's stick to Global for the charts to avoid confusion,
    # BUT the "Total Expenses" card will reflect the filter.

    context = {
        'month': month,
        'year': year,
        'budget': budget,
        'total_budget': total_budget,
        'total_expenses': total_expenses, # Filtered
        'unexpected_expenses': unexpected_expenses, # Filtered
        'remaining': global_remaining, # Global
        'transactions': transactions, # Filtered
        'account_filter': account_filter,
        'accounts': Account.objects.all(),
        'budget_vs_actual_json': json.dumps(budget_vs_actual_data),
        'owner_data_json': json.dumps({'labels': owner_labels, 'data': owner_data}),
    }
    return render(request, 'finance/dashboard.html', context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(initial={'date': timezone.now().date()})

    return render(request, 'finance/add_transaction.html', {'form': form})
