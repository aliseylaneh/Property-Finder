from django.core.exceptions import ValidationError


class AgentNotFound(Exception):
    def __init__(self):
        super(AgentNotFound, self).__init__("Agent doesn't exists.")


class InvalidEmailAddress(ValidationError):
    def __init__(self):
        super(InvalidEmailAddress, self).__init__("Invalid email address")


class InvalidPhoneNumber(ValidationError):
    def __init__(self):
        super(InvalidPhoneNumber, self).__init__("Invalid phone number")
