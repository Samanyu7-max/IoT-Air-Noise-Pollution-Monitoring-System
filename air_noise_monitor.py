import network
import urequests
from machine import ADC, Pin
from time import sleep

# ------------------------------
# WiFi DETAILS
# ------------------------------
SSID = "WW"
PASSWORD = "password"

# ------------------------------
# ThingSpeak Settings
# ------------------------------
API_KEY = "K9F4WEOJ25MTYCJU"
URL = "http://api.thingspeak.com/update?api_key=" + API_KEY

# ------------------------------
# Sensor Setup
# ------------------------------
mq135 = ADC(26)  # Air quality sensor (Analog input GP26)
sound = ADC(27)  # Sound sensor (Analog input GP27)

sound_digital = Pin(16, Pin.IN)  # Optional digital output


# ------------------------------
# Connect WiFi
# ------------------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        print(".", end="")
        sleep(0.5)

    print("\nConnected!")
    print("IP:", wlan.ifconfig()[0])


# ------------------------------
# Main Loop
# ------------------------------
connect_wifi()

while True:
    air_value = mq135.read_u16()
    sound_value = sound.read_u16()
    digital_state = sound_digital.value()

    air_quality_ppm = round((air_value / 65535) * 500, 2)
    noise_db = round((sound_value / 65535) * 120, 2)

    print("--------------------------")
    print("Air Quality (PPM):", air_quality_ppm)
    print("Sound Level (dB):", noise_db)
    print("Digital State:", digital_state)

    try:
        send_url = (URL +
                   "&field1=" + str(air_quality_ppm) +
                   "&field2=" + str(noise_db) +
                   "&field3=" + str(digital_state))
                   
        response = urequests.get(send_url)
        print("ThingSpeak Response:", response.text)
        response.close()
    except Exception as e:
        print("Upload Error:", e)

    sleep(20)  # ThingSpeak requires 15s minimum
