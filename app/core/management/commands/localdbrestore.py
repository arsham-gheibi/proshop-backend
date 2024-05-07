from django.core.management.base import BaseCommand
from subprocess import run
from os import listdir


class Command(BaseCommand):
    """ Django Command to backup database"""

    def handle(self, *args, **options):
        """Entry Point for Command"""

        self.stdout.write('Restoring database ...')

        files = listdir('core/fixtures')
        backup_files_list = [
            file for file in files
            if file.startswith('backup_')
        ]

        if not len(backup_files_list):
            self.stdout.write(self.style.ERROR('There is no Backup file'))

        else:
            backup_files_list.sort()
            backup_file_name = backup_files_list[-1]
            backup_file_path = f'core/fixtures/{backup_file_name}'

            run(
                ['python', 'manage.py', 'loaddata',
                 '--format=json',
                 '--traceback',
                 backup_file_path]
            )

            self.stdout.write(self.style.SUCCESS('Database Restored'))
