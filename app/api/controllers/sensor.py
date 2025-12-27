from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_put, http_delete
from typing import List
from ..schemas import SensorIn, SensorOut
from ..services.sensor import SensorService
from typing import Optional

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