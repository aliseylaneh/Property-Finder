class PropertyTypeNotFound(Exception):
    def __init__(self):
        super(PropertyTypeNotFound, self).__init__("Type doesn't exists.")


class MainTypeNotFound(Exception):
    def __init__(self):
        super(MainTypeNotFound, self).__init__("Main type doesn't exists.")


class SubTypeNotFound(Exception):
    def __init__(self):
        super(SubTypeNotFound, self).__init__("Sub type doesn't exists.")


class PropertyTypeErrorAssignment(Exception):
    def __init__(self):
        super(PropertyTypeErrorAssignment, self).__init__("You can't assign the same ID for main type and sub type together.")
