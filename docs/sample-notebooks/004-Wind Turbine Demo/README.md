Credits

https://github.com/microsoft/sql-server-samples/tree/master/samples/demos/azure-sql-edge-demos

## Overview

The Azure SQL Edge demo is based on a Contoso Renewable Energy, a wind turbine farm that leverages Azure SQL Edge for data processing onboard the generator. 

The demo will walk you through resolving an alert being raised due to wind turbulence being detected at the device. You will train a model and deploy it to SQL DB Edge that will correct the detected wind wake and ultimately optimize power output. 

We will also look at some of the security features available with Azure SQL Edge. 

## Wind Turbine Data Explanation for the Wake Detection model

The data stored in the database table represents the following:


* **RecordId:** _Unique identifier for the entry._
* **TurbineId:** _Unique identifier for the turbine in scope._
* **GearboxOilLevel:** _Oil level recorded for the turbine gear box at the time of the reading._
* **GearboxOilTemp:** _Oil temperature recorded for the turbine gear box at the time of the reading._
* **GeneratorActivePower:** _Active Power recorded by the turbine generator._
* **GeneratorSpeed:** _Speed recorded by the turbine generator._
* **GeneratorTemp:** _Temperature recorded by the turbine generator._
* **GeneratorTorque:** _Torque recorded by the turbine generator._
* **GridFrequency:** _Frequency recorded in the grid for the specific wind turbine._
* **GridVoltage:** _Voltage recorded in the grid for the specific wind turbine._
* **HydraulicOilPressure:** _Current pressure of the hydraulic oil for the wind turbine._
* **NacelleAngle:** _Angle of the nacelle at the time of the reading (the housing that contains all the generating components)._
* **PitchAngle:** _Pitch angle of the blades against the oncoming air stream to obtain the optimal amount of energy._
* **Vibration:** _Vibration of the wind turbine at the time of the reading._
* **WindSpeedAverage:** _Average wind speed calculated from the last X records._
* **Precipitation:** _Flag to represent if rain was present at the time of the reading._
* **WindTempAverage:** _Average wind temperature calculated from the last X records._
* **OverallWindDirection:** _Overall wind direction recorded at the time of the reading._
* **TurbineWindDirection:** _Turbine wind direction recorded at the time of the reading._
* **TurbineSpeedAverage:** _Average turbine speed calculated from the last X records._
* **WindSpeedStdDev:** _Standard Deviation of the last X WindSpeedAverage records._
* **TurbineSpeedStdDev:**  _Standard Deviation of the last X TurbineSpeedAverage records._

The above dataset definition contains trends that will enable us to detect the existence of wake in a wind turbine. There are two main conditions that influence the presence of wind wake:

1.	Overall wind farm and turbine wind direction are both between 40° - 45° degrees.
1.	TurbineSpeedStdDev and WindSpeedStdDev have been too far apart for greater than a minute.

The wind turbine will experience wake when the turbine wind direction is between 40° - 45° degrees and the values of TurbineSpeedStdDev and WindSpeedStdDev are not similar. For example: 
* Wake Present:
    * TurbineWindDirection = 43.5°
    * TurbineSpeedStdDev = 8.231
    * WindSpeedStdDev = 0.23
* Wake Not Present:
    * TurbineWindDirection = 23.5°
    * TurbineSpeedStdDev = 0.921
    * WindSpeedStdDev = 0.213


