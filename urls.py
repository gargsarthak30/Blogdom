from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/blogs/')),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^user_account/', include('user_account.urls')),

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

