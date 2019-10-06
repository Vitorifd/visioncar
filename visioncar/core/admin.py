from django.contrib import admin

from .models import Owner, Car, Log


class CarInline(admin.StackedInline):
  model = Car
  extra = 1


class OwnerAdmin(admin.ModelAdmin):
  list_display = ('get_full_name', 'email', 'instituition', 'get_status')
  fields = ('first_name', 'last_name', 'email', 'instituition')
  inlines = [CarInline]
  search_fields = (
    'first_name',
    'last_name',
    'email',
    'instituition'
  )


class CarAdmin(admin.ModelAdmin):
  list_display = ('car_plate', 'get_owner', 'color', 'description', 'get_instituition', 'get_status')
  search_fields = (
    'owner__first_name',
    'owner__instituition',
    'car_plate',
    'color'
  )


class LogAdmin(admin.ModelAdmin):
  list_display = ('entry_time', 'departure_time', 'car', 'get_owner', 'get_instituition')
  search_fields = (
    'car__owner__first_name',
    'car__owner__instituition',
    'car__car_plate',
    'entry_time',
    'departure_time'
  )


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Log, LogAdmin)
