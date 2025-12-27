from django.shortcuts import get_object_or_404
from ..models import Sensor, ProductionReading
from ..schemas import ProductionReadingIn
from typing import Optional
from ninja.errors import HttpError
from django.http import Http404
from datetime import datetime

class ReadingService:
    def create(self, item: ProductionReadingIn):
        try: 
            sensor = get_object_or_404(Sensor, sensor_id=item.sensor_id)
            production_reading = ProductionReading.objects.create(sensor_id=sensor, timestamp=item.timestamp, value=item.value, unit=item.unit)
            return production_reading
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")
    
    def list_all(self, sensor_id: Optional[int] = None, start: Optional[str] = None, end: Optional[str] = None):
        try: 
            # print(sensor_id, start, end)
            
            # default url
            if not sensor_id and not start and not end:
                production_readings = ProductionReading.objects.all()
            # query based on sensor_id
            elif sensor_id and not start and not end:
                sensor = Sensor.objects.get(sensor_id=sensor_id)
                production_readings = sensor.readings.all()
            # filter based on time range
            elif not sensor_id and start and end:
                start += " 00:00:00+00:00"
                end += " 00:00:00+00:00"
                start = datetime.fromisoformat(start)
                end = datetime.fromisoformat(end)
                production_readings = ProductionReading.objects.all()
                res = []
                for reading in production_readings:
                    if start <= reading.timestamp <= end:
                        res.append(reading.reading_id)
                production_readings = ProductionReading.objects.filter(reading_id__in=res)
            # raise an exception 
            else:
                raise HttpError(400, ("Invalid Request"))
            return production_readings
        except Exception as e:
            raise HttpError(400, "Something Went Wrong")

    def get_by_id(self, id: int):
        production_reading = get_object_or_404(ProductionReading, reading_id=id)
        return production_reading

    def update(self, id: int, updated: ProductionReadingIn):
        try: 
            production_reading = get_object_or_404(ProductionReading, reading_id=id)
            sensor = get_object_or_404(Sensor, sensor_id=updated.sensor_id)
            production_reading.sensor_id = sensor
            production_reading.timestamp = updated.timestamp
            production_reading.value = updated.value
            production_reading.unit = updated.unit
            production_reading.save()
            return production_reading
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")

    def delete(self, id: int):
        try: 
            production_reading = get_object_or_404(ProductionReading, reading_id=id)
            production_reading.delete()
            return {"message": "Object Deleted Successfully"}
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Something Went Wrong")