
from apps.WebApp.models import Config

def queryConfig(param):    
    time_value = int(Config.objects.get(parameter=param).value)
    time_unit = Config.objects.get(parameter=param).unit.lower()
    return [time_value, time_unit]
    