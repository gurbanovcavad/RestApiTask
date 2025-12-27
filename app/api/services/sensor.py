from django.shortcuts import get_object_or_404
from ..models import Well, Sensor
from ..schemas import SensorIn
from typing import Optional
from ninja.errors import HttpError
from django.http import Http404

class SensorService:
    def create(self, item: SensorIn):
        try: 
            well = get_object_or_404(Well, well_id=item.well_id)
            sensor = Sensor.objects.create(well_id=well, sensor_type=item.sensor_type, install_date=item.install_date, is_active=item.is_active)
            return sensor
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")
    
    def list_all(self, well_id: Optional[int] = None):
        try: 
            sensors = Sensor.objects.all() if not well_id else Well.objects.get(well_id=well_id).sensors.all()
            return sensors
        except Exception as e:
            raise HttpError(404, "Not Found")

    def get_by_id(self, id: int):
        sensor = get_object_or_404(Sensor, sensor_id=id)
        return sensor

    def update(self, id: int, updated: SensorIn):
        try: 
            sensor = get_object_or_404(Sensor, sensor_id=id)
            well = get_object_or_404(Well, well_id=updated.well_id)
            sensor.sensor_type = updated.sensor_type
            sensor.install_date = updated.install_date
            sensor.is_active = updated.is_active
            sensor.well_id = well
            sensor.save()
            return sensor
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")

    def delete(self, id: int):
        try: 
            sensor = get_object_or_404(Sensor, sensor_id=id)
            sensor.delete()
            return {"message": "Object Deleted Successfully"}
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Something Went Wrong")