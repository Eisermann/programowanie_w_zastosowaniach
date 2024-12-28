from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from weasyprint import HTML

from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            # Wysyłanie e-mail
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    subject=f'New Task Assigned: {task.title}',
                    message=f'Hello {task.assigned_to.username},\n\n'
                            f'You have been assigned a new task:\n\n'
                            f'Title: {task.title}\n'
                            f'Description: {task.description}\n'
                            f'Deadline: {task.deadline}\n\n'
                            f'Please complete it on time.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[task.assigned_to.email],
                    fail_silently=False,
                )
            return redirect(reverse('task_list'))
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('task_detail', args=[task.pk]))
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('task_list'))
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def generate_report(request):
    # Pobierz wszystkie zadania
    tasks = Task.objects.all().order_by('deadline')

    # Renderowanie szablonu do HTML
    html_string = render_to_string('tasks/report_template.html', {'tasks': tasks, 'generated_at': timezone.now()})

    # Generowanie PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="task_report.pdf"'
    HTML(string=html_string).write_pdf(response)

    return response
