from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Setup site for django.contrib.sites'

    def handle(self, *args, **kwargs):
        try:
            site, created = Site.objects.get_or_create(
                id=1,  # Using SITE_ID = 1
                defaults={
                    'domain': 'easydsapro.onrender.com',
                    'name': 'EasyDSA Pro'
                }
            )
            if not created:
                site.domain = 'easydsapro.onrender.com'
                site.name = 'EasyDSA Pro'
                site.save()
            
            self.stdout.write(self.style.SUCCESS(f'✓ Site configured: {site.domain}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))