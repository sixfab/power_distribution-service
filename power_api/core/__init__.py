import time

from .power_api import SixfabPower
from .exceptions import CRCCheckFailed
from helpers.exceptions import RetryLimitError

_hat_api = SixfabPower()

def hat_api(function: str, *args, **kwargs):
    func = getattr(_hat_api, function, None)

    if not func:
        return NotImplementedError("Function '{}' not exists!".format(func))

    try_count = 0
    while True:
        if try_count > 4:
            time.sleep(2)
            raise RetryLimitError()

        try:
            resp = getattr(_hat_api, function)(*args, **kwargs)
        except CRCCheckFailed:
            print("clearing pipe")
            _hat_api.clear_pipe()
        except Exception:
            pass
        else:
            return resp
        finally:
            try_count += 1

        time.sleep(.05)