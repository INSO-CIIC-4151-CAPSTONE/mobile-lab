from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates a technician user if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Technician's username", required=True)
        parser.add_argument('--email', help="Technician's email", required=True)
        parser.add_argument('--password', help="Technician's password", required=True)

    def handle(self, *args, **options):
        User = get_user_model()
        exists = User.objects.filter(username=options['username']).exists()

        if exists == True:
            print("Username already taken")
        else:
            print("Adding technician account")
            User.objects.create_superuser(username=options['username'],
                                          email=options['email'],
                                          password=options['password'],
                                          role='TECHNICIAN')
            print("Technician account added")