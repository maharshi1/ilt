from django.conf.urls import url, include
from mapping import views

urlpatterns = [
    url(r'^add-map$', views.add_map, name='lang_map'),
    url(r'^add-word$', views.add_word, name='add_word'),
    url(r'^list-outlier', views.list_outlier, name='add_word'),
]

