#!/usr/bin/python3

#import interrupt_client, MCP342X, wind_direction, HTU21D, bmp085, tgs2600, ds18b20_therm
import time
import interrupt_client
import wind_direction

#wind_dir = wind_direction.wind_direction(adc_channel = 7, config_file="wind_direction.json")
interrupts = interrupt_client.interrupt_client(port = 49501)
if __name__ == "__main__":
	while True:
		#wind_average = wind_dir.get_value(10) #ten seconds
		#print(wind_average)
		if (interrupts.get_wind() >0):
		    print("********** Speed " + str(interrupts.get_wind()))
		    interrupts.reset()
		#interrupts.get_wind_gust() gives you the highest value in last 5 seconds - assuming you don't reset interrupts
		
	
