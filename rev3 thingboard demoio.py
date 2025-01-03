from tb_device_mqtt import TBDeviceMqttClient
import network  
import socket  
import struct
import time
# Wi-Fi credentials  
SSID = 'Redmi10'  
PASSWORD = 'shami1234'  

# Connect to Wi-Fi  
def connect_wifi():  
    wlan = network.WLAN(network.STA_IF)  
    wlan.active(True)  
    wlan.connect(SSID, PASSWORD)  

    while not wlan.isconnected():  
        print("Connecting to WiFi...")  
        time.sleep(1)  

    print("Connected to WiFi")  
connect_wifi()
# Replace with your ThingsBoard Cloud hostname and device token
THINGSBOARD_HOST = "demo.thingsboard.io"  # or your ThingsBoard Cloud server
ACCESS_TOKEN = "ESP32_REV0"  # Replace with your device token

# Telemetry data to send

# Create a client instance
client = TBDeviceMqttClient(THINGSBOARD_HOST, access_token=ACCESS_TOKEN)

# Connect to ThingsBoard
client.connect()
while True:
    for x in range(1, 100):
        temp=x
        telemetry = {"temperature": temp, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
        time.sleep(1)
        client.send_telemetry(telemetry)
        
        
      
# Sending telemetry


# Disconnect from ThingsBoard
client.disconnect()

