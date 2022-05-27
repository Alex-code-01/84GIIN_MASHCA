
from apps.WebApp.models import ConfigDate

def queryConfig(param):    
    time_value = int(ConfigDate.objects.get(parameter=param).value)
    time_unit = ConfigDate.objects.get(parameter=param).unit.lower()
    return [time_value, time_unit]
    