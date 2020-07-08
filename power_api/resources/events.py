from core import hat_api
from core.definitions import Definition
from core.event import Event
from flask import request

MAP_ACTIONS = {
    "start": Definition.HARD_POWER_ON,
    "shutdown_hard": Definition.HARD_POWER_OFF,
    "shutdown_soft": Definition.SOFT_POWER_OFF,
    "reboot_hard": Definition.HARD_REBOOT,
    "reboot_soft": Definition.SOFT_REBOOT,
    "start_soft" : Definition.SOFT_POWER_ON
}

MAP_DAYS = {
    "mon": Definition.MONDAY,
    "tue": Definition.TUESDAY,
    "wed": Definition.WEDNESDAY,
    "thu": Definition.THURSDAY,
    "fri": Definition.FRIDAY,
    "sat": Definition.SATURDAY,
    "sun": Definition.SUNDAY
}

MAP_INTERVAL_TYPE = {"seconds": 1, "minutes": 2, "hours": 3}



def get_event_ids():
    return {
        "ids": [id for id in hat_api("get_scheduled_event_ids")]
    }


def delete_event_by_ids():
    payload = request.get_json()

    if not payload or "ids" not in payload.keys():
        return {"err": "'ids' key required in request body as json."}, 400

    if type(payload["ids"]) != list:
        return {"err": "Event IDs must be integer."}, 403

    for id in payload["ids"]:
        hat_api(
            "remove_scheduled_event",
            int(id)
        )

    return {}, 200
    

def create_event():
    """
    {
        "events": [
            {
                "type": ""
            }
        ]
    }
    """

    event_types = {
        "time": ["id", "time", "frequency", "action"], # optional: days
        "interval": ["id", "frequency", "value", "action"] # optional: is_one_shot
    }

    payload = request.get_json()

    if not payload or "events" not in payload.keys():
        return {"err": "'events' key required in request body as json."}, 400

    if type(payload["events"]) != list:
        return {"err": "'events' must be an array."}, 400

    if not all([type(event) == dict for event in payload["events"]]):
        return {"err": "'events' must be an array of objects."}, 400

    for event in payload["events"]:
        event_to_save = Event()

        if event["type"] == "time":
            """

            try_until_done(api, "createScheduledEventWithEvent", event_to_save)
            """

            epoch_time = event["time"].split(":")
            epoch_time = int(epoch_time[0]) * 60 * 60 + int(epoch_time[1]) * 60

            days = 0
            if event["frequency"] == "daily":
                days = Definition.EVERYDAY
            else:
                if event.get("days", ""):
                    for day in event["days"].split(","):
                        days = days | MAP_DAYS[day]

            event_to_save.id = event["id"]
            event_to_save.schedule_type = Definition.EVENT_TIME
            event_to_save.repeat = (
                Definition.EVENT_ONE_SHOT
                if event["frequency"] == "once"
                else Definition.EVENT_REPEATED
            )
            event_to_save.time_interval = epoch_time
            event_to_save.day = days
            event_to_save.action = MAP_ACTIONS[event["action"]]


        elif event["type"] == "interval":
            """
            event_to_save.repeat = (
                Definition.EVENT_ONE_SHOT
                if event["interval_type"] == "once"
                else Definition.EVENT_REPEATED
            )

            try_until_done(api, "createScheduledEventWithEvent", event_to_save)
            """
            

            event_to_save.id = event["id"]
            event_to_save.schedule_type = Definition.EVENT_INTERVAL
            event_to_save.time_interval = int(event["value"])

            if event["frequency"] not in ("seconds", "minutes", "hours"):
                return {"err": "{} is not valid frequency for interval type events.".format(event["frequency"])}, 400
            else:
                event_to_save.interval_type = MAP_INTERVAL_TYPE[event["frequency"]]
                
            event_to_save.action = MAP_ACTIONS[event["action"]]

            event_to_save.repeat = (
                Definition.EVENT_ONE_SHOT
                if event.get("is_one_shot", False)
                else Definition.EVENT_REPEATED
            )

        hat_api("create_scheduled_event_with_event", event_to_save)

    return "asd"