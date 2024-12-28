from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Task

class Command(BaseCommand):
    help = 'Send reminders for tasks with deadlines in 24 hours'

    def handle(self, *args, **kwargs):
        upcoming_tasks = Task.objects.filter(
            deadline__range=(now(), now() + timedelta(hours=24)),
            status='PENDING'
        )
        for task in upcoming_tasks:
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    subject=f'Reminder: Task "{task.title}" Deadline Approaching',
                    message=f'Hello {task.assigned_to.username},\n\n'
                            f'This is a reminder that the deadline for the task "{task.title}" is approaching.\n\n'
                            f'Deadline: {task.deadline}\n\n'
                            f'Please ensure it is completed on time.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[task.assigned_to.email],
                    fail_silently=False,
                )
        self.stdout.write(self.style.SUCCESS('Reminders sent successfully.'))
