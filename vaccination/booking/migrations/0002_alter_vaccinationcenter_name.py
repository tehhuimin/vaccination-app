# Generated by Django 3.2 on 2021-11-11 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationcenter',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]