# Author: Kunj Dave
# Date created: 22/07/20

# Import all dependencies
import time
import random
# Using the Python Device SDK for IoT hub: https://github.com/Azure/azure-iot-sdk-python
# This helps connect the data generated here to a device-specific MQTT endpoint on the IoT Hub
from azure.iot.device import IoTHubDeviceClient, Message


# Define device connection strings
environmentSensor = "HostName=msa-project-iot-hub.azure-devices.net;DeviceId=LightSensor;SharedAccessKey=TMH6FAeq0kbF/+E6cbP5tVgTWnAfLi2ZI3lF5OxMpgI="
message = '{{"LightIntensity": {intensity}, "SoilTension": {tension}}}'

# Create base data
init_lightIntensity = 50  # In 1000 lux
init_soilTension = 40  # In kPa assuming a Tensiometer is used
desiredTensionMax = 50
desiredTensionMin = 20

# Initial weather
init_overcast = False  # Represents whether the weather is becoming more overcast (True) or less overcast (False)


def run_simulation(overcast, lightIntensity, soilTension):
    try:
        client = IoTHubDeviceClient.create_from_connection_string(environmentSensor)
        print("Light and soil sensor sending periodic messages (press Ctrl-C to exit)" )

        while True:
            if not overcast:
                # Sunlight keeps increasing
                lightIntensity += random.random()/100

                # There's some chance clouds start obscuring the sky again
                # Probability of change is low since if the weather was overcast before it would tend to stay overcast
                # the next minute.
                if random.random() < 0.05:
                    overcast = True

                # Soil Moisture generally increases if sun light intensity increases
                # Soil Moisture is measured in kPa so would not fluctuate a lot (i.e an increase/decrease of somewhere
                # between 0.001 and 0.01 is a reasonable assumption)
                soilTension += random.random()/100

            else:
                #  Sunlight decreases
                lightIntensity -= random.random()/100

                # There's some chance clouds start disappearing
                if random.random() < 0.05:
                    overcast = False

                soilTension -= random.random()/100

            # Check if soilMoisture is still valid (it cannot exceed 80 or fall below 0 is using a Tensiometer)
            soilTension = min(soilTension, 80)
            soilTension = max(soilTension, 0)

            # Ensure Light Intensity measurements are valid
            lightIntensity = min(lightIntensity, 100000)  # Has to be lower than 65000 lux (round figure)
            lightIntensity = max(lightIntensity, 0.001)  # Has to be greater than 1 lux

            # Packet measurements
            data = Message(message.format(intensity=lightIntensity, tension=soilTension))
            # intensity_data = Message(message_light.format(intensity=lightIntensity))
            # soil_data = Message(message_soil.format(tension=soilTension))

            # Check if soil tension which is roughly related to it's dryness is within good limits
            if soilTension > desiredTensionMax:
                data.custom_properties["drynessAlert"] = "True"
                data.custom_properties["wetnessAlert"] = "False"
            elif soilTension < desiredTensionMin:
                data.custom_properties["drynessAlert"] = "False"
                data.custom_properties["wetnessAlert"] = "True"
            else:
                data.custom_properties["drynessAlert"] = "False"
                data.custom_properties["wetnessAlert"] = "False"

            # Send packet data
            client.send_message(data)
            print(data)


            # Wait a second before sending next message
            time.sleep(1)

    except KeyboardInterrupt:
        print("Message outflow stopped")


if __name__ == '__main__':
    run_simulation(init_overcast, init_lightIntensity, init_soilTension)

