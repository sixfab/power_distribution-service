import re
from ..core import hat_api


def get_metric_by_sensor(sensor, metric):
    available_metrics = {
        "battery": ("temperature", "voltage", "current", "power", "level", "health"),
        "system": ("temperature", "voltage", "current", "power"),
        "input": ("temperature", "voltage", "current", "power"),
        "fan": ("health", "speed"),
    }

    if sensor not in available_metrics.keys() or metric not in available_metrics.get(
        sensor, ()
    ):
        return {"err": "Sensor or metric name is not valid."}, 400

    if metric == "temperature":
        metric = (
            "temp"  # 'temperature' is not valid keyword for power_api, must be 'temp'
        )

    value = hat_api("get_{}_{}".format(sensor, metric))

    return {
        "sensor": sensor,
        "metric": metric,
        "value": value
    }


def get_metric(metric):
    metrics = {
        "working_mode": "get_working_mode",
        "rtc": "get_rtc_time",
        "version": "get_firmware_ver",
        "button1": "get_button1_status",
        "button2": "get_button2_status"
    }

    if metric not in metrics.keys():
        return {"err": "Metric '{metric}' is not exists.".format(metric=metric)}, 404

    value = hat_api(metrics[metric])

    if metric == "working_mode":
        value = {
            1: "charging",
            2: "fully_charged",
            3: "battery_powered"
        }[value]

    elif metric == "version":
        if isinstance(value, str):
            value = re.search("v([0-9]*.[0-9]*.[0-9]*)", value)[1]
        elif isinstance(value, bytearray) or isinstance(value, bytes):
            value = value.decode().replace("v", "")
        else:
            value = '0.0.0'

    elif metric.startswith("button"):
        value = {
            1: "short_press",
            2: "long_press",
            3: "released"
        }[value]

    return {"metric": metric, "value": value}


def get_all_metrics():
    metrics = [
        "working_mode",
        "rtc",
        "version",
        "button1",
        "button2"
    ]

    sensor_metrics = {
        "battery": ("temperature", "voltage", "current", "power", "level", "health"),
        "system": ("temperature", "voltage", "current", "power"),
        "input": ("temperature", "voltage", "current", "power"),
        "fan": ("health", "speed"),
    }

    response = {
        "metrics": {}
    }

    for metric in metrics:
        response["metrics"][metric] = get_metric(metric)["value"]


    for sensor, metrics in sensor_metrics.items():
        for metric in metrics: 
            if sensor not in response["metrics"]:
                response["metrics"][sensor] = {}
                
            response["metrics"][sensor][metric] = get_metric_by_sensor(sensor, metric)["value"]

    return response


def get_configurations(keyword):
    keywords = {
        "led": "get_rgb_animation",
        "watchdog": "get_watchdog_status",
        "fan": "get_fan_automation",
        "battery": "get_safe_shutdown_battery_level",
        "rtc": "get_rtc_time"
    }

    if keyword not in keywords.keys():
        return {"err": "The key '{}' is not valid configuration key.".format(keyword)}, 404

    value = hat_api(keywords[keyword])

    if keyword == "watchdog":
        value = True if hat_api("get_watchdog_status") == 1 else False

    elif keyword == "led":
        value = {
            "type": {1: "disabled", 2: "heartbeat", 3: "temperature_map"}[value[0]],
            "color": {
                1: "red",
                2: "green",
                3: "blue",
                4: "yellow",
                5: "cyan",
                6: "magenta",
                7: "white",
                8: "black",
            }[value[1]],
            "speed": {1: "slow", 2: "normal", 3: "fast"}[value[2]],
        }

    elif keyword == "fan":
        value = {"slow_threshold": value[0], "fast_threshold": value[1]}

    elif keyword == "battery":
        value = {
            "safe_shutdown": value,
            "max_charge": hat_api("get_battery_max_charge_level"),
            "design_capacity": hat_api("get_battery_design_capacity")
        }

    return {"key": keyword, "value": value}
