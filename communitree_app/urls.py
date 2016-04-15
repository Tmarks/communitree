from django.conf.urls import url

from . import views

app_name="communitree_app"
urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^viewy/$', views.Viewy.as_view(), name="viewy"),
    url(r'^facemake/$', views.Facemake.as_view(), name="facemake"),
    url(r'^querydb/$', views.QueryDB.as_view(), name="querydb"),
    url(r'^jqtesty/$', views.JQTesty.as_view(), name="jqtesty"),
]