# Generated by Django 3.2 on 2021-11-12 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_vaccinationcenter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='time_slot',
            field=models.IntegerField(choices=[('10:00 - 11:00', 'Am10 Am11'), ('11:00 - 12:00', 'Am11 Pm12'), ('12:00 - 13:00', 'Pm12 Pm01'), ('13:00 - 14:00', 'Pm01 Pm02'), ('14:00 - 15:00', 'Pm02 Pm03'), ('15:00 - 16:00', 'Pm03 Pm04'), ('16:00 - 17:00', 'Pm04 Pm05'), ('17:00 - 18:00', 'Pm05 Pm06')], default='10:00 - 11:00'),
        ),
        migrations.AlterField(
            model_name='nurseavailability',
            name='time_slot',
            field=models.IntegerField(choices=[('10:00 - 11:00', 'Am10 Am11'), ('11:00 - 12:00', 'Am11 Pm12'), ('12:00 - 13:00', 'Pm12 Pm01'), ('13:00 - 14:00', 'Pm01 Pm02'), ('14:00 - 15:00', 'Pm02 Pm03'), ('15:00 - 16:00', 'Pm03 Pm04'), ('16:00 - 17:00', 'Pm04 Pm05'), ('17:00 - 18:00', 'Pm05 Pm06')], default='10:00 - 11:00'),
        ),
    ]
