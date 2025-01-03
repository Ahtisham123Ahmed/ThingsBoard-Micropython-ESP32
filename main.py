import time
import network
import machine
import ubinascii
from umqtt.simple import MQTTClient

# ThingsBoard MQTT broker details
THINGSBOARD_SERVER = "thingsboard.cloud"
THINGSBOARD_PORT = 1883
TOKEN = "FR7IOfTyqxlW6TQW9WmZ"  # Ensure this is correctly set

# MQTT topics
TELEMETRY_TOPIC = "v1/devices/me/telemetry"
ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
COMMANDS_TOPIC = "v1/devices/me/rpc/request/+"

# Pin to control the LED (use the onboard LED pin)
LED_PIN = 2  # Adjust based on your board

# Wi-Fi connection details
SSID = 'Redmi10'
PASSWORD = 'shami1234'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)

    print("Connected to WiFi")

def on_message(topic, msg):
    print("Received message on topic:", topic)
    print("Message:", msg)

    # Example command handling for turning the LED on/off
    if topic == COMMANDS_TOPIC:
        command = msg.decode('utf-8')
        if command == "turn_on":
            machine.Pin(LED_PIN, machine.Pin.OUT).value(1)  # Turn LED on
            print("LED turned ON")
        elif command == "turn_off":
            machine.Pin(LED_PIN, machine.Pin.OUT).value(0)  # Turn LED off
            print("LED turned OFF")

def mqtt_connect():
    if not TOKEN:
        print("Error: TOKEN is not set!")
        return None 

    client_id = ubinascii.b2a_base64(TOKEN.encode()).decode().strip()
    print("Connecting to ThingsBoard with client ID:", client_id)

    client = MQTTClient(client_id, THINGSBOARD_SERVER, user=TOKEN, port=THINGSBOARD_PORT)
    client.set_callback(on_message)

    try:
        client.connect()
        print("Connected to ThingsBoard")
        return client 
    except Exception as e:
        print("Failed to connect to ThingsBoard:", e)
        return None 

def publish_telemetry(client, data):
    if client:
        client.publish(TELEMETRY_TOPIC, data)
        print("Published telemetry:", data)

def send_attributes(client, led_mode, led_state):
    if client:
        client.publish(ATTRIBUTES_TOPIC,
                       '{"ledMode":' + str(led_mode) + ',"ledState":' + str(led_state) + '}')
        print(f"Sent attributes: ledMode={led_mode}, ledState={led_state}")

def main():
    connect_wifi()
    
    client = mqtt_connect()
    
    if not client: 
        print("MQTT connection failed. Exiting.")
        return
    
    led_mode = 0  # 0 = continuous, 1 = blinking
    led_state = False  # LED off initially 
    blinking_interval = 1000  # in milliseconds 
    last_blink_time = time.ticks_ms() 
    
    last_telemetry_time = time.ticks_ms() 
    
    try:
        while True:
            current_time = time.ticks_ms()
            
            # Handle blinking mode 
            if led_mode == 1 and time.ticks_diff(current_time, last_blink_time) >= blinking_interval:
                led_state = not led_state  # Toggle LED state 
                last_blink_time = current_time 
                machine.Pin(LED_PIN, machine.Pin.OUT).value(led_state)  # Control the LED pin 

            # Send telemetry data every two seconds 
            if time.ticks_diff(current_time, last_telemetry_time) >= 2000:
                last_telemetry_time = current_time 
                telemetry_data = '{"temperature":24.8,"humidity":55.6}'
                publish_telemetry(client, telemetry_data) 
                send_attributes(client, led_mode, led_state)

            # Check for incoming MQTT messages (e.g., RPC commands) 
            client.check_msg() 

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
        
    finally:
        client.disconnect()
        print("Disconnected from ThingsBoard")

# Run the main loop 
if __name__ == "__main__":
     main()
