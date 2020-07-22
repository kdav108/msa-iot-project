# Author: Kunj Dave
# Date created: 22/07/20

# Import all dependencies
from azure.iot.device import IoTHubDeviceClient, Message
import time
import random

# Define device connection strings
lightSensor = "HostName=msa-project-iot-hub.azure-devices.net;DeviceId=LightSensor;SharedAccessKey=TMH6FAeq0kbF/+E6cbP5tVgTWnAfLi2ZI3lF5OxMpgI="

# Create base data
lightIntensity = 15  # In 1000 lux
soilTension = 40  # In kPa assuming a Tensiometer is used
desiredTensionMax = 50
desiredTensionMin = 20

# Initial weather
overcast = False  # Represents whether the weather is becoming more overcast (True) or less overcast (False)


def run_simulation():
    try:
        client = IoTHubDeviceClient.create_from_connection_string(lightSensor)
        print("Light sensor sending periodic messages (press Ctrl-C to exit)" )

        while True:
            if not overcast:
                # Sunlight keeps increasing
                lightIntensity += random.random()

                # There's some chance clouds start obscuring the sky again
                # Probability of change is low since if the weather was overcast before it would tend to stay overcast
                # the next minute.
                if random.random() < 0.01:
                    overcast = True

                # Soil Moisture generally increases if sun light intensity increases
                # Soil Moisture is measured in kPa so would not fluctuate a lot (i.e an increase/decrease of somewhere
                # between 0 and 1 is a reasonable assumption)
                soilTension += random.random()

            else:
                #  Sunlight decreases
                lightIntensity -= random.random()

                # There's some chance clouds start disappearing
                if random.random() < 0.01:
                    overcast = False

                soilTension -= random.random()

            # Check if soilMoisture is still valid (it cannot exceed 80 or fall below 0 is using a Tensiometer)
            soilTension = min(soilTension, 80)
            soilTension = max(soilTension, 0)

            # Packets and send message data
            data = Message('{{"LightIntensity": {intensity}, "SoilTension": {tension}}}'.format(lightIntensity, soilTension))
            client.send_message(data)

            # Wait 1 second before sending next message
            time.sleep(1)

    except KeyboardInterrupt:
        print("message outflow stopped")


if __name__ == '__main__':
    run_simulation()

