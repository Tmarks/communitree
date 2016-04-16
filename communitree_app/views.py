from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from .models import CropFeature
import json
from django.contrib.gis.geos import Polygon

from .forms import FaceForm


class Index(View):
    def get(self, request):
        return render(request, "communitree_app/index.html")


class Viewy(View):
    def get(self, request):
        form = FaceForm()
        return render(request, "communitree_app/face.html", {'form': form})

    def post(self, request):
        form = FaceForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("communitree_app:facemake"))


class Facemake(View):
    def get(self, request):
        form = FaceForm(request.POST)
        # already validated in Viewy.post()?
        # uh
        return JsonResponse({'foo': 'bar'})


class QueryDB(View):
    def get(self, request):
        """
        Send all of the CropFeature polygons from the database within the received Bounding Box.
        :param request HttpRequest object -- request.GET["bounds"] should be the
        bounding box as a string.
        :return JSONResponse containing "cropfeatures", a list of GeoJSON
        objects representing the CropFeatures found:
        """

        # request.GET["bounds"] is the return value from LeafletJS's
        # Map.getBounds().toBBoxString().
        # That's 'southwest_lng,southwest_lat,northeast_lng,northeast_lat'
        # So this fits what Polygon.from_bbox expects.
        # ... except I think if the box crosses the International Date Line, or
        # if it would containa  pole.
        # TODO: Might be worth figuring this out some day, though no one's growing
        # any cucumbers in the middle of the pacific or at the south pole
        print request.GET
        bounds = [float(x) for x in request.GET['bounds'].split(',')]
        bounds_polygon = Polygon.from_bbox(bounds)
        cropfeatures_in_view = [cf.geojson for cf in CropFeature.objects.filter(mpoly__touches=bounds_polygon)]
        return JsonResponse({"cropfeatures": cropfeatures_in_view})

        """
        cf = CropFeature.objects.last()
        return JsonResponse({"cropfeature": {"name": cf.name,
                                             "species": cf.species,
                                             "mpoly": json.loads(cf.mpoly.geojson)
                                             }
                             })
        # return JsonResponse({"cropfeature" : CropFeature.objects.last().mpoly.geojson})
        """


class JQTesty(View):
    def get(self, request):
        print request.GET
        print type(request.GET)
        resp = {}
        for d in request.GET:
            resp[d.upper()] = request.GET[d]*3
        return JsonResponse({'eh': resp})
