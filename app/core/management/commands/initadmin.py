from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        account = get_user_model()
        if account.objects.count() == 0:
            email = os.environ.get('ADMIN_USER')
            password = os.environ.get('ADMIN_PASS')
            admin = account.objects.create_superuser(email=email, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('admin accounts can only be initialized if no accounts exist')