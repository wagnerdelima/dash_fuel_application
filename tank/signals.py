from itertools import groupby
from datetime import datetime, timedelta

from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from tank.models import TankVolume, AverageSales


class AverageSalesCalculator:
    def __init__(self):
        self.sales = []

    def calculate_sales_average(self, sender, instance) -> None:
        dates = self.create_week_days()
        last_aggregated_date = dates[-1]
        next_date_index = 1
        max_date = TankVolume.objects.latest('created_at').created_at
        two_pairs = 4
        while last_aggregated_date.date() < max_date.date():
            last_aggregated_date = dates[-1]
            tank_volumes = sender.objects.annotate(
                day=TruncDay('created_at'),
                month=TruncMonth('created_at'),
                year=TruncYear('created_at')
            ).filter(
                tank=instance.tank.id,
                created_at__gte=dates[0].strftime('%Y-%m-%d'),
                created_at__lte=(last_aggregated_date + timedelta(days=1)).strftime('%Y-%m-%d')
            ).values('id', 'volume', 'created_at').order_by('created_at')
            aggregated_volumes_by_date = groupby(tank_volumes, key=lambda x: (x['created_at'].strftime("%d %m %Y")))

            single_agg = []
            for _, volume_agg in aggregated_volumes_by_date:
                list_volume = list(volume_agg)
                combined = list(zip(list_volume, list_volume[1:])) if len(list_volume) != two_pairs else zip(
                    list_volume[::2], list_volume[1::2])

                if not combined:
                    single_agg.extend(list_volume)
                    continue

                if single_agg:
                    self.calculate_difference(list(zip(single_agg, single_agg[1:])))
                    single_agg = []

                self.calculate_difference(combined)

            if self.sales:
                self.save_average_sales(instance.tank, last_aggregated_date)
            # update 5-week date range

            dates = self.create_week_days(day=dates[next_date_index].day)
            next_date_index += 1

    def create_week_days(self, start: int = 1, end: int = 5, year: int = 2023, month: int = 1, day: int = 1):
        base = timezone.datetime(year, month, day, tzinfo=timezone.utc)
        days = [base]
        for x in range(start, end):
            base += timedelta(days=7)
            days.append(base)
        return days

    def calculate_difference(self, combined_aggregation):
        for first_volume, second_volume in combined_aggregation:
            delta = 0
            if first_volume['volume'] < second_volume['volume']:
                delta = second_volume['volume'] - first_volume['volume']
            print(delta)
            self.sales.append(delta)

    def save_average_sales(self, tank: int, date):
        avg_sales = sum(self.sales) / len(self.sales)
        try:
            avg_sales_obj = AverageSales.objects.get(tank=tank, calculated_at=date)
            avg_sales_obj.avg_sales = avg_sales
            avg_sales_obj.save()
        except AverageSales.DoesNotExist:
            AverageSales.objects.create(tank=tank, avg_sales=avg_sales, calculated_at=date)
        self.sales = []


@receiver(post_delete, sender=TankVolume)
@receiver(post_save, sender=TankVolume)
def recalculate_sales_average(sender, instance, **kwargs):
    sales = AverageSalesCalculator()
    sales.calculate_sales_average(sender, instance)
