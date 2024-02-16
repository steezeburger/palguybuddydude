from django.core.management.base import BaseCommand


class BaseManagementCommand(BaseCommand):
    """
    This class if for containing logic that
    we want shared across all management commands.
    """

    def add_arguments(self, parser):
        """
        Add dry_run argument for every management command by default.
        """
        parser.add_argument(
            '--dry_run',
            help='Run script with out saving changes to database.',
            action='store_true'
        )

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.

        Copied directly from Django's code from django/core/management/base.py
        """
        raise NotImplementedError('subclasses of BaseManagementCommand must provide a handle() method')
