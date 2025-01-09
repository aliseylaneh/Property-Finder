class PropertyNotFound(Exception):
    def __init__(self):
        super(PropertyNotFound, self).__init__("Property doesn't exists.")
