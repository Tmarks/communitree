from django.conf.urls import url

from . import views

app_name="communitree_app"
urlpatterns = [
    url(r'^viewy/$', views.Viewy.as_view(), name="viewy"),
    url(r'^facemake/$', views.Facemake.as_view(), name="facemake")
]