from resources import getters
from resources import setters
from resources import signals
from resources import events

urls = [
    (['GET'], '/metrics/<sensor>/<metric>', getters.get_metric_by_sensor),
    (['GET'], '/metrics/<metric>', getters.get_metric),
    (['GET'], '/configurations/<keyword>', getters.get_configurations),

    (['POST'], '/configurations', setters.set_configurations),

    (['GET'], '/signals/<signal>', signals.main),

    (['GET'], '/events', events.get_event_ids),
    (['POST'], '/events', events.create_event),
    (['DELETE'], '/events', events.delete_event_by_ids),
]