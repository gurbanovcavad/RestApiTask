from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_put, http_delete
from typing import List
from ..schemas import OilFieldIn, OilFieldOut
from ..services.oil_field import OilFieldService
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