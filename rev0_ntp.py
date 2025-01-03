import network  
import socket  
import struct  
import time  
import ntptime
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
local_time=time.localtime()
print(local_time)

    
