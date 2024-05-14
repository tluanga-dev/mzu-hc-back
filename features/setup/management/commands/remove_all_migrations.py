from django.core.management.base import BaseCommand, call_command
import os
import shutil
from config import settings
import django

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def handle(self, *args, **options):

        def remove_database_file(database_file):
            if os.path.exists(database_file):
                try:
                    os.remove(database_file)
                    print(f'Successfully deleted {database_file}')
                except Exception as e:
                    print(f'Failed to delete {database_file}. Reason: {e}')

        remove_database_file('db.sqlite3')
        self.stdout.write(self.style.SUCCESS('Successfully removed database file'))

        def remove_migrations():
            start_path = settings.BASE_DIR
            django_path = os.path.dirname(django.__file__)
            for root, dirs, files in os.walk(start_path):
                if 'migrations' in dirs and django_path not in root:
                    migrations_dir = os.path.join(root, 'migrations')
                    try:
                        shutil.rmtree(migrations_dir)
                        print(f'Successfully deleted {migrations_dir}')
                    except Exception as e:
                        print(f'Failed to delete {migrations_dir}. Reason: {e}')

        remove_migrations()
        self.stdout.write(self.style.SUCCESS('Successfully removed migrations'))

        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Successfully ran migrations'))