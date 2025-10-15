from django.core.management.base import BaseCommand

from ...models import Person
from faker import Faker


class Command(BaseCommand):
    help = "Update contracts item count"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Person.objects.all().delete()
        fake = Faker()

        for _ in range(100):
            person = Person.objects.create(
                name=fake.name(),
                date_of_birth=fake.date_of_birth(),
                email=fake.email(),
                street_address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
            )
