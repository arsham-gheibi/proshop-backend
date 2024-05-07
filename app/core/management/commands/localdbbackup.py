from django.core.management.base import BaseCommand
from django.utils import timezone
from subprocess import run


class Command(BaseCommand):
    """ Django Command to backup database"""

    def handle(self, *args, **options):
        """Entry Point for Command"""

        self.stdout.write('Backuping database ...')
        backup_file_name = f'backup_{timezone.now().timestamp()}.json'
        backup_file_path = f'core/fixtures/{backup_file_name}'

        run(
            ['python', 'manage.py', 'dumpdata',
             '--traceback',
             '--format=json',
             '--output', backup_file_path,
             '--exclude', 'admin',
             '--exclude', 'sessions',
             '--exclude', 'contenttypes']
        )

        self.stdout.write(self.style.SUCCESS('Database Backuped'))
