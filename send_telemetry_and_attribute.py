# Copyright 2024. ThingsBoard
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
RPC_REQUEST_TOPIC = 'v1/devices/me/rpc/request/'
msg={}
import logging
from tb_device_mqtt import TBDeviceMqttClient
import time
logging.basicConfig(level=logging.DEBUG)
import network
from time import sleep, time
telemetry = {"temperature": 41.9, "humidity": 69, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
telemetry_as_array = [{"temperature": 42.0}, {"humidity": 70}, {"enabled": True}, {"currentFirmwareVersion": "v1.2.3"}]
telemetry_with_ts = {"ts": int(round(time() * 1000)), "values": {"temperature": 42.1, "humidity": 70}}
telemetry_with_ts_as_array = [{"ts": 1451649600000, "values": {"temperature": 42.2, "humidity": 71}},
                              {"ts": 1451649601000, "values": {"temperature": 42.3, "humidity": 72}}]
attributes = {"sensorModel": "DHT-22", "attribute_2": "value"}

log = logging.getLogger(__name__)

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
def on_connect(client, userdata, flags, result_code, *extra_params, tb_client):
    if result_code == 0:
        log.info("Connected to ThingsBoard!")
    else:
        log.error("Failed to connect to ThingsBoard with result code: %d", result_code)


def main():
    client = TBDeviceMqttClient(THINGSBOARD_HOST, access_token=ACCESS_TOKEN)
    client.connect()


    # Sending data in async way
    client.send_attributes(attributes)
    client.send_telemetry(telemetry)
    client._handle_rpc_request(RPC_REQUEST_TOPIC,msg)
  
    
    client.send_telemetry(telemetry_with_ts)
    client.send_telemetry(telemetry_with_ts_as_array)

    # Waiting for data to be delivered
    result = client.send_attributes(attributes)
    #log.info("Attribute update sent: " + str(result.rc() == TBPublishInfo.TB_ERR_SUCCESS))
    result = client.send_attributes(attributes)
    #log.info("Telemetry update sent: " + str(result.rc() == TBPublishInfo.TB_ERR_SUCCESS))

    client.disconnect()


client.connect()
main()