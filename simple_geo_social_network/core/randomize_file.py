import os
import uuid

from django.utils.deconstruct import deconstructible


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, instance, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        if hasattr(instance, 'content_type'):
            self.path = os.path.join(instance.content_type.model, "%s%s")
        extension = os.path.splitext(filename)[-1]
        return self.path % (uuid.uuid4(), extension)
