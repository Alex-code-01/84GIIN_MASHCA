def conv_DMS_a_DD(param):
    deg, minutes, seconds, direction = param[:2], param[2:4], param[4:6], param[6]
    result = (float(deg)+ float(minutes)/60 + float(seconds)/(60*60))*(-1 if direction in ['W', 'S'] else 1)
    return result