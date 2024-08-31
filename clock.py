import os
import sys
import RPI.GPIO as GPIO
import multiprocessing as mp
import asyncio 
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont.
import json 
## {"alarm":"12:00","snooze":0,}
##{"set_alarm":"12:00","snooze":0,"alarm_vol": (0 to 100),"display_alarm":0 or 1} send as string 
class disp:
    width=10
    height=10

image1 = Image.new("1", (disp.width, disp.height), "WHITE")

def set_alarm(data):
    pass

def snooze(data):
    pass

def alarm_vol(data):
    pass
def display_alarm(data):
    pass

def read(data):
    pass

def run():
    try:
        while 1:
            then=datetime.now()

            await call(check info from aws)# microseconds
            await call(send info to aws)# microseconds

            if (datetime.now()-then).seconds >= 1:

                time=time_to_display.now()
                draw = ImageDraw.Draw(image1)
                Font1 = ImageFont.truetype("../Font/Font01.ttf",25)

                draw.text((5, 68), f'TIME: {time}', fill = 0, font=Font1)

            read(data)
    except KeyboardInterrupt:
        print("kill program")
