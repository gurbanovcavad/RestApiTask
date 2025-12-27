from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_put, http_delete
from typing import List
from ..schemas import ProductionReadingIn, ProductionReadingOut
from ..services.reading import ReadingService
from typing import Optional

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