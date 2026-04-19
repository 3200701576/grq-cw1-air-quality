"""
Django management command to renumber AirQualityRecord IDs sequentially from 1.

Usage:
    python manage.py renumber_records
"""
from django.core.management.base import BaseCommand
from api.models import AirQualityRecord


class Command(BaseCommand):
    help = 'Renumber all AirQualityRecord IDs sequentially from 1'

    def handle(self, *args, **options):
        total = AirQualityRecord.objects.count()
        
        if total == 0:
            self.stdout.write(self.style.WARNING('No records found.'))
            return
        
        self.stdout.write(f'Found {total} records. Renumbering IDs...')
        
        # Get all records ordered by some consistent criteria (e.g., city, date)
        records = list(AirQualityRecord.objects.all().order_by('city', 'date'))
        
        # Delete all existing records
        AirQualityRecord.objects.all().delete()
        
        # Re-insert with new sequential IDs
        new_id = 1
        for record in records:
            record.id = new_id
            record.save()
            new_id += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully renumbered {total} records (IDs 1 to {total})'))
