
from abc import abstractmethod

class NetworkModel:
    def __init__(self):
        pass

    @abstractmethod
    def op(self):
        pass

class ZeroMQPubSub                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       (NetworkModel):
    def __init__(self):
        super().__init__()

    def op(self):
        import network_models.ZeroMQPubSubModel as ZeroMQPubSubModel
        print(ZeroMQPubSubModel.fetch_weather_info())
        return ZeroMQPubSubModel.fetch_weather_info()

'''class ImageCollection(NetworkModel):
    def __init__(self):
        super().__init__()

    def op(self):
        import udo_models.getPictureModel as getPictureModel
        getPictureModel.getPicture_()
        print("!Get Picture")
        return None
'''
