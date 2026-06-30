from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='минуты')
    price = models.PositiveIntegerField()
    icon = models.CharField(max_length=10, default='✂️')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Master(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='masters/', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('done', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер')
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    client_phone = models.CharField(max_length=20, verbose_name='Телефон')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} — {self.service} ({self.date} {self.time})"

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']
