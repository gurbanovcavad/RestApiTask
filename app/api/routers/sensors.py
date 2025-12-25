from ninja import Router
from typing import List, Optional
from ..models import Sensor, Well
from ..schemas import SensorIn, SensorOut 
from ninja.errors import HttpError
from django.http import Http404
from django.shortcuts import get_object_or_404

sensors = Router()

# create a new sensor
@sensors.post("/", response=SensorOut, tags=["Sensor CRUD"])
def create_sensor_item(request, item: SensorIn):
    try: 
        well = get_object_or_404(Well, well_id=item.well_id)
        sensor = Sensor.objects.create(well_id=well, sensor_type=item.sensor_type, install_date=item.install_date, is_active=item.is_active)
        return sensor
    except Http404 as e:
        raise e
    except Exception as e:
        raise HttpError(400, "Invalid Input")

# return the list of sensors and also sensors of well with id=well_id
@sensors.get("/", response=List[SensorOut], tags=["Sensor CRUD"])
def list_sensor_items(request, well_id: Optional[int] = None):
    try: 
        sensors = Sensor.objects.all() if not well_id else Well.objects.get(well_id=well_id).sensors.all()
        return sensors
    except Exception as e:
        raise HttpError(404, "Not Found")

# return the sensor with id=sensor_id
@sensors.get("/{sensor_id}", response=SensorOut, tags=["Sensor CRUD"])
def get_sensor_item(request, sensor_id: int):
    sensor = get_object_or_404(Sensor, sensor_id=sensor_id)
    return sensor

# update the sensor with id=sensor_id
@sensors.put("/{sensor_id}", response=SensorOut, tags=["Sensor CRUD"])
def update_sensor_item(request, sensor_id: int, updated: SensorIn):
    try: 
        sensor = get_object_or_404(Sensor, sensor_id=sensor_id)
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

# delete the sensor with id=sensor_id 
@sensors.delete("/{sensor_id}", tags=["Sensor CRUD"])
def delete_sensor_item(request, sensor_id: int):
    try: 
        sensor = get_object_or_404(Sensor, sensor_id=sensor_id)
        sensor.delete()
        return {"message": "Object Deleted Successfully"}
    except Http404 as e:
        raise Http404(str(e))
    except Exception as e:
        raise HttpError(400, "Something Went Wrong")