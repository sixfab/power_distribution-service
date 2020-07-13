import os
import time

from .. import app
from ..core import _hat_api
from threading import Thread
from flask import request, session, current_app


def lock():
    current_app.config["locked"] = time.time() + 180
    return {"msg": "Service locked."}, 200


def release():
    current_app.config["locked"] = False
    return {"msg": "Service released."}, 200
