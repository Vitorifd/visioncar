from django.db import models


class Owner(models.Model):
  first_name = models.CharField(max_length=20, verbose_name='Nome')
  last_name = models.CharField(max_length=20, verbose_name='Sobrenome')
  email = models.EmailField(max_length=60, verbose_name='Email')
  instituition = models.CharField(max_length=50, verbose_name='Instituição')

  class Meta:
    verbose_name = 'Dono'
    verbose_name_plural = 'Donos'

  def __str__(self):
    return self.first_name

  def get_full_name(self):
    return self.first_name + ' ' + self.last_name

  def get_status(self):
    log = Log.objects.filter(car__owner=self.id, departure_time=None)

    if len(log) == 0:
      return 'Não'
    else:
      return 'Sim'

  get_full_name.short_description = 'Nome completo'
  get_status.short_description = 'Está no local?'


class Car(models.Model):
  car_plate = models.CharField(max_length=7, verbose_name='Placa')
  owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='Dono')
  color = models.CharField(max_length=30, blank=False, verbose_name='Cor')
  description = models.TextField(max_length=10000, blank=False, verbose_name='Descrição')

  class Meta:
    verbose_name = 'Carro'
    verbose_name_plural = 'Carros'

  def __str__(self):
    return self.car_plate

  def get_owner(self):
    return self.owner.first_name

  def get_instituition(self):
    return self.owner.instituition

  def get_status(self):
    log = Log.objects.filter(car=self.id, departure_time=None)

    if len(log) == 0:
      return 'Não'
    else:
      return 'Sim'

  get_owner.short_description = 'Dono'
  get_instituition.short_description = 'Instituição'
  get_status.short_description = 'Está no local?'


class Log(models.Model):
  entry_time = models.DateTimeField(verbose_name='Horário de entrada')
  departure_time = models.DateTimeField(verbose_name='Horário de saída', blank=True, null=True)
  car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Carro')

  class Meta:
    verbose_name = 'Registro'
    verbose_name_plural = 'Registros'

  def __str__(self):
    return self.get_owner() + ' - ' + self.car.car_plate

  def get_owner(self):
    return self.car.owner.first_name

  def get_instituition(self):
    return self.car.get_instituition()

  get_owner.short_description = 'Dono'
  get_instituition.short_description = 'Instituição'
