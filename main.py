import pico_wifi
from umqtt_simple import MQTTClient
import time
import config
from breakout_bme280 import *
from pimoroni_i2c import PimoroniI2C

CLIENT_NAME = "pico"
BROKER_ADDR = "192.168.0.2"
PINOUT = {"sda": 0, "scl": 1}

i2c = PimoroniI2C(**PINOUT)
bme = BreakoutBME280(i2c)
bme.configure(
    FILTER_COEFF_2,
    STANDBY_TIME_0_5_MS,
    OVERSAMPLING_16X,
    OVERSAMPLING_2X,
    OVERSAMPLING_1X,
    FORCED_MODE,
)
time.sleep(3)
pico_wifi.connect(config.WIFI_SSID, config.WIFI_PWD, verbose=True, led_toggle=True)
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=3600, user=config.MQTT_USER, password=config.MQTT_PWD)
mqttc.connect()

def publish(topic, value):
    mqttc.publish(topic, value)
    
while True:
    # check wifi connection
    if not pico_wifi.isconnected():
        pico_wifi.connect(config.WIFI_SSID, config.WIFI_PWD, verbose=False, led_toggle=True)
    reading = bme.read()
    temp,pres,humid = reading
    print(temp,pres,humid)
    publish('pico/temperature',str(temp).encode())
    publish('pico/humidity',str(humid).encode())
    publish('pico/pressure',str(pres).encode())
    time.sleep(300)
