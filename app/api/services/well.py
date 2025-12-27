from django.shortcuts import get_object_or_404
from ..models import OilField, Well
from ..schemas import OilFieldIn, WellIn
from typing import Optional
from ninja.errors import HttpError
from django.http import Http404

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