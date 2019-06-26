from django.urls import path, include

from django.conf.urls import url

from .views import *


from rest_framework import routers
from api.resources import test

router = routers.DefaultRouter()
router.register(r'api/test', test)


urlpatterns = [
    url(r'^$', LoginFormView.as_view(), name='login'),
    url(r'^(?P<pk>\d+)/grafica/$', login_required(grafica), name='grafica'),
    url(r'^simple/', login_required(simple_upload), name='simple_upload'),
    url(r'^list/', login_required(list.as_view()), name='list'),
    url(r'^grafica/', login_required(grafica.as_view()), name='grafica'),
    url(r'^borrar/', login_required(borrar.as_view()), name='borrar'),
    path('<int:id>/delete/', login_required(delete_view), name='delete'),
    url(r'^(?P<numb>\d+)/create_image/$', login_required(create_image), name='plot'),
	url(r'^register/$', RegisterFormView.as_view(), name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^prueba/$', prueba, name='prueba'),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls',namespace='rest_framework'))


]



