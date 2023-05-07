from django.db.models import (
    Model,
    CharField,
    FloatField,
    DateTimeField,
    ForeignKey,
    DO_NOTHING,
)


class Tank(Model):
    name = CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='A valid name for a tank.',
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TankVolume(Model):
    tank_id = ForeignKey(
        Tank,
        null=False,
        blank=False,
        on_delete=DO_NOTHING,
        help_text='Reference to the tank.'
    )
    volume = FloatField(
        null=False,
        default=0,
        help_text='The volume of the tank at a given moment.'
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f'Volume {self.volume}'


class AverageSales(Model):
    tank_id = ForeignKey(
        Tank,
        null=False,
        blank=False,
        on_delete=DO_NOTHING,
        help_text='Reference to the tank.'
    )

    avg_sales = FloatField(
        null=False,
        default=0,
        help_text='The average sales of the past 5 weeks.'
    )

    calculated_at = DateTimeField(
        help_text='The day the average of 5 previous weeks was calculated.'
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
