import os
from itertools import cycle
from datetime import datetime

from model_bakery.recipe import Recipe

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dash_fuel_application.settings')
from django import setup

setup()

from tank.signals import AverageSalesCalculator
from tank.models import TankVolume, Tank, AverageSales


def create_tank_volume(quantity: int = 12):
    tank = Recipe(Tank).make()
    volumes = (10, 20, 8, 25, 30, 45, 23, 35, 60)
    dates = (
        datetime(2023, 1, 1),
        datetime(2023, 1, 8),
        datetime(2023, 1, 15),
        datetime(2023, 1, 22),
        datetime(2023, 1, 29),
        datetime(2023, 2, 5),
    )
    return Recipe(
        TankVolume, tank=tank, volume=cycle(volumes), created_at=cycle(dates)
    ).make(_quantity=quantity)


def tear_down():
    TankVolume.objects.all().delete()
    AverageSales.objects.all().delete()
    Tank.objects.all().delete()


def test_get_max_date_from_db():
    create_tank_volume()
    avg_calculator = AverageSalesCalculator()
    max_date = avg_calculator.get_max_date(datetime.now())

    actual = TankVolume.objects.latest('created_at').created_at
    assert max_date == actual

    tear_down()


def test_get_max_date_from_param():
    avg_calculator = AverageSalesCalculator()
    dt = datetime.now()
    max_date = avg_calculator.get_max_date(dt)
    assert max_date == dt


def test_create_past_weeks():
    avg_calculator = AverageSalesCalculator()
    date = datetime(2023, 1, 29)
    past_weeks_days = (29, 22, 15, 8, 1)
    past_weeks = avg_calculator.create_past_weeks(date, end=5)

    assert all(date.day in past_weeks_days for date in past_weeks)


def test_calculate_difference():
    avg_calculator = AverageSalesCalculator()
    combined_aggregations = [
        ({'volume': 10}, {'volume': 20}),
        ({'volume': 50}, {'volume': 20}),
    ]
    avg_calculator.calculate_difference(combined_aggregations)
    assert len(avg_calculator.sales) == 2
    assert avg_calculator.sales[0] == 10
    assert avg_calculator.sales[1] == 0
