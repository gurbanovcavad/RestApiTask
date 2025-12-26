import csv
from django.core.management.base import BaseCommand
from api.models import OilField, Well, Sensor, ProductionReading
from datetime import datetime
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data_dir = r"/app/api/data"
        oil_fields = []
        with open(os.path.join(data_dir, 'oil_fields.csv'), mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                oil_fields.append(OilField(
                    name=row['name'],
                    location=row['location'],
                    operator_company=row['operator_company'],
                    start_date=datetime.strptime(row['start_date'], "%m/%d/%Y")
                ))
        OilField.objects.bulk_create(oil_fields)
        wells = []
        with open(os.path.join(data_dir, 'wells.csv'), mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                wells.append(Well(
                    oil_field_id=OilField.objects.get(oil_field_id=row['oil_field_id']),
                    name=row['name'],
                    status=row['status'],
                    drill_date=datetime.strptime(row['drill_date'], "%Y-%m-%d"),
                    depth_m=row['depth_m']
                ))
        Well.objects.bulk_create(wells)
        sensors = []
        with open(os.path.join(data_dir, 'sensors.csv'), mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sensors.append(Sensor(
                    well_id=Well.objects.get(well_id=row['well_id']),
                    sensor_type=row['sensor_type'],
                    install_date=datetime.strptime(row['install_date'], "%Y-%m-%d"),
                    is_active=row['is_active'].strip().lower() == 'true'
                ))
        Sensor.objects.bulk_create(sensors)
        production_readings = []
        with open(os.path.join(data_dir, 'production_readings.csv'), mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                production_readings.append(ProductionReading(
                    sensor_id=Sensor.objects.get(sensor_id=row['sensor_id']),
                    timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S"),
                    value=row['value'],
                    unit=row['unit']
                ))
        ProductionReading.objects.bulk_create(production_readings)
        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))
