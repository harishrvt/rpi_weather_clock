import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

import time
import requests
import datetime


### Initialize GPIO pins based on Physical Connections

lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D22)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_backlight = digitalio.DigitalInOut(board.D4)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


## Configuration Items
weather_data_refresh_in_mins = 5

location_latitude = '-10.5'
location_longitude = '107.3'
api_key = 'enter_api_key_here'


## Initialize weather counter to 1 less than update value so that it updates on first run of the loop
weather_update_ctr = (60 * weather_data_refresh_in_mins) - 1

## Display Init message if API call is unsuccessful
message = 'Pi Init ...'
temp = 'Unk'
weather_desc = 'Unk'

while (True):
    weather_update_ctr = weather_update_ctr + 1
    
    ## Check if weather update counter has reached its target and refresh
    if (weather_update_ctr == 60 * weather_data_refresh_in_mins):
        weather_update_ctr = 0
        
        ## Use OpenWeatherMap API to get weather using LAT, LONG and API KEY
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+location_latitude+ 
                                '&lon='+location_longitude+
                                '&appid='+api_key)
        
        ## If API response is OK, then convert temp from Kelvin to Celcius and get weather description
        if (response.status_code == 200):
            temp = round(response.json()['main']['temp'] - 273, 1)
            weather_desc = response.json()['weather'][0]['description']
            
   ## Display message on LCD if update available, else use last values
    message = str(temp) + '-' + weather_desc + '\n' + datetime.datetime.now().strftime('%b %d  %H:%M:%S\n')
    lcd.clear()    
    lcd.message = message
    time.sleep(1.0)



