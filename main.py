# Author: Kunj Dave
# Date created: 22/07/20

# Import all dependencies
from azure.iot.device import IoTHubDeviceClient, Message
import time
import random

# Define device connection strings
lightSensor = "HostName=msa-project-iot-hub.azure-devices.net;DeviceId=LightSensor;SharedAccessKey=TMH6FAeq0kbF/+E6cbP5tVgTWnAfLi2ZI3lF5OxMpgI="
soilSensor = "HostName=msa-project-iot-hub.azure-devices.net;DeviceId=SoilDevice;SharedAccessKey=9Of1GyYiq4Z70nXL8u82KtgqD/u+t+GLPp81+m3MqO0="
message_light = '{{"LightIntensity": {intensity}}}'
message_soil = '{{"SoilTension": {tension}}}'
# message_light = '{{"LightIntensity": {intensity}, "SoilTension": {tension}}}'

# Create base data
init_lightIntensity = 50  # In 1000 lux
init_soilTension = 40  # In kPa assuming a Tensiometer is used
desiredTensionMax = 50
desiredTensionMin = 20

# Initial weather
init_overcast = False  # Represents whether the weather is becoming more overcast (True) or less overcast (False)


def run_simulation(overcast, lightIntensity, soilTension):
    try:
        client_light_sensor = IoTHubDeviceClient.create_from_connection_string(lightSensor)
        client_tension_sensor = IoTHubDeviceClient.create_from_connection_string(soilSensor)
        print("Light and soil sensor sending periodic messages (press Ctrl-C to exit)" )

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
                # between 0.01 and 0.1 is a reasonable assumption)
                soilTension += random.random()/10

            else:
                #  Sunlight decreases
                lightIntensity -= random.random()/10

                # There's some chance clouds start disappearing
                if random.random() < 0.01:
                    overcast = False

                soilTension -= random.random()

            # Check if soilMoisture is still valid (it cannot exceed 80 or fall below 0 is using a Tensiometer)
            soilTension = min(soilTension, 80)
            soilTension = max(soilTension, 0)

            # Ensure Light Intensity measurements are valid
            lightIntensity = min(lightIntensity, 100000)  # Has to be lower than 65000 lux (round figure)
            lightIntensity = max(lightIntensity, 0.001)  # Has to be greater than 1 lux

            # Packet measurements
            # data = Message(message.format(intensity=lightIntensity, tension=soilTension))
            intensity_data = Message(message_light.format(intensity=lightIntensity))
            soil_data = Message(message_soil.format(tension=soilTension))

            # Check if soil tension which is roughly related to it's dryness is within good limits
            if soilTension > desiredTensionMax:
                soil_data.custom_properties["drynessAlert"] = "True"
                soil_data.custom_properties["wetnessAlert"] = "False"
            elif soilTension < desiredTensionMin:
                soil_data.custom_properties["drynessAlert"] = "False"
                soil_data.custom_properties["wetnessAlert"] = "True"
            else:
                soil_data.custom_properties["drynessAlert"] = "False"
                soil_data.custom_properties["wetnessAlert"] = "False"

            # Send packet data
            # client.send_message(data)
            client_light_sensor.send_message(intensity_data)
            client_tension_sensor.send_message(soil_data)
            print(soil_data)
            print(intensity_data)

            # Wait 1 second before sending next message
            time.sleep(1)

    except KeyboardInterrupt:
        print("Message outflow stopped")


if __name__ == '__main__':
    run_simulation(init_overcast, init_lightIntensity, init_soilTension)

