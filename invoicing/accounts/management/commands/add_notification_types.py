from django.core.management.base import BaseCommand, CommandError
from accounts.models import NotificationType

class Command(BaseCommand):
  help = "Populate the database with the default notification types."

  def load_notif_types(self):
    for nt in ["T", "E"]:
      NotificationType.objects.get_or_create(name=nt)

  def handle(self, *args, **kwargs):
    self.stdout.write("Loading database with notification types... ")
    self.load_notif_types()
    self.stdout.write(self.style.SUCCESS("Notification types  added."))
