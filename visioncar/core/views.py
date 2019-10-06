import datetime
import pytz

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Car, Log


@csrf_exempt
@require_http_methods(["POST"])
def log_create(request, car_plate):

  try:
    car = Car.objects.get(car_plate=car_plate)

    log = Log.objects.filter(car=car.id, departure_time=None)

    if len(log) == 0:
      newLog = Log(car=car, entry_time=getCurrentDatetime())
      newLog.save()

      return JsonResponse({
        'id': newLog.id,
        'entry_time': newLog.entry_time,
        'departure_time': newLog.departure_time,
        'car': newLog.car.car_plate,
      })

    log = log[0]
    log.departure_time = getCurrentDatetime()
    log.save()

    return JsonResponse({
      'id': log.id,
      'entry_time': log.entry_time,
      'departure_time': log.departure_time,
      'car': log.car.car_plate,
    })

  except Car.DoesNotExist:
    return JsonResponse({ 'error': True })


timezone = pytz.timezone('America/Campo_Grande')

def getCurrentDatetime():
  return datetime.datetime.now(tz=timezone)
