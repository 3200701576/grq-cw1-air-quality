"""
Django management command to import air quality data from city_day.csv
"""
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from api.models import AirQualityRecord


class Command(BaseCommand):
    help = 'Import air quality data from city_day.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing records before importing',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of records to import (for testing)',
        )

    def handle(self, *args, **options):
        csv_path = 'data/city_day.csv'

        if options['clear']:
            count = AirQualityRecord.objects.count()
            AirQualityRecord.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing records'))

        # Count total rows first
        with open(csv_path, 'r', encoding='utf-8') as f:
            total_rows = sum(1 for _ in f) - 1  # subtract header

        limit = options.get('limit')
        if limit:
            total_rows = min(total_rows, limit)

        self.stdout.write(f'Found {total_rows} records to import')

        imported = 0
        skipped = 0
        errors = 0

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row_num, row in enumerate(reader, start=2):
                if limit and imported >= limit:
                    break

                try:
                    # Parse date
                    date_str = row['Date'].strip()
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        self.stderr.write(f'Row {row_num}: Invalid date format "{date_str}"')
                        errors += 1
                        continue

                    # Helper function to parse float or None
                    def parse_float(value):
                        if value is None or value.strip() == '':
                            return None
                        try:
                            return float(value)
                        except ValueError:
                            return None

                    # Create record
                    record = AirQualityRecord(
                        city=row['City'].strip(),
                        date=date,
                        pm25=parse_float(row.get('PM2.5')),
                        pm10=parse_float(row.get('PM10')),
                        no2=parse_float(row.get('NO2')),
                        co=parse_float(row.get('CO')),
                        aqi=int(parse_float(row.get('AQI'))) if parse_float(row.get('AQI')) is not None else None,
                    )
                    record.save()
                    imported += 1

                    # Progress indicator every 1000 records
                    if imported % 1000 == 0:
                        self.stdout.write(f'Progress: {imported}/{total_rows} records imported')

                except IntegrityError:
                    skipped += 1
                except Exception as e:
                    self.stderr.write(f'Row {row_num}: Error - {str(e)}')
                    errors += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nImport complete!\n'
            f'  - Imported: {imported}\n'
            f'  - Skipped (duplicates): {skipped}\n'
            f'  - Errors: {errors}'
        ))
