# Generated by Django 5.1.2 on 2024-10-27 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_medicine_prescriptions_prescription_medicines'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medicines',
        ),
        migrations.AddField(
            model_name='medicine',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.prescription'),
        ),
    ]
