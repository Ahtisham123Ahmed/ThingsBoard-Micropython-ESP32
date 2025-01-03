import machine
import time
import logging
from tb_device_mqtt import TBDeviceMqttClient
import network

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# GPIO pin for LED
led = machine.Pin(2, machine.Pin.OUT)
led.value(0)
SSID = 'Redmi10'  
PASSWORD = 'shami1234'  

# Step 1: Connect to Wi-Fi
def connect_wifi():  
    wlan = network.WLAN(network.STA_IF)  
    wlan.active(True)  
    wlan.connect(SSID, PASSWORD)  

    while not wlan.isconnected():  
        print("Connecting to WiFi...")  
        time.sleep(1)  

    print("Connected to WiFi")  

connect_wifi()

# Step 2: ThingsBoard Configuration
THINGSBOARD_HOST = "demo.thingsboard.io"  # ThingsBoard host
ACCESS_TOKEN = "ESP32_REV0"               # Device token for ESP32

# Initialize ThingsBoard MQTT client
client = TBDeviceMqttClient(THINGSBOARD_HOST, access_token=ACCESS_TOKEN)

# Callback function to handle RPC requests
def on_rpc_request(client, params):
    log.info("Received RPC request: %s", str(params))

    method = params.get('method')

    if method == 'setLedStateon':
        print("debug ledon")
        led.on()

    elif method == 'setLedStateoff':
        led.off()
        print("debug ledoff")
    

# Set the callback for RPC requests
client.set_server_side_rpc_request_handler(on_rpc_request)

# Step 3: Connect to ThingsBoard
def connect_to_thingsboard():
    client.connect()

# Main function to handle telemetry and attributes
def main():
    client.connect()

    # Sending data in async way
    attributes = {"sensorModel": "DHT-22", "attribute_2": "value"}
    telemetry = {"temperature": 41.9, "humidity": 69, "enabled": False, "currentFirmwareVersion": "v1.2.2"}

    client.send_attributes(attributes)
    client.send_telemetry(telemetry)
    client.set_server_side_rpc_request_handler(on_rpc_request)

    # Periodically check for new MQTT messages
while True:
    time.sleep(0.5)  # Sleep to reduce CPU usage while waiting for incoming messages
    #client.check_for_rpc_requests()  # Check for incoming RPC requests
    main()
    time.sleep(0.5)
 





