# Final Project Assignment: Real-time Monitoring System for Rideau Canal Skateway

##  Scenario Description

The Rideau Canal Skateway in Ottawa is a famous naturally frozen skating rink in winter and requires constant monitoring for public safety. This project provides a real-time monitoring system that simulates IoT sensors placed at key locations along the canal to track environmental and ice conditions. These sensors send data to Azure IoT Hub, which is then processed using Azure Stream Analytics and stored in Azure Blob Storage for further analysis. This system helps the National Capital Commission (NCC) make informed decisions about skateway safety.

---

## System Architecture

![image](https://github.com/user-attachments/assets/f7ee5107-9607-48ff-be51-631f8f050bc6)


**Data Flow Overview**:
1. **Simulated IoT Sensors** (Dow's Lake, Fifth Avenue, NAC) generate data every 10 seconds.
2. **Azure IoT Hub** ingests this data in real-time.
3. **Azure Stream Analytics Job** processes the data using 5-minute window aggregations, aggreate average icae thickness, maximum snow accumulation.
4. **Azure Blob Storage** stores the processed output in JSON format for historical analysis.

---

## Implementation Details

### 1.  IoT Sensor Simulation

- Simulated with a Python script located in `sensor-simulation/sensor1.py`.
- Sends data message to Azure IoT Hub using the Device SDK, by command `python sensor1.py`.
- Example payload:
```json
  {"Location":"NAC",
  "AvgIceThickness":36.0,
  "MaxSnowAccumulation":12.0,
  "EventTime":"2025-04-14T22:05:00.0000000Z"}
```
### 2.  Azure IoT Hub Configuration
 - created IoT Hub on Azure Portal.
 - created 3 devices name `sensor1`, `sensor2` and `sensor3`, it repensents three different locations.
 - copy the primary connection string to python code, the devices are connceted now.
 - routes incoming messages to default event hub compatible endpoint.
### 3.  Azure Stream Analytics Job
- created Stream Analytics Job on Azure Portal.
- create input from IoT Hub named `iotinput`.
- create ouput from blob storage named `iotouput`.
- the input is ingest from IoT hub, and output will storage in blob storage.
- simple Query:
```sql
SELECT
    location AS Location,
    AVG(CAST(iceThickness AS float)) AS AvgIceThickness,
    MAX(CAST(snowAccumulation AS float)) AS MaxSnowAccumulation,
    System.Timestamp AS EventTime
INTO
    [iotoutput]
FROM
    [iotinput]
GROUP BY
    location, TumblingWindow(minute, 5)
```
### 4. Azure Blob Storage
-Output is saved in JSON format.
-Organized by folder pattern: `container/iotoutput`.
-Each file contains the average ice thickness and max snow accumulation for 5-minute intervals.

## Usage Instructions
### 1. Running the LoT Sensor Simulation
- create IoT Hub, Storage and Stream Analytic Jobs in the Azure Portal.
- create 3 sensors devices in IoT Hub, create container in Storage.
- add primary connection strings to python script from devices details.
- Install the `azure-iot-device` library to simulate sensor data. Run the following command:
```bash
pip install azure-iot-device
```
- run python script by command:
```bash
python sensor1.py
python sensor2.py
python sensor3.py
```

### 2. Configuring Azure Services
- create IoT Hub and add 3 devices named `sensor1`, `sensor2` and `sensor3`.
- create blob storage, and create container named `iotouput`.
- create stream analytic jobs, add input from IoT Hub named `iotinput`, add ouput from blob storage named `iotoutput`.
- apply query to retrieve datas.
### 3. Accessing Stored Data
- start azure stream analytic jobs.
- running python commands.
- go to container folder named iotoutput.
- wait for several times, refresh.
- click on the file, download.
- open the downloaded file using vs code, and we can see the JSON format data.
## Results
Simple JSON format output data from downloaded iotouput:
```json
{
"Location":"Dow's Lake",
"AvgIceThickness":31.40740740740741,
"MaxSnowAccumulation":15.0,
"EventTime":"2025-04-14T22:10:00.0000000Z"
}
```
## Reflection
The challege i meet are how to create the sensor simulator in python, i browse the code from in class IoT tutorial, and add locations and ice thickness, surface temperature, snow accumulation and external temperature.
The time window is 5 minutes, so i have to wait a long time for the data to collect and store in storage container.
The output data is in json format, can not be simply display beside on vs code, it will be better to power bi dashboards in the future.
