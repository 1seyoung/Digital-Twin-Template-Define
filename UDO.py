
from abc import abstractmethod
import asyncio

class UserDefinedObject:
    def __init__(self):
        pass

    @abstractmethod
    def op(self):
        pass

    @abstractmethod
    def oo(self):
        pass

class WeatherCollection(UserDefinedObject):
    def __init__(self):
        super().__init__()

    def op(self):
        import udo_models.EnvFetchModel as EnvFetchModel
        print(EnvFetchModel.fetch_weather_info())
        return EnvFetchModel.fetch_weather_info()
    
class BitcoinPriceCollection(UserDefinedObject):
    def __init__(self):
        super().__init__()

    def op(self):
        import udo_models.getBitcoinPrice as getBF

        print(getBF.get_bf())
        return None

class DetectThingNum(UserDefinedObject):
    def __init__(self):
        super().__init__()

    def op(self):
        import udo_models.detectThing as dt
        print(dt.cap())

class ImageCollection(UserDefinedObject):
    def __init__(self):
        super().__init__()


    def op(self):
        import udo_models.getPictureModel as getPictureModel
        getPictureModel.getPicture()
        return None



