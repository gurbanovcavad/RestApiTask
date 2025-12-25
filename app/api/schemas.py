from datetime import date, datetime
from ninja import Schema
from typing import Optional

class OilFieldBase(Schema):
    name: str
    location: str
    operator_company: str
    start_date: date

class OilFieldIn(OilFieldBase):
    pass

class OilFieldOut(OilFieldBase):
    oil_field_id: int
    
    class Config:
        from_attributes = True

class WellBase(Schema):
    name: str
    status: str
    drill_date: date
    depth_m: int

class WellIn(WellBase):
    oil_field_id: int  

class WellOut(WellBase):
    well_id: int
    oil_field_id: OilFieldOut

    class Config:
        from_attributes = True
        
class SensorBase(Schema):
    sensor_type: str
    install_date: date
    is_active: bool

class SensorIn(SensorBase):
    well_id: int  

class SensorOut(SensorBase):
    sensor_id: int
    well_id: WellOut

    class Config:
        from_attributes = True
        
class ProductionReadingBase(Schema):
    timestamp: datetime
    value: float
    unit: str

class ProductionReadingIn(ProductionReadingBase):
    sensor_id: int  

class ProductionReadingOut(ProductionReadingBase):
    reading_id: int
    sensor_id: SensorOut

    class Config:
        from_attributes = True