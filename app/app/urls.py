from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('graphql', csrf_exempt(GraphQLView.as_view()))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns.append(path('admin/', admin.site.urls))
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
