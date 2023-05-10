from django.contrib import admin

from tank.models import Tank, TankVolume, AverageSales


@admin.register(AverageSales)
class AverageAdmin(admin.ModelAdmin):
    list_display = (
        'tank',
        'avg_sales',
        'calculated_at',
    )


@admin.register(TankVolume)
class AverageAdmin(admin.ModelAdmin):
    list_display = ('tank', 'volume', 'created_at', 'updated_at')


# Register your models here.
admin.site.register(Tank)
