from django.db import models

# Create your models here.
class OilField(models.Model):
    oil_field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    operator_company = models.CharField(max_length=255)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name   

class Well(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("shut-in", "Shut-in"), ("abandoned", "Abandoned")]
    well_id = models.AutoField(primary_key=True)
    oil_field_id = models.ForeignKey(OilField, on_delete=models.CASCADE, related_name="wells")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    drill_date = models.DateField()
    depth_m = models.FloatField()
    
    def __str__(self):
        return self.name

class Sensor(models.Model):
    SENSOR_TYPES = [("pressure", "Pressure"), ("temperature", "Temperature"), ("flow_rate", "Flow Rate")]
    sensor_id = models.AutoField(primary_key=True)
    well_id = models.ForeignKey(Well, on_delete=models.CASCADE, related_name="sensors")
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    install_date = models.DateField()
    is_active = models.BooleanField()
    
    def __str__(self):
        return f"{self.sensor_type} sensor for {self.well_id.name}"
    

class ProductionReading(models.Model):
    reading_id = models.AutoField(primary_key=True) 
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="readings")
    timestamp = models.DateTimeField()
    value = models.FloatField()
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"Reading {self.reading_id} at {self.timestamp}"