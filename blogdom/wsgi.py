import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling
# from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogdom.settings")
application = get_wsgi_application()
# application = Cling(MediaCling(get_wsgi_application()))
# application = DjangoWhiteNoise(application)
