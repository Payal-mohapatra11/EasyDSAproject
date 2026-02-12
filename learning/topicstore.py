from django.core.management.base import BaseCommand
from learning.models import Topic

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        topics = [
            {"name": "Array", },
            {"name": "Linkedlist", },
            {"name": "Stack", },
            {"name": "Queue", },
            {"name": "Tree"},
            {"name": "Graph"},
            {"name": "Sorting"},
            {"name": "Searching"},
        ]

        for topic in topics:
            Topic.objects.get_or_create(**topic)

        self.stdout.write(self.style.SUCCESS("Topics added successfully!"))
