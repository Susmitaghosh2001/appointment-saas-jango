from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Create a default super admin account'

    def handle(self, *args, **options):
        email = 'admin@example.com'
        password = 'Admin@123'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Super admin already exists: {email}'))
            return

        User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            role='super_admin',
            is_superuser=True,
            is_staff=True,
        )

        self.stdout.write(self.style.SUCCESS(f'Super admin created: {email} / {password}'))
