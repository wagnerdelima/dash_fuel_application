# Generated by Django 4.2.1 on 2023-05-09 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="A valid name for a tank.", max_length=100
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TankVolume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "volume",
                    models.FloatField(
                        default=0, help_text="The volume of the tank at a given moment."
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "tank",
                    models.ForeignKey(
                        help_text="Reference to the tank.",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="tank.tank",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AverageSales",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "avg_sales",
                    models.FloatField(
                        default=0, help_text="The average sales of the past 5 weeks."
                    ),
                ),
                (
                    "calculated_at",
                    models.DateTimeField(
                        help_text="The day the average of 5 previous weeks was calculated."
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "tank",
                    models.ForeignKey(
                        help_text="Reference to the tank.",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="tank.tank",
                    ),
                ),
            ],
        ),
    ]
