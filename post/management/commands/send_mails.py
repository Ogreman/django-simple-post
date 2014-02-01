from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from post.models import Email

class Command(BaseCommand):
    help = 'Checks for any emails that need to be sent.'

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                "Sending unsent mail..."
            )
            for mail in Email.objects.filter(sent=False):
                mail.send()
        except Exception as ex:
            raise CommandError('An error occurred: ', ex)
        finally:
            print "Process complete."