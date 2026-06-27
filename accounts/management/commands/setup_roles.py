from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from tasks.models import Task


class Command(BaseCommand):
    help = 'Create Admin and User roles and set up permissions'

    def handle(self, *args, **options):
        admin_group, created = Group.objects.get_or_create(name='Admin')
        user_group, created = Group.objects.get_or_create(name='User')

        content_type = ContentType.objects.get_for_model(Task)
        permissions = Permission.objects.filter(content_type=content_type)

        admin_group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS('Roles created: Admin (full access), User'))
        self.stdout.write(self.style.SUCCESS('To create an admin user, run:'))
        self.stdout.write(self.style.SUCCESS('  python manage.py shell -c "from django.contrib.auth.models import User, Group; u = User.objects.get(username=\\\'USERNAME\\\'); u.groups.add(Group.objects.get(name=\\\'Admin\\\'))"'))
        self.stdout.write(self.style.SUCCESS('Or via Django admin at /admin/'))
