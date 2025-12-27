from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_put, http_delete
from typing import List
from .schemas import OilFieldIn, OilFieldOut, WellIn, WellOut, SensorIn, SensorOut, ProductionReadingIn, ProductionReadingOut
from .services import OilFieldService, WellService, SensorService, ReadingService
from typing import Optional

@api_controller('/oil-fields', tags=['OilField CRUD'])
class OilFieldController(ControllerBase):
    def __init__(self, service: OilFieldService):
        self.service = service

    # create a new oil_field
    @http_post('/', response=OilFieldOut)
    def create_oilfield(self, item: OilFieldIn):
        return self.service.create(item)

    # return the list of oil_fields
    @http_get('/', response=List[OilFieldOut])
    def list_oilfields(self):
        return self.service.list_all()

    # return the oil_field with id=oil_field_id
    @http_get('/{oil_field_id}', response=OilFieldOut)
    def get_oilfield(self, oil_field_id: int):
        return self.service.get_by_id(oil_field_id)

    # update the oil_field with id=oil_field_id 
    @http_put('/{oil_field_id}', response=OilFieldOut)
    def update_oilfield(self, oil_field_id: int, item: OilFieldIn):
        return self.service.update(oil_field_id, item)

    # delete the oil_field with id=oil_field_id
    @http_delete('/{oil_field_id}')
    def delete_oilfield(self, oil_field_id: int):
        return self.service.delete(oil_field_id)
    
@api_controller('/wells', tags=['Well CRUD'])
class WellController(ControllerBase):
    def __init__(self, service: WellService):
        self.service = service

    # create a new well
    @http_post('/', response=WellOut)
    def create_well(self, item: WellIn):
        return self.service.create(item)

    # return the list of wells and also wells of oilfield with id=oil_field_id
    @http_get('/', response=List[WellOut])
    def list_wells(self, oil_field_id: Optional[int] = None):
        return self.service.list_all(oil_field_id)

    # return the well with id=well_id
    @http_get('/{well_id}', response=WellOut)
    def get_well(self, well_id: int):
        return self.service.get_by_id(well_id)

    # update the well with id=well_id 
    @http_put('/{well_id}', response=WellOut)
    def update_well(self, well_id: int, item: WellIn):
        return self.service.update(well_id, item)

    # delete the well with id=well_id
    @http_delete('/{well_id}')
    def delete_well(self, well_id: int):
        return self.service.delete(well_id)
    
@api_controller('/sensors', tags=['Sensor CRUD'])
class SensorController(ControllerBase):
    def __init__(self, service: SensorService):
        self.service = service

    # create a new sensor
    @http_post('/', response=SensorOut)
    def create_sensor(self, item: SensorIn):
        return self.service.create(item)

    # return the list of sensors and also sensors of well with id=well_id
    @http_get('/', response=List[SensorOut])
    def list_sensors(self, well_id: Optional[int] = None):
        return self.service.list_all(well_id)

    # return the sensor with id=sensor_id
    @http_get('/{sensor_id}', response=SensorOut)
    def get_sensor(self, sensor_id: int):
        return self.service.get_by_id(sensor_id)

    # update the sensor with id=sensor_id 
    @http_put('/{sensor_id}', response=SensorOut)
    def update_sensor(self, sensor_id: int, item: SensorIn):
        return self.service.update(sensor_id, item)

    # delete the sensor with id=sensor_id
    @http_delete('/{sensor_id}')
    def delete_sensor(self, sensor_id: int):
        return self.service.delete(sensor_id)

@api_controller('/production-readings', tags=['ProductionReading CRUD'])
class ReadingController(ControllerBase):
    def __init__(self, service: ReadingService):
        self.service = service

    # create a new production_reading
    @http_post('/', response=ProductionReadingOut)
    def create_reading(self, item: ProductionReadingIn):
        return self.service.create(item)

    # return the list of production_readings with optional filters
    @http_get('/', response=List[ProductionReadingOut])
    def list_readings(self, sensor_id: Optional[int] = None, start: Optional[str] = None, end: Optional[str] = None):
        return self.service.list_all(sensor_id, start, end)

    # return the production_reading with id=reading_id
    @http_get('/{reading_id}', response=ProductionReadingOut)
    def get_reading(self, reading_id: int):
        return self.service.get_by_id(reading_id)

    # update the production_reading with id=reading_id
    @http_put('/{reading_id}', response=ProductionReadingOut)
    def update_reading(self, reading_id: int, item: ProductionReadingIn):
        return self.service.update(reading_id, item)

    # delete the production_reading with id=reading_id
    @http_delete('/{reading_id}')
    def delete_reading(self, reading_id: int):
        return self.service.delete(reading_id)