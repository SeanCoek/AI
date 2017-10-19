from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    # url(r'^index/', views.index),
    url(r'^rule_add/', views.rule_add),
    url(r'^api/animal_rec/', views.animal_rec)
]