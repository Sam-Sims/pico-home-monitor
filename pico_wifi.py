import network
import time
from machine import Pin

wlan = network.WLAN(network.STA_IF)

def check_status(status):
        if status == network.STAT_IDLE:
            return "STAT_IDLE"
        if status == network.STAT_CONNECTING:
            return "STAT_CONNECTING"
        if status == network.STAT_WRONG_PASSWORD:
            return "STAT_WRONG_PASSWORD"
        if status == network.STAT_NO_AP_FOUND:
            return "STAT_NO_AP_FOUND"
        if status == network.STAT_CONNECT_FAIL:
            return "STAT_CONNECT_FAIL"
        if status == network.STAT_GOT_IP:
            return "STAT_GOT_IP"
        else:
            return "STAT_NO_ERROR_CODE"

def connect(ssid, pwd, retry_timeout=10, led_toggle=False, verbose=False):
    if led_toggle:
        led = Pin("LED", Pin.OUT)
        led.off()

    wlan.active(True)
    if verbose:
        print(f"Connecting to {ssid} with a timeout of {retry_timeout} seconds...")
    wlan.connect(ssid, pwd)

    while retry_timeout > 0 and wlan.isconnected() == False:
        retry_timeout -= 1
        if verbose:
            print("Waiting for connection...")
            time.sleep(1)

    if wlan.isconnected() == False:
        print("Connection failed")
        time.sleep(1)
        wlan.disconnect()
        print(wlan.status())
        raise RuntimeError(check_status(wlan.status()))
    elif wlan.isconnected():
        print("Connected to WLAN!")
        if led_toggle:
            led.on()
        if verbose:
            check_status(wlan.status())
            print(f"IP: {wlan.ifconfig()[0]}")


def get_ip():
    if wlan.isconnected():
        return wlan.ifconfig()[0]
    else:
        raise RuntimeError("No connection found")
