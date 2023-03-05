from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def home(request):

    return render(request=request, template_name="index.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/accounts/', include("app_one.urls")),
    path('', home)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
