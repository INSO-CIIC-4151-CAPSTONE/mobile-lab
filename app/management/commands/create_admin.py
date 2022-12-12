from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username", required=True)
        parser.add_argument('--email', help="Admin's email", required=True)
        parser.add_argument('--password', help="Admin's password", required=True)

    def handle(self, *args, **options):
        User = get_user_model()
        exists = User.objects.filter(username=options['username']).exists()

        if exists == True:
            print("Admin account exists")
        else:
            print("Adding admin account")
            User.objects.create_superuser(username=options['username'],
                                          email=options['email'],
                                          password=options['password'],
                                          role='ADMIN')
            print("Admin account added")