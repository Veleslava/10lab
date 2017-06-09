
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^todolists/$', All_lists),
    url(r'^todolists/create/$', CreateList),
    url(r'^login/$', LogIn),
    url(r'^logout/$', LogOut),
    url(r'^todolists/shared/$', SharedListView),
    url(r'^todolists/shared/(?P<list_id>[0-9]+)/$', SharedTasksView),
    url(r'^todolists/(?P<pk>[0-9]+)/$', Tasks),
    url(r'^todolists/(?P<pk>[0-9]+)/create_task/$', CreateTask),
    url(r'^todolists/(?P<list_id>[0-9]+)/share/$', ToShare),
    url(r'^sign_up/$', Registration),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskEdit),
    url(r'^todolists/(?P<list_id>[0-9]+)/delete/(?P<pk>[0-9]+)/$', TaskDelete),
    url(r'^todolists/(?P<list_id>[0-9]+)/delete/$',ListDelete),
    url(r'^todolists/(?P<list_id>[0-9]+)/edit/$',ListEdit),

}

urlpatterns = format_suffix_patterns(urlpatterns)