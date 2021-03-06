from django.conf.urls import url

from . import views

app_name="communitree_app"
urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^crops/(?P<id>[0-9]*)$', views.Crops.as_view(), name="crops"),
    url(r'^cropsbybounds$', views.CropsByBounds.as_view(), name="cropsbybounds"),
]
