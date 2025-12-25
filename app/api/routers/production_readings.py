from ninja import Router
from typing import List, Optional
from ..models import ProductionReading, Sensor
from datetime import datetime
from ..schemas import ProductionReadingIn, ProductionReadingOut
from ninja.errors import HttpError
from django.http import Http404
from django.shortcuts import get_object_or_404

production_readings = Router()

# def is_iso(dt_str):
#     try:
#         datetime.fromisoformat(dt_str)
#         return True
#     except ValueError:
#         return False

# create a new production_reading
@production_readings.post("/", response=ProductionReadingOut, tags=["ProductionReading CRUD"])
def create_production_reading_item(request, item: ProductionReadingIn):
    try: 
        sensor = get_object_or_404(Sensor, sensor_id=item.sensor_id)
        production_reading = ProductionReading.objects.create(sensor_id=sensor, timestamp=item.timestamp, value=item.value, unit=item.unit)
        return production_reading
    except Http404 as e:
        raise e
    except Exception as e:
        raise HttpError(400, "Invalid Input")

# return the list of production_readings 
@production_readings.get("/", response=List[ProductionReadingOut], tags=["ProductionReading CRUD"])
def list_production_reading_items(request, sensor_id: Optional[int] = None, start: Optional[str] = None, end: Optional[str] = None):
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

# return the production_readings with id=production_reading_id
@production_readings.get("/{reading_id}", response=ProductionReadingOut, tags=["ProductionReading CRUD"])
def get_production_reading_item(request, reading_id: int):
    production_reading = get_object_or_404(ProductionReading, reading_id=reading_id)
    return production_reading
    
# update the production_reading with id=production_reading_id
@production_readings.put("/{reading_id}", response=ProductionReadingOut, tags=["ProductionReading CRUD"])
def update_production_reading_item(request, reading_id: int, updated: ProductionReadingIn):
    try: 
        production_reading = get_object_or_404(ProductionReading, reading_id=reading_id)
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

# delete the production_readings with id=production_reading_id 
@production_readings.delete("/{reading_id}", tags=["ProductionReading CRUD"])
def delete_production_reading_item(request, reading_id: int):
    try: 
        production_reading = get_object_or_404(ProductionReading, reading_id=reading_id)
        production_reading.delete()
        return {"message": "Object Deleted Successfully"}
    except Http404 as e:
        raise e
    except Exception as e:
        raise HttpError(400, "Something Went Wrong")