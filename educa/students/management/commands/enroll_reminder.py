import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

"""
To run (locally):
`python manage.py enroll_reminder --days=20 --settings=educa.settings.local`

To run via docker (prod):
`docker compose exec web python /code/educa/manage.py enroll_reminder --days=20 --settings=educa.settings.prod`

Or through code execution:
from django.core import management
management.call_command('enroll_reminder', days=20)
"""

class Command(BaseCommand):
  help = 'Sends an e-mail reminder to users registered more than N days that are not enrolled into any courses yet'

  def add_arguments(self, parser):
    parser.add_argument('--days', dest='days', type=int)

  def handle(self, *args, **options):
    emails = []
    subject = 'Enroll in a course'
    date_joined = timezone.now().today() - datetime.timedelta(
      days=options['days'] or 0
    )
    users = User.objects.annotate(
      course_count=Count('courses_joined')
    ).filter(course_count=0, date_joined__date__lte=date_joined)
    for user in users:
      message = f"""Dear {user.first_name},
      We noticed that you didn't enroll in any courses yet
      What are you waiting for?"""
      emails.append(
        (
          subject,
          message,
          settings.DEFAULT_FROM_EMAIL,
          [user.email]
        )
      )
    send_mass_mail(emails)
    self.stdout.write(f'Sent {len(emails)} reminders')