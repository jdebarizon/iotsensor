import os
import glob
import subprocess
import time
import urllib2
import json

#initialize
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Temperature device
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Opens raw device, code changed to reflect issue in Raspian
def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

# Reads temperature, outputs celsius
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

url = 'http://129.144.9.165:7070/jderest/orchestrator/JDE_ORCH_Sample_UpdateMeterReadings_Generic'

postdata = {
     'username': 'jde',  
     'password': 'your_e1_password',
      'inputs': [ {
        'name': 'EquipmentNumber',
        'value': '34665'
       }, {
        'name': 'NewFuelMeterReading',
        'value': str(read_temp())
       }, {
        'name': 'NewHourMeterReading',
        'value': '22'
       }]
}

req = urllib2.Request(url)
req.add_header('Content-Type','application/json')
data = json.dumps(postdata)

response = urllib2.urlopen(req,data)
