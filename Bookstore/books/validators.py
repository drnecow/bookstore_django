from django.core.exceptions import ValidationError
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Validator for Book's cover_image field
def validate_cover_image(field_image):
    file_size = field_image.file.size
    limit_megabytes = 5

    if file_size > limit_megabytes * 1024 * 1024:
        raise ValidationError("Maximum accepted size of image is %s MB" % limit_megabytes)

    image = Image.open(field_image)
    max_height = 1920
    max_width = 1080

    width = image.size[0]
    height = image.size[1]

    if width > max_width or height > max_height:
        raise ValidationError("Image is larger than allowed. Maximum height: 1920, width: 1080")

    logger.debug("Cover image successfully uploaded to the server: validate_image")


# Validator for Book's isbn field
def validate_isbn(input_string):
    if len(input_string) != 13 or not input_string.isdigit():
        raise ValidationError("Input isn't valid ISBN. ISBN must contain exactly 13 decimal numbers.")
