from ninja import Router
from typing import List
from ..models import OilField
from ..schemas import OilFieldIn, OilFieldOut
from ninja.errors import HttpError
from django.http import Http404
from django.shortcuts import get_object_or_404

oil_fields = Router()

# create a new oil_field
@oil_fields.post("/", response=OilFieldOut,  tags=["OilField CRUD"])
def create_oilfield_item(request, item: OilFieldIn):
    try: 
        oil_field = OilField.objects.create(name=item.name, location=item.location, operator_company=item.operator_company, start_date=item.start_date)
        return oil_field
    except Exception as e:
        raise HttpError(400, "Invalid Input")

# return the list of oil_fields
@oil_fields.get("/", response=List[OilFieldOut], tags=["OilField CRUD"])
def list_oilfield_items(request):
    try:
        oilfields = OilField.objects.all()
        return oilfields
    except Exception as e:
        raise HttpError(404, "Not Found")

# return the oil_field with id=oil_field_id
@oil_fields.get("/{oil_field_id}", response=OilFieldOut, tags=["OilField CRUD"])
def get_oilfield_item(request, oil_field_id: int):
    oilfield = get_object_or_404(OilField, oil_field_id=oil_field_id)
    return oilfield

# update the oil_field with id=oil_field_id 
@oil_fields.put("/{oil_field_id}", response=OilFieldOut, tags=["OilField CRUD"])
def update_oilfield_item(request, oil_field_id: int, updated: OilFieldIn):
    try: 
        oilfield = get_object_or_404(OilField, oil_field_id=oil_field_id)
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

# delete the oil_field with id=oil_field_id
@oil_fields.delete("/{oil_field_id}", tags=["OilField CRUD"])
def delete_oilfield_item(request, oil_field_id: int):
    try:
        oilfield = get_object_or_404(OilField, oil_field_id=oil_field_id)
        oilfield.delete()
        return {"message": "Object Deleted Successfully"}
    except Http404 as e:
        raise e
    except Exception as e:
        raise HttpError(400, "Something Went Wrong")