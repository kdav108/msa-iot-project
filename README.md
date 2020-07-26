# IoT project for Microsoft Student Accelerator Program 2020

### Description
The python script in this repository simulates an IoT device that makes measurement of the sun intensity (in 1000's of Lux) and the soil moisture (indictaed by the soil tension in kPa). The system is a prototype for an IoT device that helps gardeners track their soil and location suitability to continue growing the crops.

The data from the simulated device is sent to Azure IoT Hub through which it connects to the Azure Stream Analytics and ultimately used in power BI to create a report with visual information summarising the average soil Tension, the average Light Intensity and a graph of the light Intensity and soil tension over time. This information can help figure out whether the location for the plants/crops being grown and the amount of water fed is ideal or not.

The range of the Light Intensity measurements is between 0 Lux to 100000 Lux (Which can be typical on a summer day)
The range of the soil Tension level is between 0 to 80 kPa (Typical of a Tensiometer)
Note: A higher soil tension indicates dryer soil.

### Technology used:
- Python version 3.7
- Azure IoT Hub library
- Azure cloud service (specifically Azure IoT Hub and Azure Stream Analytics)
- Power BI 

### Contributor/s
KUNJ DAVE
