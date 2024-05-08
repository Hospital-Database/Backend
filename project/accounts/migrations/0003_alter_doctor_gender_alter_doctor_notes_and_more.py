# Generated by Django 5.0.3 on 2024-05-08 14:46

import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_doctor_address_alter_doctor_phone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="gender",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="gender",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="blood_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="code",
            field=shortuuidfield.fields.ShortUUIDField(
                blank=True, editable=False, max_length=22, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="disease_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="gender",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]