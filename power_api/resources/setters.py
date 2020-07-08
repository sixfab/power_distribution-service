from flask import request
from core import hat_api


def set_configurations():
    """
        fan:
            - slow_threshold
            - fast_threshold, default: 100

        battery:
            - safe_shutdown_level, optional
            - max_charge_level, optional

        rtc:
            - timestamp
    """
    request_json = request.get_json()

    configuration_fields = {
        "fan": ["slow_threshold"],
        "battery": [],
        "rtc": ["timestamp"],
        "watchdog": ["is_enabled"],
        "rgb": ["type"],
    }

    if not request_json:
        return {"err": "Json body missing."}, 400

    for key, value in request_json.items():
        if key not in configuration_fields.keys():
            return (
                {"err": "Key '{}' is not valid configuration key.".format(key)},
                404,
            )

        if not all(
            [
                required_configuration_key in value
                for required_configuration_key in configuration_fields[key]
            ]
        ):
            return (
                {"err": "Required fields not exists for '{}'.".format(key)},
                400,
            )

        if not value:
            return (
                {"err": "At least one field required to update configurations. The dictionary of '{}' is blank".format(key)},
                400,
            )

        if not type(value) == dict:
            return {"err": "Configuration data must be object."}, 400

        if key == "fan":
            hat_api(
                "set_fan_automation",
                value["slow_threshold"],
                fast_threshold=value.get("fast_threshold", 100),
            )

        if key == "battery":
            if "safe_shutdown_level" in value:
                hat_api("set_safe_shutdown_battery_level", value["safe_shutdown_level"])

            if "max_charge_level" in value:
                hat_api("set_battery_max_charge_level", value["max_charge_level"])

            if "design_capacity" in value:
                hat_api("set_battery_design_capacity", value["design_capacity"])

        if key == "rtc":
            hat_api("set_rtc_time", value["timestamp"])

        if key == "watchdog":
            hat_api("set_watchdog_status", {True: 1, False: 2}[value["is_enabled"]])

        if key == "rgb":
            if value["type"] not in ("disabled", "heartbeat", "temperature_map"):
                return (
                    {"err": "Animation type '{}' is not valid for RGB animation.".format(value["type"])},
                    400,
                )

            hat_api(
                "set_rgb_animation",
                {"disabled": 1, "heartbeat": 2, "temperature_map": 3}[value["type"]],
                {
                    "green": 1,
                    "blue": 2,
                    "red": 3,
                    "yellow": 4,
                    "cyan": 5,
                    "magenta": 6,
                    "white": 7,
                }[value.get("color", "green")],
                {"slow": 1, "normal": 2, "fast": 3}[value.get("speed", "normal")],
            )

    return {"msg": "Configurations updated."}, 200
