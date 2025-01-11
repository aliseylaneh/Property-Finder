class EventNotFound(Exception):
    def __init__(self):
        super(EventNotFound, self).__init__("Event doesn't exists.")
