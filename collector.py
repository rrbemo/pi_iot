
import datetime
import RPi.GPIO as GPIO
import PCF8591 as ADC
from gpiozero import CPUTemperature
from pymongo import MongoClient
import time
import math

# Start the mongo server with `sudo mongod --port 27018`
client = MongoClient('localhost', 27018)
db = client['pymongo_test']
temps = db['temps']

# Set up pins
pins = {
    17 : {'name' : 'Thermoresistor'}
}
GPIO.setmode(GPIO.BCM)

def awake():
	ADC.setup(0x48)
	for pin in pins:
	    GPIO.setup(pin, GPIO.IN)
    
def get_temp_data(analog_pin):
	analogVal = ADC.read(analog_pin)
	Vr = 5 * float(analogVal) / 255
	Rt = 10000 * Vr / (5 - Vr)
	temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
	temp = temp - 273.15
	temp_f = (temp * 9 / 5) + 32
	print('temperature = {}F'.format(temp_f))
	return temp_f
	#print('temperature = {}C'.format(temp))
	#return temp

def loop():
    while 1:
        cpu = CPUTemperature()
        temp = {
            "datetime"  : datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "cpu_temp"  : cpu.temperature,
            "temp_1"    : get_temp_data(0),
            "temp_2"    : get_temp_data(1)
            }
        result = temps.insert_one(temp)
        print(result.inserted_id)
        # TODO: Subtract the time it takes to run the loop from 30 seconds.
        time.sleep(30)
    
if __name__ == '__main__':
	try:
		awake()
		loop()
	except KeyboardInterrupt:
		pass