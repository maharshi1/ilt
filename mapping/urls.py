from django.conf.urls import url, include
from mapping import views

urlpatterns = [
    url(r'^add-map$', views.add_map, name='lang_map'),
    url(r'^add-word/$', views.add_word, name='add_word'),
    url(r'^list-outlier$', views.list_outlier, name='list_outlier'),
    url(r'^$', views.view_actions, name='view_actions'),
    url(r'^(?P<language>[a-z]+)/map$', views.map_lang, name='map_lang'),
]

