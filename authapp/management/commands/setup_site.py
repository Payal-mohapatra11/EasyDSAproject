from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Setup site for django.contrib.sites'

    def handle(self, *args, **kwargs):
        site, created = Site.objects.update_or_create(
            domain='easydsapro.onrender.com',
            defaults={
                'name': 'EasyDSA Pro'
            }
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Site configured: {site.domain} (ID={site.id})')
        )