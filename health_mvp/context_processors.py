from django.conf import settings

def color_palette(request):
    return {'COLOR_PALETTE': settings.COLOR_PALETTE}