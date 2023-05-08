from itertools import groupby

from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from tank.models import TankVolume


@receiver(post_save, sender=TankVolume)
def recalculate_sales_average(sender, instance, created, **kwargs):
    tank_volumes = sender.objects.annotate(
        day=TruncDay('created_at'),
        month=TruncMonth('created_at'),
        year=TruncYear('created_at')).values('id', 'volume', 'created_at').order_by('created_at')
    aggregate_count = sender.objects.annotate(
        day=TruncDay('created_at'),
        month=TruncMonth('created_at'),
        year=TruncYear('created_at')
    ).values('day').annotate(c=Count('id')).filter(c__gt=1).order_by('day')

    single_aggregate_count = sender.objects.annotate(
        day=TruncDay('created_at'),
        month=TruncMonth('created_at'),
        year=TruncYear('created_at')
    ).values('day').annotate(c=Count('id')).filter(c__lt=2).order_by('day')

    aggregated_volumes_by_date = groupby(tank_volumes, key=lambda x: (x['created_at'].strftime("%d %m %Y")))

    combined = []
    test = []
    for _, volume_agg in aggregated_volumes_by_date:
        tupled_volume = list(volume_agg)
        length_tupled = len(tupled_volume)

        combined = list(zip(tupled_volume, tupled_volume[1:]))
        if not combined:
            combined.append(tupled_volume)
            test = tupled_volume

        if len(combined[0]) >= 2:
            for first_volume, second_volume in combined:
                difference = 0
                if first_volume['volume'] < second_volume['volume']:
                    difference = second_volume['volume'] - first_volume['volume']
                print(difference)
            combined = []
"""
- retrieve all tank volumes related to a Tank.
- the tank volumes are separated by week, 1st, 8th, 15th etc
- verify the tank valume per day, if there is more then one value for the specific day, verify the lastest value is > 
than the previous value. If so, calculate the difference, otherwise, assign 0.
- if there was only 1 value for one specific day, pick the value from the previous day.
- if there is more than 2 values for a day, calculate the difference of each of the values.
- save the average of the past 5 weeks
"""