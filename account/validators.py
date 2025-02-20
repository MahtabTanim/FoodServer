from django.core.exceptions import ValidationError
import os


def allow_only_image_validator(value):
    ext = os.path.splitext(value.name)[1]
    allowed_ext = [
        ".png",
        ".jpg",
        ".jpeg",
    ]
    if ext.lower() not in allowed_ext:
        raise ValidationError(
            "Unsupported file provided , Supported : " + str(allowed_ext)
        )
