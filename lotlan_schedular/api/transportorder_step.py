from lotlan_schedular.api.event import Event
from lotlan_schedular.api.location import Location


class TransportOrderStep:
    def __init__(self, name, location, triggered_by, finished_by):
        self.name = name
        self.location = location
        self.triggered_by = triggered_by
        self.finished_by = finished_by

    @classmethod
    def create_tos(cls, tos, events, locations):
        triggered_by_events = []
        finished_by_events = []

        for event_name, event_value, comparator in tos.triggered_by_events:
            if event_name != "":
                logical_name = events[event_name].name
                physical_name = events[event_name].keyval["name"]
                event_type = events[event_name].keyval["type"]
                triggered_by_events.append(Event(logical_name, physical_name, event_type, comparator, event_value))

        for event_name, event_value, comparator in tos.finished_by_events:
            if event_name != "":
                logical_name = events[event_name].name
                physical_name = events[event_name].keyval["name"]
                event_type = events[event_name].keyval["type"]
                finished_by_events.append(Event(logical_name, physical_name, event_type, comparator, event_value))

        location = locations[tos.location]
        logical_name = tos.location
        physical_name = location.keyval["name"]
        location_type = location.keyval["type"]

        location_api = Location(logical_name, physical_name, location_type)

        return TransportOrderStep(tos.name, location_api, triggered_by_events, finished_by_events)

    def __str__(self):
        return (("\n\t Name: {}\n\t Location: {}\n\t TriggeredBy:\t{}\n\t FinishedBy:\t{}\n\t")
                .format(self.name, self.location, self.triggered_by, self.finished_by))
