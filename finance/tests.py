from django.test import TestCase, Client
from django.urls import reverse
from .models import Account, Category, Budget, Transaction
from decimal import Decimal
from django.utils import timezone

class FinanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.joint = Account.objects.create(name='Joint')
        self.husband = Account.objects.create(name='Husband')
        self.category = Category.objects.create(name='Groceries')
        self.budget = Budget.objects.create(
            month=timezone.now().month,
            year=timezone.now().year,
            limit_amount=Decimal('1000.00'),
            rollover_amount=Decimal('0.00')
        )
        self.t1 = Transaction.objects.create(
            date=timezone.now(),
            amount=Decimal('100.00'),
            description='Joint Transaction',
            category=self.category,
            account=self.joint,
            is_unexpected=False
        )
        self.t2 = Transaction.objects.create(
            date=timezone.now(),
            amount=Decimal('50.00'),
            description='Husband Transaction',
            category=self.category,
            account=self.husband,
            is_unexpected=False
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Joint Transaction')
        self.assertContains(response, 'Husband Transaction')
        # Total expenses should be 150
        self.assertEqual(response.context['total_expenses'], Decimal('150.00'))

    def test_dashboard_filtering(self):
        # Filter by Husband
        response = self.client.get(reverse('dashboard') + '?account=Husband')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Husband Transaction')
        self.assertNotContains(response, 'Joint Transaction')
        # Filtered expenses should be 50
        self.assertEqual(response.context['total_expenses'], Decimal('50.00'))
        # Global remaining should still be 1000 - 150 = 850
        self.assertEqual(response.context['remaining'], Decimal('850.00'))

    def test_add_transaction_view(self):
        response = self.client.get(reverse('add_transaction'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('add_transaction'), {
            'date': timezone.now().date(),
            'amount': '25.00',
            'description': 'New Transaction',
            'category': self.category.id,
            'account': self.joint.id,
            'is_unexpected': False
        })
        self.assertEqual(response.status_code, 302) # Redirects to dashboard
        self.assertEqual(Transaction.objects.count(), 3)
