import random
import time

def generate_packageid():

    now = time.time() 
    ssd = now * 1000  
    tem = '%d' %ssd   
    randomlength = random.randint(8,10)
    ssdx = int((tem[randomlength:13]))  
    ssd2 = ssdx + 6000
    return ssd2

t = generate_packageid()    
print(t)

def allocate_package_call(package_id, chip_type, chip_number, plant_id):
    pass