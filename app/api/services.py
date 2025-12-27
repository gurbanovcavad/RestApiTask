from django.shortcuts import get_object_or_404
from .models import OilField, Well, Sensor, ProductionReading
from .schemas import OilFieldIn, WellIn, SensorIn, ProductionReadingIn
from typing import Optional
from ninja.errors import HttpError
from django.http import Http404
from datetime import datetime

class OilFieldService:
    def create(self, item: OilFieldIn):
        try: 
            oil_field = OilField.objects.create(name=item.name, location=item.location, operator_company=item.operator_company, start_date=item.start_date)
            return oil_field
        except Exception as e:
            raise HttpError(400, "Invalid Input")
    
    def list_all(self):
        try:
            oilfields = OilField.objects.all()
            return oilfields
        except Exception as e:
            raise HttpError(404, "Not Found")

    def get_by_id(self, id: int):
        oilfield = get_object_or_404(OilField, oil_field_id=id)
        return oilfield

    def update(self, id: int, updated: OilFieldIn):
        try: 
            oilfield = get_object_or_404(OilField, oil_field_id=id)
            oilfield.name = updated.name
            oilfield.location = updated.location
            oilfield.operator_company = updated.operator_company
            oilfield.start_date = updated.start_date
            oilfield.save() 
            return oilfield
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")

    def delete(self, id: int):
        try:
            oilfield = get_object_or_404(OilField, oil_field_id=id)
            oilfield.delete()
            return {"message": "Object Deleted Successfully"}
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Something Went Wrong")
        
class WellService:
    def create(self, item: WellIn):
        try: 
            oilfield = get_object_or_404(OilField, oil_field_id=item.oil_field_id)
            well = Well.objects.create(name=item.name, status=item.status, drill_date=item.drill_date, depth_m=item.depth_m, oil_field_id=oilfield)
            return well
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")
    
    def list_all(self, oil_field_id: Optional[int] = None):
        try: 
            wells = Well.objects.all() if not oil_field_id else OilField.objects.get(oil_field_id=oil_field_id).wells.all()
            return wells
        except Exception as e:
            raise HttpError(404, "Not Found")

    def get_by_id(self, id: int):
        well = get_object_or_404(Well, well_id=id)
        return well

    def update(self, id: int, updated: OilFieldIn):
        try: 
            well = get_object_or_404(Well, well_id=id)
            oilfield = get_object_or_404(OilField, oil_field_id=updated.oil_field_id)
            well.name = updated.name
            well.status = updated.status 
            well.drill_date = updated.drill_date
            well.depth_m = updated.depth_m
            well.oil_field_id = oilfield
            well.save()
            return well
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Invalid Input")

    def delete(self, id: int):
        try: 
            well = get_object_or_404(Well, well_id=id)
            well.delete() 
            return {"message": "Object Deleted Successfully"}
        except Http404 as e:
            raise e
        except Exception as e:
            raise HttpError(400, "Something Went Wrong")
        
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