from django.contrib import admin
from .models import Account, Category, Budget, Transaction

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Transaction)
