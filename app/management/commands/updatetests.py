from django.core.management.base import BaseCommand, CommandError
from app.models import Test, Laboratory
import csv

class Command(BaseCommand):
    help = 'add lab test in csv file to databse'

    def handle(self, *args, **options):
        with open('all_lab_tests.csv', newline='') as f:
            reader = csv.DictReader(f)
            total = 0
            for row in reader:
                try:
                    # edit
                    t = Test.objects.get(name=row['name'])
                    t.description = row['description']
                    t.requirements = row['requirements']
                    t.laboratory = Laboratory.objects.get(id=row['laboratory'])
                    t.price = row['price']
                    t.save()
                    self.stdout.write(self.style.SUCCESS(f'---- updated {row["name"]} (id={t.id})'))

                except Test.DoesNotExist:
                    # add
                    t = Test()
                    t.name = row['name']
                    t.description = row['description']
                    t.requirements = row['requirements']
                    t.laboratory = Laboratory.objects.get(id=row['laboratory'])
                    t.price = row['price']
                    t.save()
                    self.stdout.write(self.style.SUCCESS(f'---- added {row["name"]} (id={t.id})'))
                total+=1
        self.stdout.write(self.style.SUCCESS(f'Done. updated {total} tests to db'))