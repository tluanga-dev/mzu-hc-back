# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission

# class Command(BaseCommand):
#     help = 'Creates user groups and assigns permissions.'

#     def handle(self, *args, **options):
#         self.create_groups()
#         self.stdout.write(self.style.SUCCESS('Successfully created user groups'))

#     def create_groups(self):
#         # Define the groups and their corresponding permissions
#         groups_permissions = {
#             'Admins': ['add_user', 'change_user', 'delete_user'],
#             'Editors': ['change_user'],
#             'Viewers': [],
#         }
#         for group_name, perms_codenames in groups_permissions.items():
#             group, created = Group.objects.get_or_create(name=group_name)
#             permissions = Permission.objects.filter(codename__in=perms_codenames)
#             group.permissions.set(permissions)
#             if created:
#                 self.stdout.write(f'Created new group: {group_name}')
#             else:
#                 self.stdout.write(f'Updated group: {group_name}')
