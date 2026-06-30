from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Service, Master, Appointment
from datetime import date, timedelta


def home(request):
    services = Service.objects.all()
    masters = Master.objects.all()
    today = date.today()
    upcoming = Appointment.objects.filter(date__gte=today, status__in=['new', 'confirmed']).count()
    return render(request, 'home.html', {
        'services': services,
        'masters': masters,
        'upcoming': upcoming,
    })


def book(request, service_id=None):
    services = Service.objects.all()
    masters = Master.objects.all()
    selected_service = None
    if service_id:
        selected_service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service = get_object_or_404(Service, id=request.POST.get('service'))
        master_id = request.POST.get('master')
        master = Master.objects.filter(id=master_id).first() if master_id else None

        appointment = Appointment.objects.create(
            service=service,
            master=master,
            client_name=request.POST.get('name', '').strip(),
            client_phone=request.POST.get('phone', '').strip(),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            comment=request.POST.get('comment', '').strip(),
        )
        messages.success(request, 'Запись успешно создана!')
        return redirect('success', pk=appointment.pk)

    # Доступные даты — следующие 14 дней кроме воскресенья
    available_dates = []
    d = date.today()
    for _ in range(20):
        d += timedelta(days=1)
        if d.weekday() != 6:  # не воскресенье
            available_dates.append(d)
        if len(available_dates) == 14:
            break

    times = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']

    return render(request, 'book.html', {
        'services': services,
        'masters': masters,
        'selected_service': selected_service,
        'available_dates': available_dates,
        'times': times,
    })


def success(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'success.html', {'appointment': appointment})


def appointments_list(request):
    today = date.today()
    appointments = Appointment.objects.select_related('service', 'master').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'appointments.html', {
        'appointments': appointments,
        'today': today,
        'status_filter': status_filter,
    })
