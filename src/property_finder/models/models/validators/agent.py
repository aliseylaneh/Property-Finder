import re

from src.property_finder.models.exceptions.agent import InvalidEmailAddress, InvalidPhoneNumber

regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def validate_email(value: str):
    if not re.fullmatch(regex_email, value):
        raise InvalidEmailAddress()


def validate_phone_number(value: str):
    if not (value.isdigit() and len(value) >= 1):
        raise InvalidPhoneNumber()
