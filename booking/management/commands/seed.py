from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import Service, Master, Appointment
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Заполнить базу тестовыми данными'

    def handle(self, *args, **options):
        # Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Создан admin/admin')

        # Services
        services_data = [
            ('Стрижка мужская', 'Классическая мужская стрижка с укладкой', 45, 1200, '✂️'),
            ('Стрижка женская', 'Женская стрижка любой сложности', 60, 2000, '💇'),
            ('Окрашивание волос', 'Окрашивание, мелирование, балаяж', 120, 4500, '🎨'),
            ('Маникюр', 'Классический маникюр с покрытием гель-лак', 75, 1800, '💅'),
            ('Педикюр', 'Аппаратный педикюр с покрытием', 90, 2500, '🦶'),
            ('Брови', 'Коррекция и окрашивание бровей', 45, 1000, '👁'),
        ]
        Service.objects.all().delete()
        created_services = []
        for name, desc, duration, price, icon in services_data:
            s = Service.objects.create(name=name, description=desc, duration=duration, price=price, icon=icon)
            created_services.append(s)
        self.stdout.write(f'Создано {len(created_services)} услуг')

        # Masters
        masters_data = [
            ('Анна Соколова', 'Стилист-колорист, 8 лет опыта', 'Специализируется на окрашивании и женских стрижках'),
            ('Михаил Петров', 'Барбер, 5 лет опыта', 'Мастер мужских стрижек и укладок'),
            ('Елена Кузнецова', 'Мастер маникюра и педикюра', 'Эксперт в nail-art и покрытиях'),
        ]
        Master.objects.all().delete()
        created_masters = []
        for name, spec, bio in masters_data:
            m = Master.objects.create(name=name, specialization=spec, bio=bio)
            created_masters.append(m)
        self.stdout.write(f'Создано {len(created_masters)} мастеров')

        # Appointments
        Appointment.objects.all().delete()
        names = ['Иван Петров', 'Мария Сидорова', 'Алексей Козлов', 'Ольга Новикова',
                 'Дмитрий Морозов', 'Юлия Волкова', 'Андрей Лебедев', 'Татьяна Соколова']
        phones = ['+7 916 123-45-67', '+7 926 234-56-78', '+7 936 345-67-89',
                  '+7 906 456-78-90', '+7 967 567-89-01', '+7 977 678-90-12']
        times = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
        statuses = ['new', 'confirmed', 'done', 'done', 'done']

        today = date.today()
        for i in range(25):
            delta = random.randint(-14, 14)
            d = today + timedelta(days=delta)
            Appointment.objects.create(
                service=random.choice(created_services),
                master=random.choice(created_masters),
                client_name=random.choice(names),
                client_phone=random.choice(phones),
                date=d,
                time=random.choice(times),
                status='done' if delta < 0 else random.choice(['new', 'confirmed']),
            )
        self.stdout.write(f'Создано 25 записей')
        self.stdout.write(self.style.SUCCESS('Готово! Логин: admin / Пароль: admin'))
