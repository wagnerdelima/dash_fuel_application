from datetime import datetime
import logging

from django.db import migrations

from tank.models import TankVolume, Tank


def populate_database_initial_data(*args, **kwargs):
    tank, created = Tank.objects.get_or_create(name='Tank 1')
    TankVolume.objects.bulk_create(
        (
            TankVolume(tank=tank, volume=10, created_at=datetime(2023, 1, 1, 10, 0)),
            TankVolume(tank=tank, volume=30, created_at=datetime(2023, 1, 1, 11, 0)),
            TankVolume(tank=tank, volume=45, created_at=datetime(2023, 1, 8, 9, 0)),
            TankVolume(tank=tank, volume=20, created_at=datetime(2023, 1, 8, 13, 0)),
            TankVolume(tank=tank, volume=30, created_at=datetime(2023, 1, 14, 23, 0)),
            TankVolume(tank=tank, volume=60, created_at=datetime(2023, 1, 15, 14, 0)),
            TankVolume(tank=tank, volume=25, created_at=datetime(2023, 1, 22, 10, 0)),
            TankVolume(tank=tank, volume=50, created_at=datetime(2023, 1, 22, 15, 0)),
            TankVolume(tank=tank, volume=70, created_at=datetime(2023, 1, 22, 20, 0)),
            TankVolume(tank=tank, volume=12, created_at=datetime(2023, 1, 29, 10, 30)),
            TankVolume(tank=tank, volume=49, created_at=datetime(2023, 1, 29, 12, 30)),
            TankVolume(tank=tank, volume=12, created_at=datetime(2023, 2, 5, 10, 0)),
            TankVolume(tank=tank, volume=25, created_at=datetime(2023, 2, 5, 12, 0)),
            TankVolume(tank=tank, volume=20, created_at=datetime(2023, 2, 5, 15, 0)),
            TankVolume(tank=tank, volume=42, created_at=datetime(2023, 2, 5, 18, 0)),
        )
    )
    logging.info('Tank and Tank Volume created.')


class Migration(migrations.Migration):
    dependencies = [("tank", "0001_initial")]

    operations = [
        migrations.RunPython(populate_database_initial_data),
    ]
