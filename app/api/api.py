from ninja_extra import NinjaExtraAPI
from .controllers import OilFieldController, WellController, SensorController, ReadingController

api = NinjaExtraAPI(title="Oilfield Operations API", version="0.1.0")

api.register_controllers(
    OilFieldController,
    WellController, 
    SensorController,
    ReadingController, 
)