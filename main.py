# Author: Kunj Dave
# Date created: 22/07/20

# Import all dependencies
from azure.iot.device import IoTHubDeviceClient, Message
import time
import random

# Define device connection strings
lightSensor = "HostName=msa-project-iot-hub.azure-devices.net;DeviceId=LightSensor;SharedAccessKey=TMH6FAeq0kbF/+E6cbP5tVgTWnAfLi2ZI3lF5OxMpgI="

# Create base data
lightIntensity = 15 # In 1000 lux


def run_simulation():
    try:
        client = IoTHubDeviceClient.create_from_connection_string(lightSensor)
        print("Light sensor sending periodic messages (press Ctrl-C to exit)" )

        while True:
            # Packets and send message data
            time.sleep(1) # Wait 1 secodn before sending next message
    except KeyboardInterrupt:
        print("message outflow stopped")


if __name__ == '__main__':
    run_simulation()

