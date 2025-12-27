from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_put, http_delete
from typing import List
from ..schemas import WellIn, WellOut
from ..services.well import WellService
from typing import Optional

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