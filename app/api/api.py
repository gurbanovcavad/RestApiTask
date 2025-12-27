from ninja_extra import NinjaExtraAPI
from .controllers.oil_field import OilFieldController
from .controllers.well import WellController
from .controllers.sensor import SensorController
from .controllers.reading import ReadingController

api = NinjaExtraAPI(title="Oilfield Operations API", version="0.1.0")

api.register_controllers(
    OilFieldController,
    WellController, 
    SensorController,
    ReadingController, 
)