# IoT project for Microsoft Student Accelerator Program 2020

### Description
The python script in this repository simulates an IoT device that makes measurement of the sun intensity (in 1000's of Lux) and the soil moisture (indictaed by the soil tension in kPa). The system is a prototype for an IoT device that helps gardeners track their soil and location suitability to continue growing crops.

The data from the simulated device is sent to Azure IoT Hub through which it connects to the Azure Stream Analytics and ultimately used in power BI to create a report with visual information summarising the average soil tension, the average light intensity and a graph of the light intensity and soil tension over time. This information can help figure out whether the location for the plants/crops being grown and the amount of water fed is ideal or not.

The range of the Light Intensity measurements is between 0 Lux to 100000 Lux (Which can be typical on a summer day)
The range of the soil Tension level is between 0 to 80 kPa (Typical of a Tensiometer)
Note: A higher soil tension indicates dryer soil.

### Code Dependencies 
- Azure IoT library (azure.iot.device)

### Technology used:
- Python version 3.7
- Azure cloud services (specifically Azure IoT Hub and Azure Stream Analytics)
- Power BI

### How to run the code and test it
- Ensure that the relevant libraries are already installed (See Code Dependencies above).
- Replace the {YOUR CONNECTION STRING} place holder with your Azure Iot Hub device connection string (in quotations) - on line 13
- Run the python file (This would start generating randomised simulated data and send it to the cloud - you can view the data sent in the console)
- Check that Azure IoT Hub is recieving the data
- Start Azure Stream Analytics Job to connect the IoT incoming telemtry data to the Power BI output
- Check to see if the data recived in Power BI match the Power BI report in this repository (named 'Enviornment Report - MSA project'). (Note: Due to the data being simulated randomly and depending on how long the code is run, the values may not exactly match those in the Power BI Report in this repository).

### Contributor/s
KUNJ DAVE
