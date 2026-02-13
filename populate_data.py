import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyFinance.settings')
django.setup()

from finance.models import Account, Category, Budget, Transaction
from django.utils import timezone
from decimal import Decimal

def populate():
    print("Populating data...")
    
    # Accounts
    husband, _ = Account.objects.get_or_create(name='Husband')
    wife, _ = Account.objects.get_or_create(name='Wife')
    joint, _ = Account.objects.get_or_create(name='Joint')
    
    # Categories
    groceries, _ = Category.objects.get_or_create(name='Groceries')
    rent, _ = Category.objects.get_or_create(name='Rent')
    entertainment, _ = Category.objects.get_or_create(name='Entertainment')
    unexpected, _ = Category.objects.get_or_create(name='Unexpected')
    
    # Budget
    now = timezone.now()
    budget, _ = Budget.objects.get_or_create(
        month=now.month, 
        year=now.year,
        defaults={'limit_amount': Decimal('5000.00'), 'rollover_amount': Decimal('0.00')}
    )
    
    # Clear existing transactions for clean slate?
    # Transaction.objects.all().delete()
    
    print("Data populated.")

if __name__ == '__main__':
    populate()
