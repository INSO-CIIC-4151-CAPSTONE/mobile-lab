# Generated by Django 4.1.3 on 2022-12-03 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_test_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='description',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='test',
            name='requirements',
            field=models.CharField(max_length=1500),
        ),
    ]