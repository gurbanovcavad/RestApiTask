from ninja import Router
from typing import List, Optional
from ..models import OilField, Well
from ..schemas import WellIn, WellOut
from ninja.errors import HttpError
from django.http import Http404
from django.shortcuts import get_object_or_404

wells = Router()

# create a new well
@wells.post("/", response=WellOut, tags=["Well CRUD"])
def create_well_item(request, item: WellIn):
    try: 
        oilfield = get_object_or_404(OilField, oil_field_id=item.oil_field_id)
        well = Well.objects.create(name=item.name, status=item.status, drill_date=item.drill_date, depth_m=item.depth_m, oil_field_id=oilfield)
        return well
    except Http404 as e:
        raise e
    except Exception as e:
        raise HttpError(400, "Invalid Input")

# return the list of wells and also wells of oilfield with id=oil_field_id
@wells.get("/", response=List[WellOut], tags=["Well CRUD"])
def list_well_items(request, oil_field_id: Optional[int] = None):
    try: 
        wells = Well.objects.all() if not oil_field_id else OilField.objects.get(oil_field_id=oil_field_id).wells.all()
        return wells
    except Exception as e:
        raise HttpError(404, "Not Found")

# return the well with id=well_id
@wells.get("/{well_id}", response=WellOut, tags=["Well CRUD"])
def get_well_item(request, well_id: int):
    well = get_object_or_404(Well, well_id=well_id)
    return well

# update the well with id=well_id
@wells.put("/{well_id}", response=WellOut, tags=["Well CRUD"])
def update_well_item(request, well_id: int, updated: WellIn):
    try: 
        well = get_object_or_404(Well, well_id=well_id)
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

# delete the well with id=well_id 
@wells.delete("/{well_id}", tags=["Well CRUD"])
def delete_well_item(request, well_id: int):
    try: 
        well = get_object_or_404(Well, well_id=well_id)
        well.delete() 
        return {"message": "Object Deleted Successfully"}
    except Http404 as e:
        raise e
    except Exception as e:
        raise HttpError(400, "Something Went Wrong")