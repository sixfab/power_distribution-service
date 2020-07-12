import os
import time

from .. import app
from ..core import _hat_api
from threading import Thread
from flask import request, session, current_app

break_thread = False

def lock():
    def coutdown_and_release(app):
        global break_thread
        start_time = time.time()

        while (time.time() - start_time) < 180:
            time.sleep(.5)
            if break_thread:
                break_thread = False
                return
        
        app.config["locked"] = False
        return

    current_app.config["locked"] = True

    Thread(target=coutdown_and_release, args=(app,)).start()
    return {"msg": "Service locked."}, 200


def release():
    global break_thread

    current_app.config["locked"] = False
    break_thread = True
    
    return {"msg": "Service released."}, 200
