# Generated by Django 4.2.17 on 2024-12-09 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enumeration", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="counter",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="gap",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="sequence",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
