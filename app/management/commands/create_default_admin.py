from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates the default admin account if it doesn't exist"

    def handle(self, *args, **options):
        User = get_user_model()
        exists = User.objects.filter(username=settings.DJANGO_SUPERUSER_USERNAME).exists()

        if exists == True:
            print("Default admin account exists")
        else:
            print("Default admin does not exists")
            print("Adding default admin account")
            User.objects.create_superuser(username=settings.DJANGO_SUPERUSER_USERNAME,
                                          password=settings.DJANGO_SUPERUSER_PASSWORD,
                                          email=settings.DJANGO_SUPERUSER_EMAIL,
                                          first_name=settings.DJANGO_SUPERUSER_FIRST_NAME,
                                          last_name=settings.DJANGO_SUPERUSER_LAST_NAME,
                                          role='ADMIN')
            print("Default admin account added")