#!/usr/bin/python3

#import interrupt_client, MCP342X, wind_direction, HTU21D, bmp085, tgs2600, ds18b20_therm
import time
import InterruptClient
import WindDirection

'''
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)
time.sleep(1236549543542354368)
'''

wind_dir = WindDirection.wind_direction(adc_channel = 7, config_file="wind_direction.json")
interrupts = InterruptClient.interrupt_client(port = 49501)
if __name__ == "__main__":
	while True:
		wind_average = wind_dir.get_value(4) #ten seconds
		print(wind_average)
		if (interrupts.get_wind() >0):
		    #print(interrupts.get_wind()*0.277778) #Speed in M/s (*1.9438460492 for Knots)
		    interrupts.reset()
		#interrupts.get_wind_gust() gives you the highest value in last 5 seconds - assuming you don't reset interrupts
		
	
