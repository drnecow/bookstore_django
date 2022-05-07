from django.core.exceptions import ValidationError


def validate_reception_type(input_string):
    if (not input_string == 'delivery') and not (input_string == 'pickup'):
        raise ValidationError("Order reception type can only be delivery or pickup")
