import time
import random
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=cst8916finallothub.azure-devices.net;DeviceId=sensor2;SharedAccessKey=NeQr8fVvhRdEaS+B2NQSzX3QkWq3GbbahZrN8yMTTS8="

def get_telemetry():
    return {
        "location": "Fifth Avenue",
        "iceThickness": random.randint(20, 40),  # cm
        "surfaceTemperature": round(random.uniform(-10, 0), 1),  # °C
        "snowAccumulation": random.randint(0, 15),  # cm
        "externalTemperature": round(random.uniform(-15, 5), 1),  # °C
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
