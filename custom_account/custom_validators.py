from django.core.validators import ValidationError
from validate_email import validate_email
import re


def validate_phone_number_or_email(email_phone):
    if email_phone.isnumeric():
        phone = email_phone
        if not re.search(r"^[1][1739685]\d{8}", phone):
            raise ValidationError('Invalid phone number')
        else:
            return phone
    else:
        email = email_phone
        if not validate_email(email, verify=True):
            raise ValidationError('Invalid Email')
        else:
            return email
