from ..core import hat_api

def main(signal):
    signals = {
        'soft_reboot': "soft_reboot", 
        'soft_shutdown': "soft_power_off", 
        'hard_reboot': "hard_reboot", 
        'hard_shutdown': "hard_power_off", 
        'system_temperature': "send_system_temp",
        'battery_temperature': "send_battery_temp",
        'watchdog': "watchdog_signal"
    }

    if signal not in signals.keys():
        return {"err": "Signal not exists."}, 404

    value = hat_api(signals[signal])

    return {"value": {1: True, 2: False}.get(value, None)}, 200
