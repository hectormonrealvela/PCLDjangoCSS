from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from Document.models import Document
from django.urls import path








urlpatterns = [
                    url('', include('Document.urls')),
                    url(r'^admin/', (admin.site.urls)),




]


