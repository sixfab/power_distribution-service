import time
from threading import Thread
from requests import get, post

SERVICE_ADDR = "http://localhost:6060"

def test_read_system_current():
    while True:
        value = get("http://localhost:6060/metrics/system/current").json().get("value", None)
        if not value:
            print("GOT ERROR: system temp")
        print("System current: ", value)


def test_read_rtc():
    while True:
        value = get("http://localhost:6060/metrics/rtc").json().get("value", None)
        if not value:
            print("GOT ERROR: rtc time")
        print("RTC timestamp: ", value)


if __name__ == "__main__":
    Thread(target=test_read_system_current).start()
    Thread(target=test_read_rtc).start()
