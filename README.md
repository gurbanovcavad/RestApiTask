# Oilfield API 

## Schemas: 

### OilFieldOut
- **name**: string
- **location**: string
- **operator_company**: string
- **start_date**: string (date)
- **oil_field_id**: integer

### OilFieldIn
- **name**: string
- **location**: string
- **operator_company**: string
- **start_date**: string (date)

### WellOut
- **name**: string
- **status**: string
- **drill_date**: string (date)
- **depth_m**: integer
- **well_id**: integer
- **oil_field_id**: object

### WellIn
- **name**: string
- **status**: string
- **drill_date**: string (date)
- **depth_m**: integer
- **oil_field_id**: object

### SensorOut
- **sensor_type**: string
- **install_date**: string (date)
- **is_active**: boolean
- **sensor_id**: integer
- **well_id**: object

### SensorIn
- **sensor_type**: string
- **install_date**: string (date)
- **is_active**: boolean
- **well_id**: object

### ProductionReadingOut
- **timestamp**: string (date-time)
- **value**: number
- **unit**: string
- **reading_id**: integer
- **sensor_id**: object

### ProductionReadingIn
- **timestamp**: string (date-time)
- **value**: number
- **unit**: string
- **sensor_id**: object

## To Seed Data
```
python manage.py load_data 
```

## Endpoint List:

### OilField CRUD
    POST: /api/oil_fields/

    Example Value:
```
{
    "name": "string",
    "location": "string",
    "operator_company": "string",
    "start_date": "2025-12-26"
}
```
    GET: /api/oil_fields/
    ---------------------------
    GET: /api/oil_fields/{oil_field_id}
    ---------------------------
    PUT: /api/oil_fields/{oil_field_id}
    
    Example Value:
```
{
    "name": "string",
    "location": "string",
    "operator_company": "string",
    "start_date": "2025-12-26"
}
```
    DELETE: /api/oil_fields/{oil_field_id}    
### Well CRUD
    POST: /api/wells/

    Example Value:
```
{
    "name": "string",
    "status": "string",
    "drill_date": "2025-12-26",
    "depth_m": 0,
    "oil_field_id": 0
}
```
    GET: /api/wells?oil_field_id=1
    ---------------------------
    GET: /api/wells/{well_id}
    ---------------------------
    PUT: /api/wells/{well_id}
    
    Example Value:
```
{
    "name": "string",
    "status": "string",
    "drill_date": "2025-12-26",
    "depth_m": 0,
    "oil_field_id": 0
}
```
    DELETE: /api/wells/{well_id} 
### Sensor CRUD
    POST: /api/sensors/

    Example Value:
```
{
    "sensor_type": "string",
    "install_date": "2025-12-26",
    "is_active": true,
    "well_id": 0
}
```
    GET: /api/sensors?well_id=1
    ---------------------------
    GET: /api/sensors/{sensor_id}
    ---------------------------
    PUT: /api/sensors/{sensor_id}
    
    Example Value:
```
{
    "sensor_type": "string",
    "install_date": "2025-12-26",
    "is_active": true,
    "well_id": 0
}
```
    DELETE: /api/sensors/{sensor_id}
### ProductionReading CRUD
    POST: /api/production-readings/

    Example Value:
```
{
    "timestamp": "2025-12-26T16:36:00.970Z",
    "value": 0,
    "unit": "string",
    "sensor_id": 0
}
```
    GET: /api/production-readings?sensor_id=1 (or ?start=2025-01-01&?end=2025-01-01)
    ---------------------------
    GET: /api/production-readings/{reading_id}
    ---------------------------
    PUT: /api/production-readings/{reading_id}
    
    Example Value:
```
{
    "timestamp": "2025-12-26T16:36:00.970Z",
    "value": 0,
    "unit": "string",
    "sensor_id": 0
}
```
    DELETE: /api/production-readings/{reading_id}

## To Run the Project:
- change the .env.example to .env and update the context
```
docker-compose up --build
```