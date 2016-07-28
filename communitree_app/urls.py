from django.conf.urls import url

from . import views

app_name="communitree_app"
urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^querydb/$', views.QueryDB.as_view(), name="querydb"),
]