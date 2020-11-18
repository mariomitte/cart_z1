import os

from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFit
#
# # Image resize defaults
# thumbnail_size = settings.IMAGE_THUMBNAIL_SIZE
# preview_size = settings.IMAGE_PREVIEW_SIZE


# def _validate_file_extension(value):
#     try:
#         ext = os.path.splitext(value.name)[1]
#         valid_extensions = ['.svg', '.png']
#         if not ext.lower() in valid_extensions:
#             raise ValidationError('Must be a valid file type.')
#     except ValidationError:
#         raise ValidationError('Must be a valid file type.')

class Website(models.Model):
    """
    A Website model
    """
    website = models.OneToOneField(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH, null=True, blank=True)
    description = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH, null=True, blank=True)
    logo = models.ImageField(upload_to='website')
    header_image = models.ImageField(upload_to='website')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'website'
        verbose_name_plural = 'websites'

    def __str__(self):
        return self.title
