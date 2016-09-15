from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.generic import View
from django.core.urlresolvers import reverse
from .models import CropFeature
import json
from django.contrib.gis.geos import Polygon

from .forms import FaceForm


class Index(View):
    def get(self, request):
        return render(request, "communitree_app/index.html")


class Crops(View):
    def get(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id'] != '':
            try:
                return JsonResponse(CropFeature.objects.get(id=kwargs['id']).geojson)
            except CropFeature.DoesNotExist:
                raise Http404("The requested crop does not exist.")

        elif 'bounds' in request.GET:
            # request.GET['bounds'] is the return value from LeafletJS's
            # Map.getBounds().toBBoxString().
            # That's 'southwest_lng,southwest_lat,northeast_lng,northeast_lat'
            # So this fits what Polygon.from_bbox expects.
            # ... except I think if the box crosses the International Date Line, or
            # if it would contain a pole.
            # TODO: Might be worth figuring this out some day, though no one's
            # gonna find any blueberries in the middle of the pacific or at the
            # South Pole.
            bounds = [float(x) for x in request.GET['bounds'].split(',')]

            print bounds
            print bounds[0]
            print bounds[1]
            print bounds[2]
            print bounds[3]
            bounds_polygon = Polygon.from_bbox(bounds)
            print bounds_polygon
            cropfeatures_in_view = [cf.geojson for cf in CropFeature.objects.filter(mpoly__intersects=bounds_polygon)]
            return JsonResponse(cropfeatures_in_view, safe=False)
                
        else:
            #TODO: I'm not sure what to do about this. For now, I'm just going to give it SOMEthing to do.
            #As of the moment though, I don't have a use case for getting CropFeatures in some order they happen to
            #come in when retrieved.
            return JsonResponse([cf.geojson for cf in CropFeature.objects.all()[:100]], safe=False)
    
