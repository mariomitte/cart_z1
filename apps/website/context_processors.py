from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Website



def website(request):
    id = settings.SITE_ID
    website = get_object_or_404(Website, id=id)
    return {'website': website}
