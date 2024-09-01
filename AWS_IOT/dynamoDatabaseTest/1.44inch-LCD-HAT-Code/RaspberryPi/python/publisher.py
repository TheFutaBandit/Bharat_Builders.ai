#1/usr/bin/env python3
import paho.mqtt.client as mqtt
import ssl
import json
import time
from datetime import datetime
from waveshare_1_44inch_LCD_HAT import LCD_1in44
from PIL import Image, ImageDraw, ImageFont

# Initialize the LCD
LCD = LCD_1in44.LCD()
LCD.Init()
LCD.clear()

# Create image buffer
image = Image.new('RGB', (LCD.width, LCD.height), "WHITE")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)

# File to store the alarm data
ALARM_FILE = "/home/pi/alarm_data.json"

def save_alarm_data(alarm_time, alarm_message):
    alarm_data = {"time": alarm_time, "message": alarm_message}
    with open(ALARM_FILE, "w") as f:
        json.dump(alarm_data, f)

def load_alarm_data():
    try:
        with open(ALARM_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def display_message(message):
    draw.rectangle((0, 0, LCD.width, LCD.height), fill="WHITE")
    draw.text((5, 30), message, font=font, fill="BLACK")
    LCD.ShowImage(image)

def check_and_display_alarm():
    alarm_data = load_alarm_data()
    if alarm_data:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == alarm_data["time"]:
            display_message(alarm_data["message"])

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        client.subscribe("raspi/data")
    else:
        print("connection error")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    process_payload(payload)

def process_payload(payloadmsg):
    print(f"Received payload: {payloadmsg}")
    try:
        data = json.loads(payloadmsg)
        action = data.get("action")
        
        if action == "set_alarm":
            alarm_time = data.get("time")
            alarm_message = data.get("message")
            save_alarm_data(alarm_time, alarm_message)
            print(f"New alarm set: {alarm_time}, Message: {alarm_message}")
        
        display = data.get("display", 0)
        if display == 1:
            alarm_data = load_alarm_data()
            if alarm_data:
                display_message(f"Alarm: {alarm_data['time']}")
            else:
                display_message("No alarm set")
    except json.JSONDecodeError:
        print("Invalid JSON payload")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='./DEVICE_Certificates/rootCA.pem', 
               certfile='./DEVICE_Certificates/certificate.pem.crt', 
               keyfile='./DEVICE_Certificates/private.pem.key', 
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3cz6591mmwk24-ats.iot.ap-south-1.amazonaws.com", 8883, 60)

def main_loop():
    client.loop_start()
    try:
        while True:
            check_and_display_alarm()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.loop_stop()
        client.disconnect()
        LCD.clear()

if __name__ == "__main__":
    main_loop()
