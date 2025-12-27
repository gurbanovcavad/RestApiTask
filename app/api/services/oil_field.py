from django.shortcuts import get_object_or_404
from ..models import OilField
from ..schemas import OilFieldIn
from ninja.errors import HttpError
from django.http import Http404

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